from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_project_details():
    url = "https://rera.odisha.gov.in/projects/project-list"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    driver.get(url)
    print(f"Opening {url} ...")

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "project-card")))
    results = []

    for i in range(6):
        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "project-card")))
            project_cards = driver.find_elements(By.CLASS_NAME, "project-card")

            print(f"\nProcessing project {i + 1}...")

            view_btn = project_cards[i].find_element(By.LINK_TEXT, "View Details")
            driver.execute_script("arguments[0].scrollIntoView(true);", view_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", view_btn)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".project-details")))
            time.sleep(1)

            details = {}
            details['Project Name'] = driver.find_element(By.XPATH, "//label[text()='Project Name']/following-sibling::strong").text.strip()
            details['RERA Regd. No'] = driver.find_element(By.XPATH, "//label[text()='RERA Regd. No.']/following-sibling::strong").text.strip()

            # Switch to Promoter Details tab
            promoter_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Promoter Details')]")))
            driver.execute_script("arguments[0].click();", promoter_tab)
            time.sleep(1)

            # Try various possible labels for Promoter Name
            promoter_name = "N/A"
            for label in ["Company Name", "Promoter Name", "Individual Name"]:
                try:
                    promoter_name = driver.find_element(By.XPATH, f"//label[text()='{label}']/following-sibling::strong").text.strip()
                    break
                except:
                    continue

            details['Promoter Name'] = promoter_name

            # Address of promoter
            try:
                details['Address of the Promoter'] = driver.find_element(By.XPATH, "//label[text()='Registered Office Address']/following-sibling::strong").text.strip()
            except:
                details['Address of the Promoter'] = "N/A"

            # GST
            try:
                details['GST No.'] = driver.find_element(By.XPATH, "//label[text()='GST No.']/following-sibling::strong").text.strip()
            except:
                details['GST No.'] = "N/A"

            results.append(details)
            print(f"✔ Scraped: {details['Project Name']}")

            driver.back()
            time.sleep(1)

        except Exception as e:
            print(f"❌ Failed to process project {i + 1}: {e}")
            try:
                driver.back()
                time.sleep(1)
            except:
                pass

    driver.quit()

    # Print results to terminal
    print("\nFinal Results:")
    for i, project in enumerate(results, 1):
        print(f"\nProject {i}:")
        for key, value in project.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    scrape_project_details()
