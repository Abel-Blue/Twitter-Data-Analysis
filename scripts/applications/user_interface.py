import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px


def loadData():
    query = "select * from tweets"
    # df = db_execute_fetch(query, dbName="tweet_db", rdf=True)
    df = pd.read_csv(
        'data/cleaned_economic_data.csv')
    return df


def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)


def wordCloud():
    df = loadData()
    cleanText = ''
    for text in df['retweet_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='black',
                   min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())


def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['screen_name'])[
                           'retweet_text'].count()}).reset_index()
    dfCount["screen_name"] = dfCount["screen_name"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    numBC = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {numBC} Ranking By Number of tweets"
    barChart(dfCount.head(numBC), title, "screen_name", "Tweet_count")


def langPie():
    df = loadData()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(
        ['lang'])['retweet_text'].count()}).reset_index()
    dfLangCount["lang"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count']
                    < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count',
                 names='lang', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)


def tweetSentiments():
    df = loadData()
    st.title(" Tweets Sentiment Chart")
    st.bar_chart(df.sentiment.value_counts())


def app():
    st.title("Data Visualizations")
    wordCloud()
    with st.expander("Show More Graphs"):
        stBarChart()
        langPie()
        tweetSentiments()
