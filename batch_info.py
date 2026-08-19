import time
from datetime import datetime
import smtplib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

try:
   driver = webdriver.Chrome(options=options)
   driver.get("https://botsdna.com/BatchProcess/")
   driver.maximize_window()

except Exception as e:
   print(f"Error starting browser or loading page: {e}")
   exit()

time.sleep(2)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
sender_email = "laibabaig1000@gmail.com"
receiver_email = "laibabaig1000@gmail.com"
app_password = "pgwl svmg lfyt jbcm"

row_num = 1

while True:
    try:
        data = driver.find_element(By.XPATH, f"//html/body/center/table/tbody/tr[{row_num}]/td").text
        print("Processing row", row_num, ":", data)
        time.sleep(1)

        data = data.replace("[BATCH ", "").replace("]", "")
        parts = data.split(" | ")

        print(parts)

        version = parts[0]
        batch_info = parts[1]

        max_version, min_version = version.split(".")

        if "PORD:" in batch_info:
            date_part, batch_code = batch_info.split("PORD:")
            order_type = "Potassium"
        elif "DORD:" in batch_info:
            date_part, batch_code = batch_info.split("DORD:")
            order_type = "Dubnium"
        else:
            print("Invalid order type:", batch_info)
            row_num += 1
            continue

        print("Max Version:", max_version)
        print("Min Version:", min_version)
        print("Date Part:", date_part)
        print("Batch Code:", batch_code)
        print("Order Type:", order_type)

        time.sleep(1)

        date_value = datetime.strptime(date_part, "%Y%d%m").strftime("%Y-%m-%d")
        print("Date:", date_value)
        time.sleep(1)

        driver.find_element(By.XPATH, "//a[@href='SubmitBatch.html']").click()
        time.sleep(1)

        driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[1]/td[2]/input").send_keys(batch_code)
        time.sleep(1)

        dropdown1 = driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[2]/td[2]/select")
        Select(dropdown1).select_by_visible_text(max_version)
        time.sleep(1)

        dropdown2 = driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[3]/td[2]/select")
        Select(dropdown2).select_by_visible_text(min_version)
        time.sleep(1)

        date_input = driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[4]/td[2]/input")
        driver.execute_script("arguments[0].value = arguments[1];", date_input, date_value)
        time.sleep(1)

        if order_type == "Dubnium":
            driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[5]/td[2]/input[1]").click()
        elif order_type == "Potassium":
            driver.find_element(By.XPATH, "//html/body/center/table/tbody/tr[5]/td[2]/input[2]").click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@value='Submit']").click()
        print("Submitted:", batch_code)
        time.sleep(2)

        transac_no = driver.find_element(By.XPATH, "//html/body/center/h1/p").text.strip()
        print("Transaction Number:", transac_no)
        time.sleep(1)

        subject = "Batch Process Created Successfully"

        body = f"""Hello!

The batch has been created successfully.

Batch Code: {batch_code}
Order Type: {order_type}
Max Version: {max_version}
Min Version: {min_version}
Date: {date_value}
Transaction Number: {transac_no}
"""

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            print("Sending email...")

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            print("Email sent successfully!")

        except Exception as e:
            print("Error sending email:", e)

        time.sleep(2)

        driver.get("https://botsdna.com/BatchProcess/")
        print("Back to Batch Process")
        time.sleep(2)

        row_num += 1

        print("Moving to next row...")
        print()

        time.sleep(2)

    except Exception as e:
        print("No more rows./Error:",e)
        break


time.sleep(2)
try:
   driver.quit()
   print("Browser closed successfully.")

except Exception as e:
   print(f"Error closing browser: {e}")

