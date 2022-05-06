import streamlit as st
from multiapp import MultiApp
import mysql.connector
from applications import basic_eda, user_interface, user_interface1, sentiment_model

st.set_page_config(page_title="Twitter Analysis Visualization", layout="wide")

app = MultiApp()

st.sidebar.markdown("""
# Multi-Page App
This multi-page app is using the [streamlit-multiapps]
(https://github.com/upraneelnihar/streamlit-multiapps) 
framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). 
Also check out his [Medium article](https://medium.com/@u
.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
# Modifications
\t- Page Folder Based Access
\t- Presentation changed to SideBar
""")

# Add all your application here
app.add_app("Basic EDA", basic_eda.app)
app.add_app("Dynamic page 1", user_interface1.app)
app.add_app("Dynamic page 2", user_interface.app)
app.add_app("Sentiment analysis", sentiment_model.app)

# Initialize connection.
# Uses st.experimental_singleton to only run once.


@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])


conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


run_query("SELECT * from tweets;")

# The main app

app.run()
