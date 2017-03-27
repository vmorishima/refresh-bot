import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# requirements: pip install selenium, install chromedriver to PATH

# recommend to run with caffeinate on mac



def refresh_bot(url, searchstring, comment):
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

username = raw_input("Please enter your da username:")
password = getpass.getpass("Please enter your da password:")

user = raw_input("Please enter the username of the user whose journals you wish to search:")

url = "http://" + user + ".deviantart.com/journal/"

searchstring = str(raw_input("Please enter the term you wish to search for:"))
comment = str(raw_input("Please enter the text you wish to comment on the journal:"))
# change how many seconds between refreshes here
wait_time = int(raw_input("Please enter time (in seconds) between refreshes here:"))
if wait_time < 60:
    wait_time = int(raw_input("Please enter a value greater than 60:"))

# logging in to da
print "Logging you in..."
driver = webdriver.Chrome()
driver.get("https://www.deviantart.com/users/login?ref=http://www.deviantart.com/")
username_box = driver.find_element_by_id("login_username")
password_box = driver.find_element_by_id("login_password")
username_box.send_keys(username)
password_box.send_keys(password)
password_box.send_keys(Keys.RETURN)

refresh_bot(url, searchstring, comment)
