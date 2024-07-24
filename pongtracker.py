import streamlit as st
import gsheet
import score
import pandas as pd
import altair as alt
import os
from itertools import combinations

st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

url_gsheet = os.getenv('URL_GSHEET')
if url_gsheet is None:
    st.warning("Pass URL_GSHEET as enviroment var, with url of game database")
    st.stop()
else:
    st.link_button("Game database",url_gsheet)

    df = gsheet.getDfFromGsheet(url_gsheet)
    df, players, model = score.calcRatings(df)
    totals = score.calcTotalWinLoss(df)
    df_by_eod = df[["date"] + score.getUniquePlayers(df)].groupby("date").last()


    df_by_eod = df_by_eod.reset_index()
    df_by_eod.rename(columns={"index": "date"}, inplace=True)
    df_by_eod = pd.melt(df_by_eod, id_vars="date", var_name="player", value_name="MMR")

    c = (
        alt.Chart(df_by_eod)
        .mark_line()
        .encode(
            x="date:T",
            y=alt.Y("MMR:Q", scale=alt.Scale(zero=False)),
            color="player:N",
        )
    )

    st.altair_chart(c.interactive(), use_container_width=True)

    st.dataframe(totals, hide_index=True)

    df_last = df.iloc[[-1]]
    df_last = df_last.drop(columns=['date','win','loss'])
    two_player_combinations =list(combinations(players, 2))

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

    df_matchscore = pd.DataFrame(columns=['match', 'quality'])
    for match in matches:
        match_name = match[0][0].name + match[0][1].name+' vs '+ match[1][0].name+match[1][1].name
        match_score = model.predict_draw(match)
        df_matchscore = df_matchscore.append({'match':match_name, 'quality': match_score},ignore_index=True)
    
    st.dataframe(df_matchscore.sort_values('quality', ascending=False), hide_index=True)

    with st.expander("Game Log"):
        df.set_index("date", inplace=True)
        st.dataframe(df.style.format(precision=0), height=4000, use_container_width=True)
