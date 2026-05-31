# WhenDataTalks 📊🎬

> Python projects exploring data, APIs, and machine learning through real-world entertainment datasets.

---

## 🗂 Projects

---

### 🎥 Day 4 — Bollywood vs Hollywood Dashboard

Scraped live box office data from the web and built a dark-themed dashboard comparing the two biggest film industries in the world.

**✨ Highlights**
- 🕸️ Live scraping with BeautifulSoup
- 🧹 Automated data cleaning pipeline
- 🌑 Dark-themed matplotlib dashboard
- 📊 Side-by-side industry comparison

**🛠 Stack:** `Python` · `BeautifulSoup` · `pandas` · `matplotlib`

```bash
python scraper.py
python clean.py
python dashboard.py
```

---

### 🌐 Day 5 — Multi-API Analytics Terminal

A live data terminal that pulls from 4 different APIs simultaneously and generates automated weekly reports.

**✨ Highlights**
- ☁️ Live weather tracking
- 💻 GitHub profile analytics
- ₿ Cryptocurrency price monitoring
- 🎬 TMDB movie trend analysis
- 📋 Automated Friday digest report

**🔗 APIs:** `OpenWeather` · `GitHub` · `CoinGecko` · `TMDB`

**🛠 Stack:** `Python` · `requests` · `pandas` · `python-dotenv`

```bash
python live_data_terminal.py
python friday_report.py
```

---

### 🤖 Day 6 — CinePredict AI

A machine learning web app that predicts whether a movie will be a **HIT or FLOP** — trained on real scraped data, enriched via TMDB, and deployed as an interactive Streamlit app.

**✨ Highlights**
- 🧹 Real box office data cleaned from scratch
- 🎯 Random Forest classifier — 96 movies, 7 features
- 📈 Confidence score + feature importance breakdown
- 🌐 Live Streamlit web app with sliders and dropdowns

**🛠 Stack:** `Python` · `scikit-learn` · `pandas` · `Streamlit`

```bash
python dataset.py        # build & enrich dataset
python train.py          # train model → model.pkl
python -m streamlit run app.py   # launch web app
```

---

## 🧰 Full Stack

`Python` · `BeautifulSoup` · `pandas` · `matplotlib` · `scikit-learn` · `Streamlit` · `REST APIs`

---

> Built as a hands-on learning sprint in data analytics, APIs, and machine learning. 🚀




