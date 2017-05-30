import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# requirements: pip install selenium, install chromedriver to PATH

# recommend to run with caffeinate on mac

driver = webdriver.Chrome()

def login(username, password):
    print "Logging you in..."
    driver.get("https://www.deviantart.com/users/login?ref=http://www.deviantart.com/")
    username_box = driver.find_element_by_id("login_username")
    password_box = driver.find_element_by_id("login_password")
    username_box.send_keys(username)
    password_box.send_keys(password)
    password_box.send_keys(Keys.RETURN)

def gallery_refresh(url):
    driver.get(url)
    # get original url to check against updates
    original_elem = driver.find_element_by_css_selector(".torpedo-container .thumb .torpedo-thumb-link")
    original_href = str(original_elem.get_attribute("href"))
    print original_elem
    print original_href
    outerloop = True

    while outerloop:
        print 'Checking first deviation for original term'
        elem = driver.find_element_by_css_selector(".torpedo-container .thumb .torpedo-thumb-link")
        href = str(elem.get_attribute("href"))

        if href != original_href:
            print 'Update found:', href
            driver.find_element_by_css_selector(".torpedo-container .thumb .torpedo-thumb-link").click()
            print '\a'
        else:
            print 'Update not found. Waiting for', wait_time, 'seconds.'
            time.sleep(wait_time)
            print 'Refreshing...'
            driver.refresh()

def journal_refresh(url, searchstring, comment):
    driver.get(url)
    outerloop = True
    # strips case from searchstring
    searchstring = str(searchstring).lower()

    while outerloop:
        print 'Checking first journal text for', searchstring
        # selects first journal entry for testing
        elem = driver.find_element_by_css_selector("ul.f.list li.f")
        # strips case from element text
        text = str(elem.text).lower()

        if searchstring in text:
            print 'found it!'
            driver.find_element_by_css_selector("ul.f.list li.f > a").click()
            driver.find_element_by_css_selector("textarea#commentbody").click()
            textarea = driver.find_element_by_css_selector(".ccwriter-content > .writer.selectable")
            textarea.send_keys(comment)
            driver.find_element_by_css_selector("a.smbutton.smbutton-green.smbutton-big.comment-submit").click()
            outerloop = False
            print 'Successfully commented!'
            print '\a'
        else:
            print 'String not found. Waiting for', wait_time, 'seconds.'
            time.sleep(wait_time)
            print 'Refreshing...'
            driver.refresh()

username = raw_input("Please enter your da username: ")
password = getpass.getpass("Please enter your da password: ")
wait_time = int(raw_input("Please enter time (in seconds) between refreshes here: "))
if wait_time < 60:
    wait_time = int(raw_input("Please enter a value greater than 60: "))

user = raw_input("Please enter the username of the user whose journals/deviations you wish to search: ")
search_type = int(raw_input("Please enter 1 to search journals, 2 to search deviations: "))

if search_type == 1:
    url = "http://" + user + ".deviantart.com/journal/"

    searchstring = str(raw_input("Please enter the term you wish to search for: "))
    comment = str(raw_input("Please enter the text you wish to comment on the journal: "))
    login(username, password)
    journal_refresh(url, searchstring, comment)


if search_type == 2:
    url = "http://" + user + ".deviantart.com/gallery/"
    login(username, password)
    gallery_refresh(url)
