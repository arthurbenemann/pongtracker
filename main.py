import score
import gsheet
from matplotlib import pyplot as plt
import argparse
import pandas as pd

from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import io


app = Flask(__name__)

@app.route('/')
def index():

    df = gsheet.getDfFromGsheet(app.url)
    processAndPlot(df)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Return the plot as a response
    return send_file(img, mimetype='image/png')


def processAndPlot(df: pd.DataFrame):
    df = score.calcRatings(df)
    totals = score.calcTotalWinLoss(df)
    df_by_eod = df[['date']+score.getUniquePlayers(df)].groupby('date').last()

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), height_ratios=[2, 1])
    trendPlot = axes[0]
    df_by_eod.plot(kind="line", ax=trendPlot)
    trendPlot.set_xticks(df_by_eod.index)
    trendPlot.set_xticklabels(df_by_eod.index.strftime('%Y-%m-%d'), rotation=45)
    trendPlot.grid()

    tablePlot = axes[1]
    tablePlot.xaxis.set_visible(False)
    tablePlot.yaxis.set_visible(False)
    tablePlot.set_frame_on(False)
    tablePlot.table(cellText=totals.values, colLabels=totals.columns, cellLoc='center', loc='center')


def main():
    parser = argparse.ArgumentParser(description="Process pongtracker URL")
    parser.add_argument("url", type=str, help="URL to Gsheet process")
    args = parser.parse_args()

    app.url = args.url

    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
