from splinter import Browser
from time import sleep
from sys import argv
import re
import os

CODES = {
    'LAX': 5180,
    'SFO': 5446,
    'LBC': 8920
}

months = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december'
]

def run_script(browser, code):
    log_in(browser)
    res = check_appointment(browser, CODES[code])
    if res is None:
        print 'no appointment'
    print res

def get_date(browser):
    text = ' '.join(node.text for node in browser.find_by_css('.background .header .date td')).lower()
    year = None
    month = None
    day = None
    for part in re.split('[^a-z0-9]+', text):
        isint = False
        try:
            int(part)
            isint = True
        except:
            pass
        if isint:
            if len(part) == 4:
                year = int(part)
            elif len(part) == 2:
                day = int(part)
            else:
                1/0
        else:
            try:
                month = months.index(part) + 1
            except:
                pass
    return (year, month, day)


def log_in(browser):
    url = "https://goes-app.cbp.dhs.gov/goes/HomePagePreAction.do"
    browser.visit(url)
    browser.fill('j_username', os.environ['USERNAME'])
    browser.fill('j_password', os.environ['PASSWORD'])
    sign_in_button = browser.find_by_css('#SignIn')
    if not sign_in_button:
        1/0
    sign_in_button.click()
    check_me = browser.find_by_css('#checkMe')
    if not check_me:
        1/0
    check_me.click()


#Select another center
def check_appointments(browser, codes):
    if not codes:
        return
    manage = browser.find_by_css('[name=manageAptm]')
    if not manage:
        1/0
    manage.click()
    reschedule = browser.find_by_css('input[name=reschedule]')
    if not reschedule:
        1/0
    reschedule.click()
    for code in codes:
        option = browser.find_by_css('input[value="%s"]' % code)
        if not option:
            1/0
        option.click()
        next_button = browser.find_by_css('input[name=next]')
        if not next_button:
            1/0
        next_button.click()
        if browser.is_text_present('no available'):
            yield None
        else:
            yield get_date(browser)


def get_browser():
    return Browser('chrome', executable_path='./chromedriver')

if __name__ == '__main__':
    with get_browser() as browser:
        browser = get_browser()
        code = 'LAX'
        if len(argv) > 1:
            code = argv[1]
        run_script(browser, code)
