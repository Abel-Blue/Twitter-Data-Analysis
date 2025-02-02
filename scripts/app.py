import streamlit as st
from multiapp import MultiApp
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

# The main app
app.run()
