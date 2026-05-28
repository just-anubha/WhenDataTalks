
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_KEY = os.getenv("TMDB_KEY")

import requests
import datetime
import time

from textwrap import shorten

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table


# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────


BASE = "https://api.themoviedb.org/3"

console = Console()


# ────────────────────────────────────────────────
# FETCH API DATA
# ────────────────────────────────────────────────

def fetch(url):

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                timeout=15
            )

            return response.json()

        except Exception:

            if attempt < 2:

                console.print(
                    f"[yellow]Retrying... ({attempt + 1}/3)[/yellow]"
                )

                time.sleep(2)

            else:

                console.print(
                    "[bold red]⚠ Failed to fetch data[/bold red]"
                )

                return {}


# ────────────────────────────────────────────────
# SECTION DIVIDER
# ────────────────────────────────────────────────

def divider(title):

    console.print(
        Rule(
            f"[bold yellow]{title}[/bold yellow]"
        )
    )


# ────────────────────────────────────────────────
# GENRE HELPER
# ────────────────────────────────────────────────

def get_genre_name(genre_id):

    genres = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Sci-Fi",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    return genres.get(genre_id, "Other")


# ────────────────────────────────────────────────
# THEATRES
# ────────────────────────────────────────────────

def get_theatres():

    divider("🎭 IN THEATRES RIGHT NOW · Global")

    url = (
        f"{BASE}/movie/now_playing"
        f"?api_key={TMDB_KEY}"
        f"&language=en-US"
    )

    data = fetch(url)

    movies = data.get("results", [])[:5]

    ratings = []
    genres_seen = []

    if not movies:

        console.print(
            "[red]No theatre data found.[/red]"
        )

        return [], []

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_magenta",
        expand=True
    )

    table.add_column("#", style="cyan", width=3)
    table.add_column("Movie", style="white", width=24)
    table.add_column("⭐", style="green", width=6)
    table.add_column("Genre", style="magenta", width=10)

    for i, m in enumerate(movies, 1):

        title = shorten(
            m.get("title", "Unknown"),
            width=22,
            placeholder="..."
        )

        rating = m.get("vote_average", 0)

        genre = get_genre_name(
            m["genre_ids"][0]
            if m.get("genre_ids")
            else 0
        )

        ratings.append(rating)
        genres_seen.append(genre)

        table.add_row(
            str(i),
            title,
            f"{rating:.1f}",
            genre
        )

    console.print(table)

    return ratings, genres_seen


# ────────────────────────────────────────────────
# OTT BOLLYWOOD
# ────────────────────────────────────────────────

def get_bollywood_trending():

    divider("📺 OTT BOLLYWOOD · Trending This Week")

    url = (
        f"{BASE}/discover/movie?api_key={TMDB_KEY}"
        f"&with_original_language=hi"
        f"&sort_by=popularity.desc"
        f"&language=en-US"
    )

    data = fetch(url)

    movies = [
        m for m in data.get("results", [])
        if m.get("vote_count", 0) > 20
    ][:5]

    if not movies:

        console.print(
            "[red]No OTT Bollywood data found.[/red]"
        )

        return []

    ratings = []

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_magenta",
        expand=True
    )

    table.add_column("#", style="cyan", width=3)
    table.add_column("Movie", style="white", width=22)
    table.add_column("⭐", style="green", width=6)
    table.add_column("Genre", style="magenta", width=10)
    table.add_column("👁", style="yellow", width=10)

    for i, m in enumerate(movies, 1):

        title = shorten(
            m.get("title", "Unknown"),
            width=20,
            placeholder="..."
        )

        rating = m.get("vote_average", 0)

        votes = m.get("vote_count", 0)

        genre = get_genre_name(
            m["genre_ids"][0]
            if m.get("genre_ids")
            else 0
        )

        ratings.append(rating)

        table.add_row(
            str(i),
            title,
            f"{rating:.1f}",
            genre,
            f"{votes:,}"
        )

    console.print(table)

    return ratings


# ────────────────────────────────────────────────
# COMING SOON
# ────────────────────────────────────────────────

def get_coming_soon():

    divider("🍿 COMING SOON · Upcoming Releases")

    url = (
        f"{BASE}/movie/upcoming"
        f"?api_key={TMDB_KEY}"
        f"&language=en-US"
    )

    data = fetch(url)

    movies = data.get("results", [])[:5]

    if not movies:

        console.print(
            "[red]No upcoming movies found.[/red]"
        )

        return "N/A"

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_magenta",
        expand=True
    )

    table.add_column("#", style="cyan", width=3)
    table.add_column("Movie", style="white", width=22)
    table.add_column("Date", style="green", width=14)
    table.add_column("Genre", style="magenta", width=10)

    for i, m in enumerate(movies, 1):

        title = shorten(
            m.get("title", "Unknown"),
            width=20,
            placeholder="..."
        )

        release_date = m.get(
            "release_date",
            "N/A"
        )

        genre = get_genre_name(
            m["genre_ids"][0]
            if m.get("genre_ids")
            else 0
        )

        table.add_row(
            str(i),
            title,
            release_date,
            genre
        )

    console.print(table)

    top = max(
        movies,
        key=lambda x: x.get("popularity", 0)
    )

    return top.get("title", "N/A")


# ────────────────────────────────────────────────
# BOLLYWOOD CLASSICS
# ────────────────────────────────────────────────

def get_bollywood_alltime():

    divider("🌟 BOLLYWOOD ALL-TIME GREATS")

    url = (
        f"{BASE}/discover/movie?api_key={TMDB_KEY}"
        f"&with_original_language=hi"
        f"&sort_by=vote_average.desc"
        f"&vote_count.gte=1000"
        f"&language=en-US"
    )

    data = fetch(url)

    movies = data.get("results", [])[:5]

    if not movies:

        console.print(
            "[red]No Bollywood classics found.[/red]"
        )

        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="bright_magenta",
        expand=True
    )

    table.add_column("#", style="cyan", width=3)
    table.add_column("Movie", style="white", width=22)
    table.add_column("⭐", style="green", width=6)
    table.add_column("Year", style="blue", width=8)
    table.add_column("👁", style="yellow", width=10)

    for i, m in enumerate(movies, 1):

        title = shorten(
            m.get("title", "Unknown"),
            width=20,
            placeholder="..."
        )

        rating = m.get("vote_average", 0)

        votes = m.get("vote_count", 0)

        release_date = m.get(
            "release_date",
            ""
        )

        year = (
            release_date[:4]
            if release_date
            else "N/A"
        )

        table.add_row(
            str(i),
            title,
            f"{rating:.1f}",
            year,
            f"{votes:,}"
        )

    console.print(table)


# ────────────────────────────────────────────────
# FINAL VERDICT
# ────────────────────────────────────────────────

def print_verdict(
    theatre_ratings,
    bollywood_ratings,
    most_anticipated,
    theatre_genres
):

    divider("🏆 THE VERDICT · OTT vs THEATRE")

    avg_theatre = (
        sum(theatre_ratings) / len(theatre_ratings)
        if theatre_ratings else 0
    )

    avg_ott = (
        sum(bollywood_ratings) / len(bollywood_ratings)
        if bollywood_ratings else 0
    )

    if avg_theatre > avg_ott:

        winner = (
            "[bold green]"
            "🎭 Theatre is beating OTT this week!"
            "[/bold green]"
        )

    elif avg_ott > avg_theatre:

        winner = (
            "[bold yellow]"
            "📺 OTT is beating theatres this week!"
            "[/bold yellow]"
        )

    else:

        winner = (
            "[bold blue]"
            "🤝 Dead tie this week!"
            "[/bold blue]"
        )

    top_genre = (
        max(
            set(theatre_genres),
            key=theatre_genres.count
        )
        if theatre_genres
        else "N/A"
    )

    verdict = (
        f"[bold cyan]Theatre avg rating[/bold cyan] : "
        f"[green]{avg_theatre:.2f} ⭐[/green]\n\n"

        f"[bold cyan]OTT Bollywood avg[/bold cyan] : "
        f"[green]{avg_ott:.2f} ⭐[/green]\n\n"

        f"{winner}\n\n"

        f"[bold cyan]Top theatre genre[/bold cyan] : "
        f"[magenta]{top_genre}[/magenta]\n\n"

        f"[bold cyan]Most anticipated film[/bold cyan] : "
        f"[green]{most_anticipated}[/green]\n"
    )

    console.print(
        Panel.fit(
            verdict,
            border_style="bright_magenta",
            title="[bold yellow]VERDICT[/bold yellow]"
        )
    )

    console.print(
        "\n[dim]Data powered by TMDB · WhenDataTalks[/dim]"
    )


# ────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────

if __name__ == "__main__":

    now = datetime.datetime.now().strftime(
        "%d %b %Y  %H:%M"
    )

    day = datetime.datetime.now().strftime(
        "%A"
    )

    console.print()

    console.print(
        Panel.fit(
            f"[bold cyan]🎬 THE FRIDAY REPORT[/bold cyan]\n\n"
            f"[white]{day}, {now}[/white]\n\n"
            f"[green]WhenDataTalks[/green]",
            border_style="bright_magenta"
        )
    )

    theatre_ratings, theatre_genres = (
        get_theatres()
    )

    time.sleep(2)

    bollywood_ratings = (
        get_bollywood_trending()
    )

    time.sleep(2)

    most_anticipated = (
        get_coming_soon()
    )

    time.sleep(2)

    get_bollywood_alltime()

    time.sleep(1)

    print_verdict(
        theatre_ratings,
        bollywood_ratings,
        most_anticipated,
        theatre_genres
    )

    console.print()
