from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime

path = "D:\chromedriver-win64\chromedriver.exe"
s = Service(path)
driver = webdriver.Chrome(service=s)
driver.get("https://www.aqi.in/dashboard/vietnam/da-nang,da-nang,da-nang,vietnam/da-nang")
time.sleep(2)

item = driver.find_element(By.CSS_SELECTOR, "div.calendar_id1")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", item)
action = ActionChains(driver)
indexes = driver.find_elements(By.XPATH, "//*[@id='calendar_id']/div/div[1]/div[3]/div/div[1]/div[1]/ul/li")
list_indexes = {"pm2.5", "pm10", "o3", "no2", "so2", "co"}
start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2024, 10, 7)
range_date = pd.date_range(start_date, end_date)
data = {"date_time": range_date,
        "pm2.5": [None] * len(range_date),
        "pm10": [None] * len(range_date),
        "o3": [None] * len(range_date),
        "no2": [None] * len(range_date),
        "so2": [None] * len(range_date),
        "co": [None] * len(range_date)}
df = pd.DataFrame(data)
dict_month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
for val in indexes:
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[@id='calendar_id']/div/div[1]/div[3]/div/div[1]/div").click()
    wait = WebDriverWait(driver, 3).until(EC.element_to_be_clickable(val))
    val.click()
    param = val.text.lower()
    print(param)
    if param not in list_indexes:
        continue
    years = driver.find_elements(By.XPATH, "//*[@id='calendar_id']/div/div[1]/div[3]/div/div[2]/div/ul/li")
    for year in years:
        driver.find_element(By.XPATH, "//*[@id='calendar_id']/div/div[1]/div[3]/div/div[2]/div").click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable(year))
        year.click()
        year_ = year.text
        time.sleep(3)
        search = driver.find_elements(By.CSS_SELECTOR, "rect.day")
        for day in search:
            tmp = day.text.split(': ')
            if len(tmp) == 2:
                date_time = f"{tmp[0]}-{year_}"[5:].split("-")
                dt = pd.Timestamp(year=int(date_time[2]), month=dict_month[date_time[1]], day=int(date_time[0]))
                df.loc[df["date_time"] == dt, param] = int(tmp[1])
        time.sleep(2)
time.sleep(3)
driver.quit()



