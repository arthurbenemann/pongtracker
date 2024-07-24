from openskill.models import PlackettLuce
import pandas as pd
from collections import Counter
from itertools import combinations


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

def qualityMatches(df,players,model):
    df_last = df.iloc[[-1]]
    df_last = df_last.drop(columns=['date','win','loss'])
    two_player_combinations = list(combinations(players, 2))
    
        # Filter combinations to ensure the teams are disjoint
    matches = []
    for combo1 in two_player_combinations:
        remaining_players = set(players) - set(combo1)
        for combo2 in combinations(remaining_players, 2):
            if set(combo2).isdisjoint(set(combo1)):
                # Sort and add the match to the list
                match = [sorted(combo1), sorted(combo2)]
                if match not in matches:
                    matches.append(match)
    
    match_score ={}
    for match in matches:
        match_name = match[0][0].name + match[0][1].name+' vs '+ match[1][0].name+match[1][1].name
        match_score[match_name] = model.predict_draw(match)
    
    df_matchscore = pd.DataFrame(match_score.items(),columns=['match', 'quality'])

    return df_matchscore
