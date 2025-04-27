import os
import zipfile
import requests
import shutil
import subprocess

class WebDriverInstaller:
    def __init__(self, browser="chrome", folder="webdriver"):
        self.browser = browser.lower()
        self.folder = folder
        self.driver_path = os.path.join(self.folder, f"{self.browser}driver.exe")

    def get_browser_version(self):
        if self.browser == "chrome":
            return self.get_chrome_version()
        elif self.browser == "edge":
            return self.get_edge_version()
        else:
            print(f"[!] Unsupported browser: {self.browser}")
            return None

    def get_chrome_version(self):
        try:
            result = subprocess.run(
                ['reg', 'query', r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True
            )
            if result.returncode != 0 or "version" not in result.stdout.lower():
                raise Exception("Chrome not found in registry")
            version_line = result.stdout.strip().split('\n')[-1]
            version = version_line.split()[-1]
            return version
        except Exception as e:
            print(f"[!] Chrome not found or error reading version: {e}")
            return None

    def get_edge_version(self):
        try:
            result = subprocess.run(
                ['reg', 'query', r'HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True
            )
            if result.returncode != 0 or "version" not in result.stdout.lower():
                raise Exception("Edge not found in registry")
            version_line = result.stdout.strip().split('\n')[-1]
            version = version_line.split()[-1]
            return version
        except Exception as e:
            print(f"[!] Edge not found or error reading version: {e}")
            return None

    def get_chromedriver_download_url(self, version):
        try:
            version_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
            json_data = requests.get(version_url).json()
            full_version = json_data['channels']['Stable']['version']
            base_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{full_version}/win32/chromedriver-win32.zip"
            return base_url
        except Exception as e:
            print(f"[!] Failed to fetch ChromeDriver URL: {e}")
            return None

    def get_edgedriver_download_url(self, version):
        try:
            base_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win32.zip"
            return base_url
        except Exception as e:
            print(f"[!] Failed to fetch EdgeDriver URL: {e}")
            return None

    def download_and_extract_driver(self):
        # Check if driver already exists
        if os.path.exists(self.driver_path):
            print(f"[✓] {self.browser.capitalize()}Driver មានរួចហើយ៖ {self.driver_path}")
            return self.driver_path

        print(f"[+] កំពុងពិនិត្យ {self.browser.capitalize()} version...")
        browser_version = self.get_browser_version()
        if not browser_version:
            print(f"[!] {self.browser.capitalize()} មិនត្រូវបានដំឡើងឡើយ។")
            return None

        print(f"[+] រកឃើញ {self.browser.capitalize()} version: {browser_version}")
        if self.browser == "chrome":
            url = self.get_chromedriver_download_url(browser_version)
        elif self.browser == "edge":
            url = self.get_edgedriver_download_url(browser_version)
        else:
            print("[!] Unsupported browser.")
            return None

        if not url:
            print(f"[!] មិនអាចទាញ URL សម្រាប់ {self.browser.capitalize()}Driver បានទេ។")
            return None

        print(f"[+] กำลังดาวน์โหลด {self.browser.capitalize()}Driver ពី: {url}")
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"[!] ទាញ {self.browser.capitalize()}Driver មិនបានទេ។")
            return None

        os.makedirs(self.folder, exist_ok=True)
        zip_path = os.path.join(self.folder, f"{self.browser}driver.zip")

        with open(zip_path, "wb") as file:
            file.write(response.content)

        print(f"[+] กำลังដាក់បញ្ជូល {self.browser.capitalize()}Driver...")

        if not zipfile.is_zipfile(zip_path):
            print(f"[!] File មិនមែនជា ZIP ត្រឹមត្រូវទេ: {zip_path}")
            return None

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.folder)

        driver_path = None
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if f"{self.browser}driver.exe" in file.lower():
                    driver_path = os.path.join(root, file)
                    break

        if not driver_path:
            print(f"[!] មិនឃើញ {self.browser.capitalize()}Driver.exe បន្ទាប់ពីដាក់បញ្ជូលឡើយ។")
            return None

        shutil.move(driver_path, self.driver_path)
        os.remove(zip_path)

        print(f"[✓] {self.browser.capitalize()}Driver បានត្រៀមរួចរាល់នៅ: {self.driver_path}")
        return self.driver_path



chrome_installer = WebDriverInstaller(browser="chrome")
chrome_path = chrome_installer.download_and_extract_driver()
# Install EdgeDriver
edge_installer = WebDriverInstaller(browser="edge")
edge_path = edge_installer.download_and_extract_driver()

