import streamlit as st
from multi import MultiApp
# import your app modules here
import eda_streamlit

st.set_page_config(page_title="Twitter Analysis Visualization", layout="wide")

app = MultiApp()


st.sidebar.markdown("""
# Multi-Page App
This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).
# Modifications
\t- Page Folder Based Access
\t- Presentation changed to SideBar
""")

# Add all your application here
app.add_app("Analysis", eda_streamlit.app)
# The main app
app.run()
