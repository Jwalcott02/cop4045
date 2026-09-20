"""Problem 4: IMDB CSV data."""

import csv


def load_rank_csv(filename: str, value_type=float) -> dict:
    """Load a Rank,Title,Year,Value csv file into a dict keyed by (title, year)."""
    try:
        d = {}
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for rank, title, year, value in reader:
                d[(title, int(year))] = value_type(value)
        return d
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        raise


def load_casts(filename: str) -> dict:
    """Load imdb-top-casts.csv into a dict keyed by (title, year)."""
    try:
        d = {}
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for title, year, director, *actors in reader:
                d[(title, int(year))] = (director, actors)
        return d
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        raise


def print_ranking(items: list, top_n: int = None) -> None:
    """Print a list of ranked items, cut to top_n if given."""
    for i, item in enumerate(items[:top_n], start=1):
        print(i, item)


def display_top_collaborations(top_rated_file: str, casts_file: str, top_n: int = None) -> None:
    """Rank (director, actor, count) pairs for top rated movies."""
    try:
        top_rated = load_rank_csv(top_rated_file, float)
        casts = load_casts(casts_file)

        counts = {}
        for key, (director, actors) in casts.items():
            if key in top_rated:
                for actor in actors:
                    counts[(director, actor)] = counts.get((director, actor), 0) + 1

        ranking = [(d, a, c) for (d, a), c in counts.items()]
        ranking.sort(key=lambda x: x[2], reverse=True)
        print_ranking(ranking, top_n)
    except Exception as e:
        print(f"Error in display_top_collaborations: {e}")
        raise


def display_top_actors(top_grossing_file: str, casts_file: str, top_n: int = None) -> None:
    """Rank actors by total box office of top grossing movies they acted in."""
    try:
        top_grossing = load_rank_csv(top_grossing_file, int)
        casts = load_casts(casts_file)

        totals = {}
        for key, (director, actors) in casts.items():
            if key in top_grossing:
                for actor in actors:
                    totals[actor] = totals.get(actor, 0) + top_grossing[key]

        ranking = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        print_ranking(ranking, top_n)
    except Exception as e:
        print(f"Error in display_top_actors: {e}")
        raise


def main() -> None:
    """Test display_top_collaborations and display_top_actors."""
    print("FAU ID: Z23692334")

    print("\na)")
    display_top_collaborations("imdb-top-rated.csv", "imdb-top-casts.csv", 10)

    print("\nb)")
    display_top_actors("imdb-top-grossing.csv", "imdb-top-casts.csv", 10)


if __name__ == "__main__":
    main()