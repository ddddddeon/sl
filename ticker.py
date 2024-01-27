from datetime import date, timedelta
import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt

def data_diff(field, col):
    with col:
        today = round(df[field].iloc[-1], 2)
        yesterday = round(df[field].iloc[-2], 2)
        diff = round(((today - yesterday) / yesterday) * 100, 2)
        col.metric(label=field, value=today, delta=f"{diff}%", )

st.title("Ticker")
        
symbol = st.text_input("Ticker symbol", "GOOGL")
title = f"Ticker - {symbol}"
data = yf.Ticker(symbol)

col1, col2, _ = st.columns(3)
today = date.today()
start = col1.date_input("Start", today - timedelta(365 * 5))
end = col2.date_input("End", today)

with st.spinner(f"Loading ticker data for {symbol}..."):
    df = data.history(period="1d", start=start, end=end)
    df.reset_index(level=0, inplace=True, col_level=0, col_fill="Date")
    df["Volume (Millions)"] = df["Volume"] / 1000000

    col1, col2, col3, col4 = st.columns(4)
    data_diff("Close", col1)
    data_diff("High", col2)
    data_diff("Low", col3)
    data_diff("Volume (Millions)", col4)

    price_chart = alt.Chart(df).mark_line().encode(x="Date", y="Close").interactive()
    volume_chart = alt.Chart(df, height=200).mark_line().encode(x="Date", y="Volume (Millions)").interactive()
    st.altair_chart(price_chart, use_container_width=True)
    st.altair_chart(volume_chart, use_container_width=True)

st.write("Chris d'Eon, 2024")
