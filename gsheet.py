import re
import pandas as pd


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
