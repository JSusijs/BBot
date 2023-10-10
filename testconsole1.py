from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm")

elem = driver.find_element(By.TAG_NAME, "h1")
print(elem.text)

elements = driver.find_elements(By.CLASS_NAME, "whs2")

for i in range(0, len(elements)):
    print(elements[i].text)

print(elements[3].text)

assert "No results found." not in driver.page_source
driver.close()