import streamlit as st
import gsheet
import score
import pandas as pd
import altair as alt
import os

st.set_page_config(
    page_title="PongTracker",
    page_icon=":table_tennis_paddle_and_ball:",
    layout= "wide"
    )

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

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(totals, hide_index=True, use_container_width=True)
    with col2:
        df_matchscore = score.qualityMatches(df, players, model)
        st.dataframe(df_matchscore.sort_values('quality', ascending=False), 
                     hide_index=True, use_container_width=True)

    with st.expander("Game Log"):
        df.set_index("date", inplace=True)
        st.dataframe(df.style.format(precision=0), height=4000,
                     use_container_width=True)


    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Game database",url_gsheet) 
    with col2:
        st.link_button("Codebase","https://github.com/arthurbenemann/pongtracker")                     
