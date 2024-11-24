
from requests.api import options
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt


st.set_page_config(page_title="Table Crawler", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

connection = False
tables=[]
 
# Sidebar config
with st.sidebar:
    st.title("Table Crawler")
    st.write("A simple table crawler built with Python")
    
    # Input for URL
    url_w = st.text_input("Please enter the URL to scrape the tables", key="text")
    col1, col2 = st.columns([1,1])
    
    # Clicked status for click me button
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    # Function for enabling clicked 
    def click_button():
        st.session_state.clicked = True

    # Function for enabling clicked 
    def clear_button():
        st.session_state.clicked = False
        st.session_state.text = ""
    
    with col1:
        # Button for click me
        st.button('Click me', on_click=click_button,type='primary', use_container_width=True)
                  
    with col2:
        st.button('Clear',on_click=clear_button, type='secondary',use_container_width=True)
        
    from time import sleep
    import time
    


    if st.session_state.clicked:


        for i in range(2):
            a = url_w + str(i+1) 
            html = requests.get(url=str(a), verify=False)
            
            if html.status_code in [200]:
                st.write("The connection successful")
                connection = True          
                data = html.text
                soup = BeautifulSoup(data, 'lxml')
                tables.append(soup.select('table'))
            
                                           
            else:
                st.write(f"Status Code: {html.status_code}")
                st.write("Seems the entered url is not valid")
            pd.DataFrame(tables)
            time.sleep(1)                



    st.write("Note: This app searches for table tag in the html page, so it returns the table only if concern tags exists.")
    


# Main Container config
with st.container():
    st.markdown("#### Scraped Tables from the URL")
    success_b=False
    if tables:
        table_dict = {}
        div_dict = {}        
        header_b=True
        mode_b='w'
        for i,tab in enumerate(tables):
            table_dict[i+1] = pd.read_html(str(tab),header=0)[0]           
            table_dict[i+1].to_csv("houseprice.csv", index = False, header=header_b, sep=',', mode=mode_b)
            header_b=False
            mode_b='a'
            success_b=True
    if success_b:        
        df_2 = pd.read_csv('houseprice.csv', sep=',',engine='python')
        df_2
        country=df_2['제목'].str.split("[ ]", expand=True)[0]
        
        if country is not None:
        # contents=pd.DataFrame(country)
            country.value_counts().to_csv("national_count.csv",  header=True, sep=',', mode='w')
            
            df_3 = pd.read_csv('national_count.csv', sep=',',engine='python')
            
            df_3.columns = ['Country', 'Count']
            
            st.subheader("Pie Chart")
        

            # plt.figure(figsize = (3,2))
            # wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
            # plt.pie(df_3['Count'], labels=df_3['Country'],autopct='%.1f%%',startangle=90,wedgeprops=wedgeprops)
            # plt.legend()
            # st.pyplot( plt )
            # st.write("Powered by Streamlit")
            
            df_3.set_index('Country', inplace=True)

            # import plotly.express as px
            st.dataframe( df_3.head() )
            st.bar_chart(df_3)
            
