from openskill.models import PlackettLuce
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
import re
import argparse


def getUniquePlayers(df: pd.DataFrame) -> list[str]:
    df[["win", "loss"]] = df[["win", "loss"]].applymap(lambda x: set(x))
    unique_players = list(set().union(*df["win"], *df["loss"]))
    unique_players.sort()
    return unique_players


def calcTotalWinLoss(df: pd.DataFrame)-> pd.DataFrame:
    # Flatten the 'win' and 'loss' columns into lists
    win_list = [player for win_set in df["win"] for player in win_set]
    loss_list = [player for loss_set in df["loss"] for player in loss_set]

    # Count the occurrences of each player
    win_count = Counter(win_list)
    loss_count = Counter(loss_list)

    # Combine the counts into a DataFrame
    players = set(win_count.keys()).union(set(loss_count.keys()))

    result_df = pd.DataFrame(
        {
            "player": list(players),
            "wins": [win_count[player] for player in players],
            "losses": [loss_count[player] for player in players],
        }
    )
    return result_df


def calcRatings(df: pd.DataFrame) -> pd.DataFrame:
    model = PlackettLuce()

    players = {model.rating(name=player) for player in getUniquePlayers(df)}
    for player in players:
        if player.name not in df.columns:
            df[player.name] = pd.NA

    # Update ratings based on matches
    for index, row in df.iterrows():
        winners = [obj for obj in players if obj.name in row["win"]]
        losers = [obj for obj in players if obj.name in row["loss"]]

        match = [winners, losers]
        model.rate(match)

        for player in players:
            df.loc[index, player.name] = player.ordinal()
    return df


def parse_google_sheet_url(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError("Invalid Google Sheets URL")
    sheet_id = match.group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    return csv_url


def getDataFromGSheet(url: str) -> pd.DataFrame:
    df = pd.read_csv(url, parse_dates=["date"])
    df = df.ffill()
    return df


def processGSheet(url: str):

    df = getDataFromGSheet(url)
    df = calcRatings(df)
    totals = calcTotalWinLoss(df)

    print(df)
    print(totals)

    df[getUniquePlayers(df)].plot(kind="line")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Process pongtracker URL")
    parser.add_argument("url", type=str, help="URL to Gsheet process")
    args = parser.parse_args()
    csv_url = parse_google_sheet_url(args.url)
    processGSheet(csv_url)


if __name__ == "__main__":
    main()
