from dotenv import load_dotenv
import os
import requests
import datetime

# ── LOAD ENV VARIABLES ──────────────────────────
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(API_KEY)

CITY = os.getenv("CITY")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# ── HELPERS ─────────────────────────────────────
def divider(title):
    width = 50
    print("\n" + "─" * width)
    print(f"  {title}")
    print("─" * width)

# ── WEATHER ─────────────────────────────────────
def get_weather():
    divider("🌤  LIVE WEATHER  ·  " + CITY)
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric"
    )
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            print(f"  Error: {data.get('message')}")
            return

        temp       = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity   = data["main"]["humidity"]
        condition  = data["weather"][0]["description"].title()
        wind       = data["wind"]["speed"]
        city_name  = data["name"]
        country    = data["sys"]["country"]

        print(f"  📍 Location   : {city_name}, {country}")
        print(f"  🌡  Temperature: {temp}°C")
        print(f"  🤔 Feels like : {feels_like}°C")
        print(f"  💧 Humidity   : {humidity}%")
        print(f"  ☁️  Condition  : {condition}")
        print(f"  💨 Wind speed : {wind} m/s")

    except Exception as e:
        print(f"  Could not fetch weather: {e}")

# ── GITHUB STATS ────────────────────────────────
def get_github():
    divider("👨‍💻  GITHUB STATS  ·  " + GITHUB_USERNAME)
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    try:
        response = requests.get(url)
        data = response.json()

        if "message" in data:
            print(f"  Error: {data['message']}")
            return

        print(f"  👤 Name       : {data.get('name', 'N/A')}")
        print(f"  📦 Public repos: {data.get('public_repos', 0)}")
        print(f"  👥 Followers  : {data.get('followers', 0)}")
        print(f"  👣 Following  : {data.get('following', 0)}")
        print(f"  🔗 Profile    : {data.get('html_url')}")

        # Also fetch repo list
        repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
        repos_res = requests.get(repos_url)
        repos     = repos_res.json()

        if isinstance(repos, list) and repos:
            print(f"\n  📁 Your repos:")
            for repo in repos[:5]:
                stars = repo.get('stargazers_count', 0)
                print(f"     ★ {repo['name']}  —  ⭐ {stars} stars")

    except Exception as e:
        print(f"  Could not fetch GitHub stats: {e}")

# ── CRYPTO BONUS ────────────────────────────────
def get_crypto():
    divider("₿  LIVE CRYPTO PRICES")
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,solana"
        "&vs_currencies=usd,inr"
    )
    try:
        response = requests.get(url)
        data = response.json()

        coins = {
            "bitcoin" : "₿  Bitcoin ",
            "ethereum": "Ξ  Ethereum",
            "solana"  : "◎  Solana  "
        }
        for coin_id, label in coins.items():
            if coin_id in data:
                usd = data[coin_id].get("usd", "N/A")
                inr = data[coin_id].get("inr", "N/A")
                print(f"  {label}: ${usd:,}  /  ₹{inr:,}")

    except Exception as e:
        print(f"  Could not fetch crypto: {e}")

# ── MAIN ────────────────────────────────────────
if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
    print("\n" + "═" * 50)
    print(f"  📡  LIVE DATA TERMINAL")
    print(f"  {now}")
    print("═" * 50)

    get_weather()
    get_github()
    get_crypto()

    print("\n" + "═" * 50)
    print("  Data fetched live  ·  WhenDataTalks")
    print("═" * 50 + "\n")