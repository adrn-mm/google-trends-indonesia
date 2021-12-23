from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://trends.google.com/trends/yis/2021/ID/"

driver = webdriver.Firefox()
driver.get(url)

# <span ng-bind="bidiText">Komorbid</span>
# fe-expandable-list-content
# //*[@id="anchorName"]/div/div/ng-include/div/div[1]/a/div/span
# //*[@id="anchorName"]/div/div/ng-include/div/div[1]/a/div
# //*[@id="anchorName"]/div/div/ng-include/div/div[1]


# tables = driver.find_elements_by_class_name("fe-expandable-list-content")
tables = driver.find_elements(By.CLASS_NAME, "fe-expandable-list-content")

for table in tables:
    keywords1 = table.find_elements(
        By.XPATH, '//*[@id="anchorName"]/div/div/ng-include/div/div[1]'
    )
    keywords2 = table.find_elements(
        By.XPATH, '//*[@id="anchorName"]/div/div/ng-include/div/div[2]'
    )
    keywords3 = table.find_elements(
        By.XPATH, '//*[@id="anchorName"]/div/div/ng-include/div/div[3]'
    )

for keyword1 in keywords1:
    print(keyword1.text)

for keyword2 in keywords2:
    print(keyword2.text)
