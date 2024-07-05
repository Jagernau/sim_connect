from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config

options = Options()

browser = webdriver.Remote(
    command_executor=f"http://{config.USER_IP}>:4444/wd/hub",
    options=options
)

browser.get("https://www.google.com")

print(browser.title)

browser.quit()
