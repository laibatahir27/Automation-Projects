import time
import zipfile
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException


input_zip = r"D:\TodaysPrice.zip"

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def handle_alert():
    try:
        alert = driver.switch_to.alert
        print("Alert:", alert.text)
        alert.accept()
        time.sleep(1)

    except NoAlertPresentException:
        pass

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://botsdna.com/VegetableBasket/")
    driver.maximize_window()

except Exception as e:
    print(f"Error starting browser or loading page: {e}")
    exit()

time.sleep(3)

with zipfile.ZipFile(input_zip, "r") as zip_file:
    files = zip_file.namelist()
    print("All files are:")
    for filename in files:
        print(filename)
        if not filename.startswith("TodaysPrice/"):
            continue

        if filename.endswith("/"):
            continue


        file_only = filename.split("/")[-1]
        print("File with extension:", file_only)

        json_text = zip_file.read(filename).decode("utf-8")
        data = json.loads(json_text)

                                     # First item
        first_item = data["Vegitables"][0]
        print("First item:", first_item)
        code1 = first_item["Code"]
        price1 = first_item["Price"].replace("/-", "")
        tb_id1 = "tbl" + code1
        print(f"Code: {code1}, Price: {price1}, Table_id: {tb_id1}")
        print("----------------------")
        driver.find_element(By.XPATH,"//input[@id='vegCode']").clear()
        driver.find_element(By.XPATH,"//input[@id='vegCode']").send_keys(code1)
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@id='Search']").click()
        time.sleep(2)
        val1 = driver.find_element(By.XPATH,f"//table[@id='{tb_id1}']/tbody/tr[3]/td[2]/input").get_attribute("value")
        print("Website Price:", val1)
        print("JSON Price:", price1)

        if val1 == price1:
            print("Price is same. Moving to next code.")

        else:
            print("Price is different. Updating price.")
            price_input1 = driver.find_element(By.XPATH,f"//table[@id='{tb_id1}']/tbody/tr[3]/td[2]/input")
            price_input1.clear()
            price_input1.send_keys(price1)
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@id='updateVeg']").click()
            time.sleep(2)
            handle_alert()
            print("Price updated successfully.")

        print("----------------------")

                                               # Second Item
        second_item = data["Vegitables"][1]
        print("Second item:", second_item)
        code2 = second_item["Code"]
        price2 = second_item["Price"].replace("/-", "")
        tb_id2 = "tbl" + code2
        print(f"Code: {code2}, Price: {price2}, Table_id: {tb_id2}")
        print("----------------------")
        driver.find_element(By.XPATH,"//input[@id='vegCode']").clear()
        driver.find_element(By.XPATH,"//input[@id='vegCode']").send_keys(code2)
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@id='Search']").click()
        time.sleep(2)
        val2 = driver.find_element(By.XPATH,f"//table[@id='{tb_id2}']/tbody/tr[3]/td[2]/input").get_attribute("value")
        print("Website Price:", val2)
        print("JSON Price:", price2)

        if val2 == price2:
            print("Price is same. Moving to next code.")

        else:
            print("Price is different. Updating price.")
            price_input2 = driver.find_element(By.XPATH,f"//table[@id='{tb_id2}']/tbody/tr[3]/td[2]/input")
            price_input2.clear()
            price_input2.send_keys(price2)
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@id='updateVeg']").click()
            time.sleep(2)
            handle_alert()
            print("Price updated successfully.")

        print("----------------------")

                                            # Third Item
        third_item = data["Vegitables"][2]
        print("Third item:", third_item)
        code3 = third_item["Code"]
        price3 = third_item["Price"].replace("/-", "")
        tb_id3 = "tbl" + code3
        print(f"Code: {code3}, Price: {price3}, Table_id: {tb_id3}")
        print("----------------------")
        driver.find_element(By.XPATH,"//input[@id='vegCode']").clear()
        driver.find_element(By.XPATH,"//input[@id='vegCode']").send_keys(code3)
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@id='Search']").click()
        time.sleep(2)
        val3 = driver.find_element(By.XPATH,f"//table[@id='{tb_id3}']/tbody/tr[3]/td[2]/input").get_attribute("value")
        print("Website Price:", val3)
        print("JSON Price:", price3)
        if val3 == price3:
            print("Price is same. Moving to next JSON file.")

        else:
            print("Price is different. Updating price.")
            price_input3 = driver.find_element(By.XPATH,f"//table[@id='{tb_id3}']/tbody/tr[3]/td[2]/input")
            price_input3.clear()
            price_input3.send_keys(price3)
            time.sleep(2)
            driver.find_element(By.XPATH,"//input[@id='updateVeg']").click()
            time.sleep(2)
            handle_alert()
            print("Price updated successfully.")


        print("==============================")


time.sleep(3)
try:
    driver.quit()

    print("Browser closed successfully.")

except Exception as e:
    print(f"Error closing browser: {e}")