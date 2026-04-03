import time
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def clean_posted_ago(value: str) -> str:

    if not value:
        return ""
    if value.strip().lower() == "yesterday":
        return "1 days ago"
    return value.strip()


def clean_employee_count(value: str):
    if not value:
        return ""
    match = re.search(r"[\d,]+", value)
    if match:
        return int(match.group().replace(",", ""))
    return ""


def find_text(card, selectors: list, default="") -> str:
    for sel in selectors:
        try:
            el = card.find_element(By.CSS_SELECTOR, sel)
            text = el.text.strip()
            if text:
                return text
        except Exception:
            pass
    return default


def find_attr(card, selectors: list, attr: str, default="") -> str:
    for sel in selectors:
        try:
            el = card.find_element(By.CSS_SELECTOR, sel)
            val = el.get_attribute(attr)
            if val:
                return val.strip()
        except Exception:
            pass
    return default


def close_popup(driver, wait):
    popup_selectors = [
        "button[aria-label='Close']",
        "[data-testid='modal-close']",
        "button.close",
        "button[class*='close']",
        "button[class*='dismiss']",
    ]
    for sel in popup_selectors:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
            btn.click()
            print("  Popup closed.")
            time.sleep(1.5)
            return
        except Exception:
            pass
    try:
        btn = driver.find_element(
            By.XPATH,
            "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),'close')"
            " or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),'stay')]"
        )
        btn.click()
        print("  Popup closed (XPath fallback).")
        time.sleep(1.5)
    except Exception:
        print("  No popup found — continuing.")

def perform_search(driver, wait):

    nav_search_selectors = [
        "button[data-testid='search-button']",
        "[data-testid='search-bar']",
        "button[aria-label*='search' i]",
        "button[aria-label*='Search' i]",
        ".sc-search-bar",
        "nav button",   
    ]
    for sel in nav_search_selectors:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
            btn.click()
            print(f"  Clicked search trigger: {sel}")
            time.sleep(1)
            break
        except Exception:
            pass

    input_selectors = [
        "input[data-testid='search-input']",
        "input[name='query']",
        "input[placeholder*='Search' i]",
        "input[placeholder*='job' i]",
        "input[type='search']",
        "input[type='text']",
    ]

    search_input = None
    for sel in input_selectors:
        try:
            el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
            if el.get_attribute("readonly") is None and el.is_enabled():
                search_input = el
                print(f"  Found input: {sel}")
                break
        except Exception:
            pass

    if search_input is None:
        print("  Input not found via selectors — using direct URL navigation.")
        driver.get(
            "https://www.welcometothejungle.com/en/jobs"
            "?refinementList%5Boffices.country_code%5D%5B%5D=US"
            "&query=Business"
        )
        time.sleep(4)
        return False   

    actions = ActionChains(driver)
    actions.move_to_element(search_input).click().perform()
    time.sleep(0.5)

    driver.execute_script("arguments[0].value = '';", search_input)
    search_input.send_keys("Business")
    search_input.send_keys(Keys.ENTER)
    print("  Typed 'Business' and pressed Enter.")
    return True

def scrape_card(card) -> dict:

    lines = card.text.split("\n")

    job_title = find_text(card, [
        "h3", "h2",
        "[data-testid='job-title']",
        "a > div > span",
    ])

    company_title = find_text(card, [
        "[data-testid='company-title']",
        "span[class*='company']",
        "p[class*='company']",
        "a[class*='company']",
    ])

    company_slogan = find_text(card, [
        "[data-testid='company-slogan']",
        "span[class*='slogan']",
        "p[class*='description']",
    ])
    if not company_slogan:
        for line in lines:
            if line and line != job_title and line != company_title and len(line) > 15:
                company_slogan = line
                break

    job_type = find_text(card, [
        "[data-testid='job-contract-type']",
        "span[class*='contract']",
        "li[class*='contract']",
    ])
    if not job_type:
        for line in lines:
            if any(k in line for k in ["contract", "Contract", "Freelance",
                                        "Internship", "Part-time", "Full-time",
                                        "Temporary", "Apprenticeship"]):
                job_type = line.strip()
                break

    location = find_text(card, [
        "[data-testid='job-location']",
        "span[class*='location']",
        "li[class*='location']",
        "address",
    ])

    work_location = find_text(card, [
        "[data-testid='remote-label']",
        "span[class*='remote']",
        "li[class*='remote']",
    ])
    if not work_location:
        keywords = ["remote", "hybrid", "on-site", "no remote",
                    "full remote", "partial remote", "temporarily remote"]
        for line in lines:
            if any(k in line.lower() for k in keywords):
                work_location = line.strip()
                break

    industry = find_text(card, [
        "[data-testid='job-sector']",
        "span[class*='sector']",
        "li[class*='sector']",
        "span[class*='industry']",
    ])

    employee_raw = find_text(card, [
        "[data-testid='company-size']",
        "span[class*='employee']",
        "li[class*='employee']",
        "span[class*='size']",
    ])
    if not employee_raw:
        for line in lines:
            if "employee" in line.lower():
                employee_raw = line.strip()
                break

    posted_raw = find_text(card, [
        "[data-testid='job-posted-at']",
        "time",
        "span[class*='date']",
        "li[class*='date']",
        "span[class*='ago']",
    ])
    if not posted_raw:
        for line in reversed(lines):
            if any(k in line.lower() for k in ["ago", "yesterday", "hour", "day", "week", "month"]):
                posted_raw = line.strip()
                break

    job_link = find_attr(card, ["a"], "href")

    return {
        "Job_Title":      job_title,
        "Company_Title":  company_title,
        "Company_Slogan": company_slogan,
        "Job_Type":       job_type,
        "Location":       location,
        "Work_Location":  work_location,
        "Industry":       industry,
        "Employes_Count": clean_employee_count(employee_raw),
        "Posted_Ago":     clean_posted_ago(posted_raw),
        "Job_Link":       job_link,
    }


def scrape_jobs():
    print("=" * 60)
    print("  Welcome to the Jungle — Business Jobs Scraper")
    print("=" * 60)

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    all_jobs = []

    try:
        print("\n[Step 1] Navigating to Welcome to the Jungle (US jobs)...")
        url = (
            "https://www.welcometothejungle.com/en/jobs"
            "?refinementList%5Boffices.country_code%5D%5B%5D=US"
        )
        driver.get(url)
        time.sleep(3)
        close_popup(driver, wait)

        print("\n[Step 2-3] Searching for 'Business'...")
        perform_search(driver, wait)

        print("\n[Step 4] Waiting for results to load...")
        time.sleep(4)

        print("\n[Step 5] Scraping all pages...")

        card_selectors = [
            "[data-testid='search-results-list-item-wrapper']",
            "li[data-testid*='job']",
            "li[class*='sc-']",
            "article[class*='job']",
        ]

        page_num = 1
        while True:
            print(f"\n  -> Page {page_num}")
            time.sleep(2)

            cards = []
            for sel in card_selectors:
                cards = driver.find_elements(By.CSS_SELECTOR, sel)
                if cards:
                    break

            print(f"     {len(cards)} cards found.")

            for card in cards:
                try:
                    job_data = scrape_card(card)
                    all_jobs.append(job_data)
                except Exception as e:
                    print(f"     Warning — skipped card: {e}")

            try:
                next_btn = driver.find_element(
                    By.CSS_SELECTOR,
                    "a[data-testid='pagination-next'], "
                    "button[aria-label='Next page'], "
                    "a[aria-label='Next'], "
                    "a[rel='next']"
                )
                if next_btn.is_displayed() and next_btn.is_enabled():
                    driver.execute_script("arguments[0].click();", next_btn)
                    page_num += 1
                    time.sleep(3)
                else:
                    print("\n  Last page reached.")
                    break
            except Exception:
                print("\n  No more pages.")
                break

    finally:
        driver.quit()

    output_file = "wttj_business_jobs.csv"
    fieldnames = [
        "Job_Title", "Company_Title", "Company_Slogan",
        "Job_Type", "Location", "Work_Location",
        "Industry", "Employes_Count", "Posted_Ago", "Job_Link"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"\nCSV saved -> '{output_file}'  ({len(all_jobs)} records total)")

    print("\n" + "=" * 60)
    print("  ANALYSIS RESULTS")
    print("=" * 60)

    total_jobs = len(all_jobs)
    print(f"(a) Total jobs scraped                   : {total_jobs}")

    ny_count = sum(
        1 for j in all_jobs
        if "new york" in j["Location"].lower()
        or "new york" in j["Work_Location"].lower()
    )
    print(f"(b) Jobs in New York                     : {ny_count}")

    more_200 = sum(
        1 for j in all_jobs
        if isinstance(j["Employes_Count"], int) and j["Employes_Count"] > 200
    )
    print(f"(c) Companies with > 200 employees       : {more_200}")

    less_200 = sum(
        1 for j in all_jobs
        if isinstance(j["Employes_Count"], int) and j["Employes_Count"] < 200
    )
    print(f"(d) Companies with < 200 employees       : {less_200}")

    permanent_count = sum(
        1 for j in all_jobs
        if "permanent contract" in j["Job_Type"].lower()
    )
    print(f"(e) Permanent Contract jobs              : {permanent_count}")

    internship_count = sum(
        1 for j in all_jobs
        if "internship" in j["Job_Type"].lower()
    )
    print(f"(f) Internship jobs                      : {internship_count}")

    print("=" * 60)


if __name__ == "__main__":
    scrape_jobs()