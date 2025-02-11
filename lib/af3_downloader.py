import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class AF3Downloader:
    def __init__(self, debugger_address="127.0.0.1:9222"):
        self.debugger_address = debugger_address
        options = webdriver.ChromeOptions()
        options.debugger_address = self.debugger_address  # Connect to the existing Chrome instance
        self.driver = webdriver.Chrome(options=options)
    
    def get_download_links(self):
        """
        Finds and returns all download links for structures (zip files) by interacting
        with the 'more_vert' buttons on the page.
        """
        all_hrefs = []
        # Locate all "more_vert" buttons on the page
        buttons = self.driver.find_elements(By.XPATH, '//*[contains(text(), "more_vert")]')
        
        if len(buttons) < 2:
            print("Warning: Fewer buttons than expected. Check if the page is loaded correctly.")
        
        # Skip the first button, then process the remaining buttons
        for index, button in enumerate(buttons[1:]):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
                print(f"Button {index + 1} clicked to open the menu.")
                time.sleep(1)  # Adjust delay as needed

                try:
                    href_elements = self.driver.find_elements(
                        By.XPATH,
                        '//a[contains(@class, "mat-mdc-menu-item") and contains(@href, "fold.zip")]'
                    )
                    for href in href_elements:
                        link = href.get_attribute('href')
                        all_hrefs.append(link)
                        print(f"Found href: {link}")
                except Exception as e:
                    print(f"No hrefs found in menu {index + 1}: {e}")

                try:
                    # Attempt to close the menu by clicking on the overlay
                    overlay = self.driver.find_element(By.CLASS_NAME, 'cdk-overlay-backdrop')
                    overlay.click()
                    print("Overlay clicked to close the menu.")
                except Exception as e:
                    print(f"Overlay not found for menu {index + 1}: {e}")

                time.sleep(1)
            except Exception as e:
                print(f"Error processing button {index + 1}: {e}")
        
        return all_hrefs

    def save_links_csv(self, links, output_file):
        """
        Saves the list of download links to a CSV file.
        """
        if links:
            df = pd.DataFrame(links, columns=["link"])
            df.to_csv(output_file, index=False, header=False)
            print(f"Links saved to {output_file}")
        else:
            print("No links to save.")

    def download_files(self, download_links):
        """
        Iterates over the download links and triggers the download by navigating to each URL.
        """
        def download_file(url):
            try:
                self.driver.get(url)
                print(f"Download initiated for {url}")
                time.sleep(1)  # Wait for the download to begin
            except Exception as e:
                print(f"Failed to download {url}: {e}")

        for link in download_links:
            download_file(link)
            time.sleep(1)  # Pause between downloads

    def close(self):
        """
        Closes the Selenium WebDriver.
        """
        self.driver.quit()
