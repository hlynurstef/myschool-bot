""" A bot for signing up for Vísindaferð on MySchool """

from getpass import getpass
import requests as r
from bs4 import BeautifulSoup as soup

def main():
    """ The main function of the program. """

    # TODO: get url from command line

    url = 'https://myschool.ru.is/myschool/?Page=Exe&ID=2.23&sID=2&e=2427'

    # Get the username and password
    auth = get_user_pass()

    response = r.get(url, auth=auth)

    page_soup = soup(response, "html.parser")

    button = page_soup.find("input", {"name": "ruButton"})

    print(button)


def get_user_pass():
    """ Gets and returns the username and password. """
    return (input('Username: '), getpass())


if __name__ == "__main__":
    main()
