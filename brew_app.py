import pandas as pd
import streamlit as st
# from dotenv import load_dotenv
# import os


# from janitor import clean_names

# Get and clean data
# load_dotenv()
# url = os.getenv("DATA_URL")
url = st.secrets["data_url"]
brew_df = pd.read_csv(url)
# brew_df = brew_df.clean_names()  
brew_df = brew_df.rename(columns={
    "Year": "year",
    "Date": "date",
    "Time": "time",
    "Brewer": "brewer"
})


# Create method column
brew_df["method"] = brew_df.brewer.case_when(caselist=[
    (brew_df.brewer.str.contains("Espresso|Gaggia"), "Espresso"),
    (brew_df.brewer.str.contains("Pourover|Chemex|V60|Clever|Pulsar"), "Pourover"),
    (pd.Series(True), "Other")
])

# (Temporarily subset to records with nonempty date and time values)
brew_df = brew_df.dropna(subset=["date", "time"])

# Produce year, month column ym to plot by
    # Cast date to date type
brew_df["date"] = pd.to_datetime(brew_df.date)
    # Get year an month components
brew_df['year'] = brew_df['date'].dt.year
brew_df['month'] = brew_df['date'].dt.month
    # Prepend single digit months with 0
brew_df['month'] = brew_df.month.case_when(caselist=[
    (brew_df.month.lt(10), "0" + brew_df.month.astype("str")),
    (pd.Series(True), brew_df.month.astype("str"))
])
    # Combine and revert to integer
brew_df["ym"] = brew_df.year.astype("str") + brew_df.month.astype("str")
brew_df["ym"] = brew_df.ym.astype("int32")

brew_type_by_month_df = brew_df[["ym", "method"]].value_counts().to_frame("count").reset_index()

st.bar_chart(brew_type_by_month_df, x = "ym", y="count", color="method")
