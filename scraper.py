import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import config

def setup_driver(download_dir):
    chrome_options = Options()
    if config.HEADLESS:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
    
    # Configure auto-download
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True # Forces download instead of viewer
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Use default Service
    driver = webdriver.Chrome(options=chrome_options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    return driver

def scrape():
    target_year = config.TARGET_YEAR
    if target_year:
        local_filename = f"{target_year}AOF-grains-oilseeds-outlook.pdf"
        local_path = os.path.join(config.PROJECT_INFO_DIR, "Samplepdfs", local_filename)
        if os.path.exists(local_path):
            print(f"Offline Mode: Found local PDF for year {target_year} at {local_path}. Using it.")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            run_download_dir = os.path.join(config.DOWNLOAD_DIR, timestamp)
            os.makedirs(run_download_dir, exist_ok=True)
            import shutil
            dest_path = os.path.join(run_download_dir, local_filename)
            shutil.copy(local_path, dest_path)
            return dest_path, target_year

    # Create timestamped directory for this run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_download_dir = os.path.join(config.DOWNLOAD_DIR, timestamp)
    os.makedirs(run_download_dir, exist_ok=True)

    driver = setup_driver(run_download_dir)
    try:
        print(f"Navigating to {config.BASE_URL}...")
        driver.get(config.BASE_URL)
        wait = WebDriverWait(driver, 20)
        
        target_year = config.TARGET_YEAR
        
        # 1. Detect target year if not specified
        if target_year is None:
            # Look for "2026 Outlook Reports" heading
            headings = driver.find_elements(By.TAG_NAME, "h4")
            for h in headings:
                if "Outlook Reports" in h.text:
                    try:
                        target_year = h.text.split()[0]
                        print(f"Detected latest year: {target_year}")
                        break
                    except:
                        continue
        
        if target_year is None:
            # Fallback to accordion toggler
            try:
                first_year_el = driver.find_element(By.CSS_SELECTOR, "dt.ckeditor-accordion-toggler")
                target_year = first_year_el.text.strip()
                print(f"Fallback: detected latest year from accordion: {target_year}")
            except:
                print("Could not detect year.")
                return None, None

        print(f"Searching for report for year {target_year}...")
        
        target_link = None
        
        # 2. Search in top section
        latest_section_found = False
        headings = driver.find_elements(By.TAG_NAME, "h4")
        for h in headings:
            if str(target_year) in h.text:
                try:
                    # Find container
                    container = h.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'usa-grid-full')]")
                    # Try both "Grains and Oilseeds" and "Grains & Oilseeds"
                    for text in ["Grains and Oilseeds Outlook", "Grains & Oilseeds"]:
                        links = container.find_elements(By.PARTIAL_LINK_TEXT, text)
                        if links:
                            target_link = links[0]
                            print(f"Found link in top section for {target_year}.")
                            latest_section_found = True
                            break
                    if latest_section_found: break
                except:
                    continue
        
        # 3. Search in accordion
        if not latest_section_found:
            accordions = driver.find_elements(By.CSS_SELECTOR, "dl.styled dt")
            for acc in accordions:
                acc_text = acc.text.strip()
                if str(target_year) in acc_text:
                    print(f"Found accordion for {target_year}. Expanding...")
                    # Scroll and click using JS
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", acc)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", acc)
                    print(f"Clicked accordion for {target_year}. Waiting for expansion...")
                    time.sleep(6) # Increased wait for expansion
                    
                    # Target link in following dd
                    content = acc.find_element(By.XPATH, "./following-sibling::dd")
                    all_links = content.find_elements(By.TAG_NAME, "a")
                    print(f"Found {len(all_links)} links in accordion content for {target_year}.")
                    
                    for link in all_links:
                        # Use textContent as .text might be empty during animation
                        text = link.get_attribute("textContent").strip().lower()
                        href = link.get_attribute("href").lower()
                        
                        try:
                            parent_text = link.find_element(By.XPATH, "..").get_attribute("textContent").lower()
                        except:
                            parent_text = ""
                            
                        combined_text = (text + " " + parent_text)
                        print(f"Checking link text: '{text}' | Href: '{href}'")
                        
                        # Match "Grains" and ("Oilseeds" or "Oil seeds" or "grains-oilseeds")
                        if ("grains" in combined_text and ("oilseeds" in combined_text or "oil seeds" in combined_text)) or "grains-oilseeds" in href:
                            target_link = link
                            print(f"MATCH FOUND in accordion: {text}")
                            break
                    if target_link: break
        
        if target_link:
            pdf_url = target_link.get_attribute("href")
            print(f"Triggering download for: {pdf_url}")
            
            # Use JS click to avoid interception by sticky banners/announcements
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_link)
            driver.execute_script("arguments[0].click();", target_link)
            
            # Wait for download
            print("Waiting for download to complete...")
            timeout = 60
            start_time = time.time()
            downloaded_file = None
            
            while time.time() - start_time < timeout:
                files = os.listdir(run_download_dir)
                pdf_files = [f for f in files if f.endswith(".pdf") and not f.endswith(".crdownload")]
                if pdf_files:
                    # Sort by size or modification time to get the newest if multiple
                    pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(run_download_dir, x)), reverse=True)
                    downloaded_file = os.path.join(run_download_dir, pdf_files[0])
                    # Check if size is stable
                    size1 = os.path.getsize(downloaded_file)
                    time.sleep(2)
                    size2 = os.path.getsize(downloaded_file)
                    if size1 == size2 and size1 > 0:
                        break
                time.sleep(2)
            
            if downloaded_file:
                print(f"Download successful: {downloaded_file}")
                return downloaded_file, target_year
            else:
                print("Download timed out.")
                return None, None
        else:
            print(f"Could not find report link for year {target_year}")
            return None, None

    finally:
        driver.quit()

if __name__ == "__main__":
    path, year = scrape()
    if path:
        print(f"Scraper finished. File saved at: {path}")
    else:
        print("Scraper failed.")
