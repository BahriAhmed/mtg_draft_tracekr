from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_cards(base_url: str, expansion: str) -> pd.DataFrame:
    """
    Scrape all BLB cards from a composed URL and return a DataFrame.
    Accepts cookies if the consent popup is present.

    Args:
        base_url: The main URL.
        expansion: Expansion code.
    """
    results = []
    url = f"{base_url}{expansion}"

    # Headless Chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Wait up to 5 seconds for a cookie banner and click accept if present
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Accept')]")
                )
            )
            accept_button.click()
        except:
            print("No cookie popup detected.")

        time.sleep(1)  # Let the page reload after clicking

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Each card is in <div class="card-list-filter">
        for card_div in soup.select(".card-list-filter"):
            name = card_div.select_one("h3")
            ai_rating_tag = card_div.find("b", string=lambda s: s and "AI Rating" in s)
            pro_rating_tag = card_div.find("b", string=lambda s: s and "Pro Rating" in s)
            description = card_div.select_one("p")

            if not all([name, ai_rating_tag, pro_rating_tag, description]):
                continue

            results.append({
                "card_name": name.get_text(strip=True),
                "ai_rating": ai_rating_tag.get_text(strip=True).split(":", 1)[1].strip(),
                "pro_rating": pro_rating_tag.get_text(strip=True).split(":", 1)[1].strip(),
                "description": description.get_text(strip=True),
            })

        time.sleep(2)  # polite wait

    finally:
        driver.quit()

    df = pd.DataFrame(results)
    return df

def prepare_card_tables(rating_df: pd.DataFrame, card_df: pd.DataFrame):
    """
    Prepare card rating table linking to card_id.
    Unmatched card names are ignored.

    """

    df = rating_df.copy()

    # Map card_name to card_id
    name_to_id = dict(zip(card_df['name'], card_df['card_id']))
    df['card_id'] = df['card_name'].map(name_to_id)

    # Keep only matched rows
    df = df[df['card_id'].notna()]

    # Keep only needed columns
    card_rating_df = df[['card_id', 'ai_rating', 'pro_rating', 'description']].copy()

    return card_rating_df
