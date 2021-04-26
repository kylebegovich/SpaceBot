from selenium import webdriver
from datetime import datetime as dt
import smtplib, ssl

NOW = dt.now()

def get_credentials():
    with open('credentials.txt', 'r') as credentials:
        lines = credentials.readlines()
        return lines[0], lines[0], lines[1]

def parse_time(to_parse):
    hour = int(to_parse[:2])
    min = int(to_parse[3:5])
    if "PM" in to_parse:
        hour += 12
    return hour, min


def send_email(sender_email, receiver_email, password, email_content):
    port = 465  # For SSL
    message = "Subject: Automated Email From BotBrain\n\n" + \
            email_content + \
            "\n\n~~~\nThis message is sent from Python."

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# actually executes the desired action in the desired time
def executor(sender_email, receiver_email, password, minutes_until_launch):
    send_email(sender_email, receiver_email, password, "here is the number of minutes until launch: %s" % minutes_until_launch)


def time_differ(line):
    launch_hour, launch_minute = parse_time(line)
    diff_hours = launch_hour - NOW.hour
    diff_minutes = launch_minute - NOW.minute
    diff_minutes += diff_hours * 60

    # return if launch has already happened
    if diff_minutes < 0:
        print("exiting, no launches remaining for the day")
        exit()

    return diff_minutes


def web_parser():
    driver = webdriver.Chrome('/Users/kylebegovich/Desktop/IndependentCode/WebScraping/SpaceBot/ChromeDriver/chromedriver')

    driver.get('https://www.rocketlaunch.live/')
    launchloop_element = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div[1]')[0]
    ll_text = launchloop_element.text
    for line in ll_text.split('\n'):
        if "PM" in line or "AM" in line:
            return line


def runner():
    print("program start")
    sender, receiver, pw = get_credentials()
    print("credentials fetched")
    time_line = web_parser()
    print("web_parser complete")
    diff_minutes = time_differ(time_line)
    print("time_differ complete")
    executor(sender, receiver, pw, diff_minutes)
    print("executor complete")

runner()
