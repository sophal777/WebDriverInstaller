import sys
import threading
import time
import random
import re
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
    QSpinBox, QPushButton, QComboBox, QTableWidget, QLabel, QTableWidgetItem
)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from import_code.WebDriverInstaller import WebDriverInstaller

# Setup WebDrivers
chrome_installer = WebDriverInstaller(browser="chrome")
chrome_path = chrome_installer.download_and_extract_driver()

edge_installer = WebDriverInstaller(browser="edge")
edge_path = edge_installer.download_and_extract_driver()


class AppGui(QWidget):
    def __init__(self):
        super().__init__()
        self.stop_flag = threading.Event()
        self.success_count = 0
        self.lock = threading.Lock()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Facebook Account Creator")
        self.setGeometry(100, 100, 600, 500)

        # Labels
        self.label1 = QLabel('Label 1:')
        self.label2 = QLabel('Label 2:')
        self.label3 = QLabel('Label 3:')

        # Spinboxes
        self.spinbox1 = QSpinBox()
        self.spinbox2 = QSpinBox()
        self.spinbox3 = QSpinBox()

        # Save section
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_data)
        self.file_format_combo = QComboBox()
        self.file_format_combo.addItems(["txt", "xlsx"])

        # Additional Buttons
        self.button1_row3 = QPushButton('Button 3')
        self.button2_row4 = QPushButton('Button 4')
        self.button1_row5 = QPushButton('Button 5')
        self.button2_row6 = QPushButton('Button 6')

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "DOB", "Gender", "Phone", "Password", "Email"])

        # Spin controls
        self.loop_count_spin = QSpinBox()
        self.loop_count_spin.setMinimum(1)
        self.loop_count_spin.setValue(5)
        self.loop_count_spin.setPrefix("🔁 Loops: ")

        self.verify_open_spin = QSpinBox()
        self.verify_open_spin.setMinimum(1)
        self.verify_open_spin.setValue(3)
        self.verify_open_spin.setPrefix("✔️ Verify at: ")

        self.thread_count_spin = QSpinBox()
        self.thread_count_spin.setMinimum(1)
        self.thread_count_spin.setValue(3)
        self.thread_count_spin.setPrefix("🧵 Threads: ")

        # Start / Stop Buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_run)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_run)
        self.ip_button = QPushButton("IP Address")

        # Dropdowns
        self.fb_action_select = QComboBox()
        self.fb_action_select.addItems(["Create_Account", "Login_Account", "Login_Account_Verify", "Create_Account_Verify"])
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["chrome", "edge"])

        self.apply_styles()
        self.setup_layout()

    def apply_styles(self):
        style = """
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-size: 12pt;
                font-family: Arial;
            }
            QPushButton {
                background-color: #0078D7;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
            QComboBox, QSpinBox {
                background-color: #333;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QTableWidget {
                background-color: #2e2e2e;
                color: gold;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #2f4f4f;
                color: gold;
            }
        """
        self.setStyleSheet(style)

    def setup_layout(self):
        layout = QVBoxLayout()

        row_labels = QHBoxLayout()
        row_labels.addWidget(self.label1)
        row_labels.addWidget(self.label2)
        row_labels.addWidget(self.label3)

        row_spinboxes = QHBoxLayout()
        row_spinboxes.addWidget(self.spinbox1)
        row_spinboxes.addWidget(self.spinbox2)
        row_spinboxes.addWidget(self.spinbox3)

        save_row = QHBoxLayout()
        save_row.addWidget(self.save_button)
        save_row.addWidget(self.file_format_combo)

        extra_buttons_row = QHBoxLayout()
        extra_buttons_row.addWidget(self.button1_row3)
        extra_buttons_row.addWidget(self.button2_row4)
        extra_buttons_row.addWidget(self.button1_row5)
        extra_buttons_row.addWidget(self.button2_row6)

        selection_row = QHBoxLayout()
        selection_row.addWidget(self.fb_action_select)
        selection_row.addWidget(self.browser_combo)

        spin_row = QHBoxLayout()
        spin_row.addWidget(self.loop_count_spin)
        spin_row.addWidget(self.verify_open_spin)
        spin_row.addWidget(self.thread_count_spin)

        control_buttons_row = QHBoxLayout()
        control_buttons_row.addWidget(self.start_button)
        control_buttons_row.addWidget(self.stop_button)
        control_buttons_row.addWidget(self.ip_button)

        layout.addLayout(row_labels)
        layout.addLayout(row_spinboxes)
        layout.addWidget(self.table)
        layout.addLayout(save_row)
        layout.addLayout(extra_buttons_row)
        layout.addLayout(selection_row)
        layout.addLayout(spin_row)
        layout.addLayout(control_buttons_row)

        self.setLayout(layout)

    def fb(self, N, browser_choice, app_all):
        self.table.insertRow(N)
        x, y = (N * 235, 2) if N <= 8 else (N * 235 - 1175, 430)

        options = ChromeOptions() if browser_choice == "chrome" else EdgeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument("--lang=en")
        options.add_argument('--no-sandbox')
        options.add_argument("--enable-unsafe-swiftshader")
        options.add_argument(f'--app=https://m.facebook.com/reg')
        options.add_argument('window-size=300,450')
        options.add_argument(f'--window-position={x},{y}')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Linux; Android 8.1.0; SM-G960F) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/72.0.3626.121 Mobile Safari/537.36'
        )
        try:
            if self.stop_flag.is_set():
                print(f"[Thread {N}] Stop flag detected.")
                return

            if browser_choice == "chrome":
                service = ChromeService(executable_path=chrome_path)
                driver = webdriver.Chrome(service=service, options=options)
            elif browser_choice == "edge":
                service = EdgeService(executable_path=edge_path)
                driver = webdriver.Edge(service=service, options=options)
            else:
                print("[!] Invalid browser selected.")
                return
            
#        self.fb_action_select.addItems(["Create_Account", "Login_Account", "Login_Account_Verify", "Create_Account_Verify"])



            if app_all == "Create_Account":
                pass
                time.sleep(3)
                file_path ="rop\\NameRead\\name.txt"
                with open(file_path, 'r', encoding='UTF-8') as file:
                    names = file.readlines()
                    name_read = names[N]
                    firstname, lastname = name_read.split('|')

                driver.find_element(By.XPATH,'//*[@aria-label="Get started"]').click()
                time.sleep(3)    

                firstname_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='First name']"))
                )
                for char in firstname:
                    firstname_field.send_keys(char)
                    time.sleep(0.2)




                lastname_field = driver.find_element(By.XPATH, "//input[@aria-label='Last name']")

                for char in lastname:
                    lastname_field.send_keys(char)
                    time.sleep(0.2)

                item = QTableWidgetItem(firstname + " " + lastname)
                self.table.setItem(N, 0, item)
                self.table.update()


                time.sleep(3)

                with open(file_path, 'r+', encoding='UTF-8') as f:
                    lines = f.readlines()  # Read all lines
                    f.seek(0)  # Move to the beginning of the file
                    f.truncate()  # Clear the file contents
                    f.writelines(lines[1:])  # Write back all lines except the first
                time.sleep(3)   
                File_birthday = "rop\\NameRead\\birthday.txt"
                with open(File_birthday, 'r', encoding='UTF-8') as file:
                    names = file.readlines()
                    name_read = names[N]
                    birthday = name_read.split('|')[0]
                birthday_input = driver.find_element(By.XPATH, "//input[@aria-label='Birthday (0 year old)']")
                for char in birthday:
                    birthday_input.send_keys(birthday)
                    time.sleep(0.3)
                driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()

                time.sleep(2)

                with open(File_birthday, 'r+', encoding='UTF-8') as f:
                    lines = f.readlines()  # Read all lines
                    f.seek(0)  # Move to the beginning of the file
                    f.truncate()  # Clear the file contents
                    f.writelines(lines[1:])  # Write back all lines except the first
                time.sleep(2)

                item = QTableWidgetItem(birthday)
                self.table.setItem(N, 1, item)
                self.table.update()


                selected_gender = "Female_Male"

                # ប្រសិនបើមិនមានការជ្រើសរើសតម្លៃ (បើវាជា "Female_Male") ទៅលើការជ្រើសរើសចៃដន្យ
                if selected_gender == "Female_Male":
                    selected_gender = random.choice(["Female", "Male"])  # ជ្រើសរើសចៃដន្យស្រី ឬ ប្រុស

                # កំណត់ XPath ទៅតាមការជ្រើសរើស
                xpath = f"//*[contains(text(), '{selected_gender}')]"

                # រកឃើញធាតុដែលត្រូវចុច
                gender_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )

                # ចុចលើធាតុដែលបានជ្រើស
                gender_element.click()

                # បោះពុម្ពលទ្ធផល
                time.sleep(3)



                item = QTableWidgetItem(selected_gender)
                self.table.setItem(N, 2, item)
                self.table.update()
                time.sleep(3)

                driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()
                time.sleep(3)
                phone_yandex_gmail_folder = "rop\\NameRead\\phone.txt"
                with open(phone_yandex_gmail_folder, 'r', encoding='UTF-8') as file:
                    names = file.readlines()
                    name_read = names[N]
                    final_phone = name_read.split('|')[0]
                    time.sleep(1)
                time.sleep(3)

                driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()
                time.sleep(3)

                phone_field = driver.find_element(By.XPATH, "//input[@aria-label='Mobile number']")
                for digit in final_phone:
                    phone_field.send_keys(digit)
                    time.sleep(0.3)  # Simulate typing
                time.sleep(3)
                driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()

                item = QTableWidgetItem(final_phone)
                self.table.setItem(N, 3, item)
                self.table.update()
                try:
                    time.sleep(3)

                    continue_xpath = "//*[contains(text(), 'Continue creating account')]"
                    continue_element = driver.find_element(By.XPATH, continue_xpath)
                    continue_element.click()
                    time.sleep(2)

                except:
                    pass
                driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]").click()
                password_ ="rop\\NameRead\\Password.txt"
                with open(password_, 'r', encoding='UTF-8') as file:
                    names = file.readlines()
                    name_read = names[N]
                    password_op = name_read.split('|')[0]

                password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
                for digit in password_op:
                    password_input.send_keys(digit)
                    time.sleep(0.3)




                item = QTableWidgetItem(password_op)
                self.table.setItem(N, 4, item)
                self.table.update()
                time.sleep(3)
                with open(phone_yandex_gmail_folder, 'r+', encoding='UTF-8') as f:
                    lines = f.readlines()  # Read all lines
                    f.seek(0)  # Move to the beginning of the file
                    f.truncate()  # Clear the file contents
                    f.writelines(lines[1:])  # Write back all lines except the first

                time.sleep(3)





                driver.quit()

        except Exception as e:
            print(f"[ERROR][Thread-{N}] {e}")

        print(f"[Thread-{N}] Running fb() with Browser: {browser_choice}, App: {app_all}")
        time.sleep(4)

    def every_loop(self):
        print("[every_loop] Verifying accounts after N loops.")

    def start_run(self):
        self.stop_flag.clear()
        threading.Thread(target=self.run).start()

    def stop_run(self):
        self.stop_flag.set()
        print("[STOP] User requested to stop the process.")

    def run(self):
        browser_choice = self.browser_combo.currentText().lower()
        app_all = self.fb_action_select.currentText()
        thread_count = self.thread_count_spin.value()
        loop_count = self.loop_count_spin.value()
        verify_open = self.verify_open_spin.value()

        loops = 0
        while loops < loop_count and not self.stop_flag.is_set():
            loops += 1
            print(f"Starting loop {loops}/{loop_count}")

            threads = []
            for N in range(thread_count):
                if self.stop_flag.is_set():
                    break
                t = threading.Thread(target=self.fb, args=(N, browser_choice, app_all))
                t.start()
                threads.append(t)
                time.sleep(1)

            for t in threads:
                t.join()

            with self.lock:
                self.success_count += 1
                if self.success_count == verify_open:
                    self.every_loop()
                    self.success_count = 0

            print("Waiting before next loop...")
            time.sleep(5)

    def save_data(self):
        format_selected = self.file_format_combo.currentText()
        if format_selected == "txt":
            self.save_as_txt()
        else:
            self.save_as_xlsx()

    def save_as_txt(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as TXT", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w') as f:
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    f.write("\t".join(row_data) + "\n")
            print(f"Data saved as TXT: {file_path}")

    def save_as_xlsx(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as XLSX", "", "Excel Files (*.xlsx)")
        if file_path:
            data = []
            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            df = pd.DataFrame(data, columns=["Name", "DOB", "Gender", "Phone", "Password", "Email"])
            df.to_excel(file_path, index=False)
            print(f"Data saved as XLSX: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppGui()
    window.show()
    sys.exit(app.exec())
