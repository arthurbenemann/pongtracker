import score
import gsheet
from matplotlib import pyplot as plt
import argparse
import pandas as pd


def processAndPlot(df: pd.DataFrame):
    df = score.calcRatings(df)
    totals = score.calcTotalWinLoss(df)

    print(df)
    print(totals)

    df_by_eod = df[['date']+score.getUniquePlayers(df)].groupby('date').last()

    ax = df_by_eod.plot(kind="line")
    ax.set_xticks(df_by_eod.index)  
    ax.set_xticklabels(df_by_eod.index.strftime('%Y-%m-%d'), rotation=45)

    ax.grid()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Process pongtracker URL")
    parser.add_argument("url", type=str, help="URL to Gsheet process")
    args = parser.parse_args()

    df = gsheet.getDfFromGsheet(args.url)
    processAndPlot(df)


if __name__ == "__main__":
    main()
