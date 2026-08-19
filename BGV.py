import time
import zipfile
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

input_zip = r"D:\Employee Documents.zip"
output_zip = r"D:\missing_documents.zip"

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://botsdna.com/BGV/")
    driver.maximize_window()

except Exception as e:
    print(f"Error starting browser or loading page: {e}")
    exit()

time.sleep(5)

count=0
with zipfile.ZipFile(input_zip, "r") as zip_file:
    files = zip_file.namelist()
    while True:
        emp_id = driver.find_element(By.XPATH, "//input[@id='CurrentEmpID']").get_attribute("value").strip()
        missing_docs = driver.find_element(By.XPATH, "//textarea[@id='MissingDocs']").get_attribute("value").strip()
        print("Employee id:", emp_id)
        print("Missing documents:", missing_docs)

        added_files = set()
        for folder in files:
            if not folder.endswith("/"):
                continue

            folder_name = folder.strip("/").split("/")[-1]
            if folder_name != emp_id:
                continue

            documents = missing_docs.split("/")

            for document in documents:
                document = document.strip()

                if not document:
                    continue

                ignore_words = {"MARKLIST", "MARK", "LIST", "CERTIFICATE", "DOCUMENT", "DOC", "COPY"}

                words = re.findall(r"[A-Z0-9]+", document.upper())

                search_words = [
                    word for word in words
                    if word not in ignore_words
                ]

                if not search_words:
                    continue

                search_text = "".join(search_words)

                for file_name in files:
                    if not file_name.startswith(folder):
                        continue

                    if file_name.endswith("/"):
                        continue

                    file_only = file_name.split("/")[-1]
                    file_without_ext = os.path.splitext(file_only)[0]   # to remove extension

                    clean_file = re.sub(r"[^A-Z0-9]", "", file_without_ext.upper())

                    if search_text in clean_file:
                        added_files.add(file_name)
                        break

            break

        if added_files:
            with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as new_zip:  # to compress files
                written_names = set()

                for file_name in added_files:
                    file_only = file_name.split("/")[-1]

                    if file_only in written_names:
                        continue

                    file_data = zip_file.read(file_name)
                    new_zip.writestr(file_only, file_data)
                    written_names.add(file_only)

            driver.find_element(By.XPATH, "//input[@id='uploadedFile']").send_keys(output_zip)
            time.sleep(3)
            button = driver.find_element(By.XPATH, "//input[@value='Submit']")
            button.click()
            count+=1

            if count==10:
                print("10 employees processed. Closing browser...")
                time.sleep(3)
                break
            
time.sleep(2)

try:
    driver.quit()
    print("Browser closed successfully.")

except Exception as e:
    print(f"Error closing browser: {e}")