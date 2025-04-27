from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service as ChromeService

def Reboot _Wi_Fi():
    # Set up Chrome options (headless mode optional)
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Uncomment to run in headless mode


    service = ChromeService('C:\\Users\\Admin_pc\\mm\\webdriver\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)


    try:
        # Navigate to the router login page
        driver.get("http://192.168.100.1/")

        # Wait for the username input and enter credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txt_Username"))
        ).send_keys("telecomadmin")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txt_Password"))
        ).send_keys("admintelecom")

        # Click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button"))
        ).click()

        # Wait for and click the "System Tools > Reboot" option
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li:nth-child(11) > .tabBtnCenter"))
        ).click()

        # Switch to the iframe containing the reboot button
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(0)  # Switch to the first iframe
        )
        time.sleep(100)
        # Wait for the reboot button and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnReboot"))
        ).click()

        # Wait for the confirmation alert and accept it
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Wait for 2 minutes for the router to reboot
        time.sleep(120)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser after execution
        driver.quit()
