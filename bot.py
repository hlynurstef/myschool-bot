#!/usr/bin/env python

"""
A bot for signing up for events on MySchool.

Make sure you have installed all the required third-party
python modules by running the following command:

pip install -r requirements.txt

Then the script is run by simply calling it with python:

python bot.py

You will be asked to enter the event URL and your username and password
for MySchool. The bot will not start until you are ready to start.
Once it starts it will continuously try to click the submit button until
it's successful and then the bot will terminate.

Step 1. Run bot
Step 2. ?
Step 3. Enjoy your beer
"""

# Built-in modules:
from getpass import getpass
import re
# Third-party modules:
import requests as r
from bs4 import BeautifulSoup as soup

__author__ = "Hlynur Stefánsson"
__copyright__ = "Copyright 2017, Hlynur Stefánsson"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Hlynur Stefánsson"
__email__ = "hlynurs15@ru.is"
__status__ = "Production"

def main():
    """ The main function of the program. """
    fancy_print('Welcome to the MySchool event registration bot!')

    # Get URL, username and password, try logging in an parse the resulting html page
    url = get_url()
    response = login(url)
    page = soup(response[0].text, "html.parser")

    # Check if user has already registered to the event
    if already_registered(page):
        fancy_print('You are already registered to this event! Enjoy your beer!')
        return

    # Find the url that should be used to send the POST request to sign up
    post_url = 'https://myschool.ru.is/myschool/'+page.find('form', {'name': 'register'})['action']

    # Allow the user to dictate when the bot starts trying to sign up for the event
    start = input('Start the bot? (y/n): ')
    if start.lower() == 'y':
        register(post_url, response[1])
    else:
        fancy_print('Goodbye!')


def get_user_pass():
    """ Gets and returns the username and password. """
    return (input('Username: '), getpass())


def get_url():
    """ Gets the url from the user """
    # Regex to check if this is a MySchool URL
    reg = re.compile('http[s]*://myschool.ru.is/myschool/')
    while True:
        url = input('Event URL: ')
        if reg.match(url):
            return url
        else:
            print('--> Invalid url, please enter a valid MySchool URL.')


def login(url):
    """ Lets user log in and returns the page response when successful. """
    while True:
        # Get the username and password
        auth = get_user_pass()
        # Login and get the even page
        response = r.get(url, auth=auth)

        if response.ok:
            print('--> Successfully logged into MySchool!')
            return (response, auth)
        else:
            print('--> Failed to login, try again.')


def register(post_url, auth):
    """ Registers the user to Viso """
    while True:
        # Send a POST request
        response = r.post(post_url, data={'pls': 'register'}, auth=auth)
        # Parse the resulting html page
        page_soup = soup(response.text, "html.parser")

        # Check if register was successful
        if response.ok and already_registered(page_soup):
            fancy_print('Successfully registered! Enjoy your beer!')
            return


def already_registered(page_soup):
    """ Check if user is already registered to Viso """
    return page_soup.find('input', {'name': 'ruButton'})['value'] == 'Afskrá'


def fancy_print(str):
    """ Prints a fancy string """
    line = '═'*(len(str)+6)
    print('╔' + line + '╗')
    print('║ ~ ' + str + ' ~ ║')
    print('╚' + line + '╝')


if __name__ == "__main__":
    main()
