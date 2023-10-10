from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()
driver.get("https://www.binance.com/en/trading-bots")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "css-1bshycy"))
    )
finally:

    BOTmp = driver.find_element(By.ID, "botMarketPlace")
    ROIp = BOTmp.find_elements(By.CLASS_NAME, "css-1bshycy")

    for i in range(0, len(ROIp)):
        print(ROIp[i].text)

driver.close()
