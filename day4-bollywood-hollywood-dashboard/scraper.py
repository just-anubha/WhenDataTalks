import requests
from bs4 import BeautifulSoup
import pandas as pd

BOLLYWOOD_URL = "https://en.wikipedia.org/wiki/List_of_highest-grossing_Indian_films"
HOLLYWOOD_URL = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

def get_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def scrape_bollywood():
    print("Scraping Bollywood data...")
    soup = get_page(BOLLYWOOD_URL)
    tables = soup.find_all("table", class_="wikitable")
    table = tables[0]
    rows = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) >= 5:
            rows.append({
                "title": cols[1].text.strip(),
                "worldwide_gross": cols[2].text.strip(),
                "year": cols[4].text.strip(),
                "industry": "Bollywood"
            })
    df = pd.DataFrame(rows)
    print(f"Found {len(df)} Bollywood films!")
    print(df.head())
    return df

def scrape_hollywood():
    print("Scraping Hollywood data...")
    soup = get_page(HOLLYWOOD_URL)
    tables = soup.find_all("table", class_="wikitable")
    table = tables[0]
    rows = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) == 6:
            rows.append({
                "title": cols[2].text.strip(),
                "year": cols[5].text.strip(),
                "worldwide_gross": cols[3].text.strip(),
                "industry": "Hollywood"
            })
    df = pd.DataFrame(rows)
    print(f"Found {len(df)} Hollywood films!")
    print(df.head())
    return df

# Scrape both
bollywood_df = scrape_bollywood()
hollywood_df = scrape_hollywood()

# Combine into one big table
combined_df = pd.concat([bollywood_df, hollywood_df], ignore_index=True)

# Save to data/ folder
bollywood_df.to_csv("data/bollywood.csv", index=False)
hollywood_df.to_csv("data/hollywood.csv", index=False)
combined_df.to_csv("data/combined.csv", index=False)

print(f"\n✅ Done! Total films collected: {len(combined_df)}")
print(f"   Bollywood: {len(bollywood_df)} films")
print(f"   Hollywood: {len(hollywood_df)} films")
print("\n📁 Saved to data/ folder!")