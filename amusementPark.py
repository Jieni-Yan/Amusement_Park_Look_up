from os import major
# from google.cloud import firestore
# from google.oauth2 import service_account

import streamlit as st
import json
import pandas as pd
import numpy as np
# from st_aggrid import AgGrid, GridOptionsBuilder
# from st_aggrid.shared import GridUpdateMode
from PIL import Image
import altair as alt

# import matplotlib.pyplot as plt
# import plotly.figure_factory as ff
# import plotly.graph_objects as go
# import plotly.express as px
#
#
# from constants import *
# from neo4j_controller import Neo4jController
# import graphviz

from neo4j import GraphDatabase

# key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds, project="college-return-on-investment")


navi = st.sidebar.radio("Navigation", ["Amusement Park Home Page", "Display", "Loan Repayment Calculator", "Contact Us"])

if navi == "Amusement Park Home Page":
    # st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
    # st.title("🎓 Diploma PDF Generator")
    # with open('choice.txt', 'w') as f:
    #     f.write('None')
    
    # image = Image.open('UNIROI.png')
    # st.image(image)

   
    st.subheader("What is UNIROI?")
    st.write("UNIROI is a webpage platform where you can search for your interested colleges and/or majors to see the financial aspect around them. "
             "The main purpose of this platform is to provide financial information that could help you make decision on which college to go to and/or which major to pursue, "
             "in another terms, whether your decision is worth it in terms of financial investment.")
    st.write("-------------------------------------------------------------------------------------------------------")
    
    st.subheader("What is the motivation behind UNIROI?")
    st.write("When it comes to pursuing a college degree, many prospective students don’t know exactly where to start."
             " There are a lot of factors such as passion, strength, personality, tuition fee, debt after graduation, "
             "etc,... to take into account when choosing a major and which college to go to.")
    st.write("Many prospective students don’t have the privilege of having family members or someone they know that had such experiences to help "
             "guide them. These students often fall into the groups of first generation college students and "
             "underrepresented minorities.")
    st.write("Additionally, American college graduates have an average of $30000 loan debt. "
             "Some graduates may end up being in more debt due to the college they pick and/or the major they choose.")
    st.write("We want to build a website that provides prospective college students an understanding of the finance "
             "factor when it comes to getting a college degree, especially for helping first generation college students "
             "and underrepresented minorities who don’t have much resources around them.")
    st.write("-------------------------------------------------------------------------------------------------------")

    st.subheader("How to use UNIROI?")
    st.write("Two main uses of UNIROI are:" )
    st.write("- Searching for colleges/majors for finances information, which can be further explored by clicking 'University/Major Search' on the navigation bar.")
    st.write("- Calculate the total time and money for repaying loan debt, which can be further explored by clicking 'Loan Repayment Calculator' on the navigation bar.")
    st.write("-------------------------------------------------------------------------------------------------------")

    st.write("This webpage platform were built by Duyen Nguyen, Kaiyin Chan and Jieni Yan.")

if navi == "Display":
    #driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", "neo"))

    st.title("Amusement Park KG")
    st.write("In this page, you can select the amusement park you want to know, and we will show you the top 10 Amusement parks information.")
    # st.image(Image.open("images/uk-charts.png"))

    # with driver.session() as session:
    #     st.subheader("Number 1s")
    #     st.write("The chart below shows the number 1 charting songs of 2019.")
    #     result = session.run("""
    #     MATCH (chart:Chart)<-[inChart:IN_CHART {position: 1}]-(song)-[:ARTIST]->(artist)
    #     WITH chart, song, collect(artist.name) AS artists
    #     RETURN toString(chart.end) AS date, song.title AS song, artists
    #     ORDER BY chart.end
    #     """)
    #     df = pd.DataFrame(result.data())
    #     st.dataframe(df.style.hide_index())

    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        # text = link.split('=')[1]
        return f'<a target="_blank" href="{link}"></a>'


    d = {'col1': [1, 2], 'link': ["https://www.kentuckykingdom.com/", "http://beachboardwalk.com/"]}
    df = pd.DataFrame(data=d)
    # link is the column with hyperlinks
    df['link'] = df['link'].apply(make_clickable)
    df = df.to_html(escape=False)
    st.write(df, unsafe_allow_html=True)
