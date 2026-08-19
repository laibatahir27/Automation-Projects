import time
import zipfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from reportlab.pdfgen import canvas

input_zip = r"D:\Required Files.zip"
output_folder = r"D:\Sample Output"

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

try:
   driver = webdriver.Chrome(options=options)
   driver.get("https://botsdna.com/poc/")
   driver.maximize_window()

except Exception as e:
   print(f"Error starting browser or loading page: {e}")
   exit()

time.sleep(5)

os.makedirs(output_folder, exist_ok=True)

with zipfile.ZipFile(input_zip, "r") as zip_file:

    files = zip_file.namelist()
    print("All files are:")
    for filename in files:
        print(filename)
    row_num = 2

    while True:
        try:
            project_code = driver.find_element(By.XPATH,f"//html/body/center/center/table/tbody/tr[{row_num}]/td[1]").text.strip()
            developer_phone = driver.find_element(By.XPATH,f"//html/body/center/center/table/tbody/tr[{row_num}]/td[2]").text.strip()
            manager_phone = driver.find_element(By.XPATH,f"//html/body/center/center/table/tbody/tr[{row_num}]/td[3]").text.strip()
            print("\nProject Code:", project_code)

            if developer_phone and manager_phone:
                contact_type = "Both"
            elif developer_phone:
                contact_type = "Developer"
            elif manager_phone:
                contact_type = "Manager"
            else:
                contact_type = ""

            if contact_type:
                dropdown = driver.find_element(By.XPATH,f"//html/body/center/center/table/tbody/tr[{row_num}]/td[4]/select")

                Select(dropdown).select_by_visible_text(contact_type)

                print("Point Of Contact:", contact_type)

            found_file = None

            for file_name in files:

                if not file_name.startswith("Required Files/Project Description/"):
                    continue

                if file_name.endswith("/"):
                    continue

                file_only = file_name.split("/")[-1]
                print("File with extension:",file_only)
                file_without_ext = os.path.splitext(file_only)[0]

                if project_code == file_without_ext:

                    found_file = file_name

                    print("Matched File:", file_only)

                    break

            if found_file:

                file_data = zip_file.read(found_file)
                description = file_data.decode("utf-8").strip()

                print("Project Description:")
                print(description)

                pdf_path = os.path.join(output_folder,project_code + ".pdf")

                pdf = canvas.Canvas(pdf_path)  # create pdf

                pdf.setFont("Helvetica", 12)

                pdf.drawString(50,800,"Project Code: " + project_code)
                pdf.drawString(50,750,"Manger Contact: " + manager_phone)
                pdf.drawString(50,700,"Developer Contact: " + developer_phone)
                pdf.drawString(50,650,"Project Description:")

                y = 620
                words = description.split()
                line = ""

                for word in words:

                    if len(line) + len(word) > 90:

                        pdf.drawString(50,y,line)

                        y -= 20
                        line = ""

                    if y < 50:

                        pdf.showPage()

                        pdf.setFont("Helvetica",12)

                        y = 800

                    line = line + word + " "

                if line:

                    pdf.drawString(50,y,line)

                pdf.save()

                print("PDF Created:",project_code + ".pdf")

            else:

                print("No matching file found.")

            row_num += 1

        except:
            break

driver.find_element(By.XPATH,'//input[@id="poc"]').click()

time.sleep(5)
try:
   driver.quit()
   print("Browser closed successfully.")

except Exception as e:
   print(f"Error closing browser: {e}")

print("\nAll PDFs created and submitted successfully!")