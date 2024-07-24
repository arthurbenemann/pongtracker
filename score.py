from openskill.models import PlackettLuce
import pandas as pd
from collections import Counter


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
            "MMR": [int(df[player].tail(1)) for player in players],
            "wins": [win_count[player] for player in players],
            "losses": [loss_count[player] for player in players],
        }
    )
    return result_df.sort_values(by='MMR',ascending=False)


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
            df.loc[index, player.name] = player.ordinal(alpha=200/model.sigma, target=1500) # Elo scaling
    return df, players, model

