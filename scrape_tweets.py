import pandas as pd
import streamlit as st
import time
import datetime 

from twitter_scraper import scrape_tweets, store_tweets_in_mongodb

# main app function
def app():
    # display app title and input fields
    st.title('Twitter Scraper')
    keyword = st.text_input('Enter a keyword or hashtag to search for:')
    max_tweets = st.number_input('Enter the maximum number of tweets to scrape:', min_value=1, max_value=10000, value=100)
    end_date = st.date_input("Select date:",max_value=datetime.date.today())
    start_date =end_date - datetime.timedelta(days=100)
    
    # add session state and scrape button
    if "scrape tweets" not in st.session_state:
        st.session_state["scrape tweets"] = False        
    if st.button("Scrape Tweets"):
        st.session_state["scrape tweets"] = not st.session_state["scrape tweets"]
   
    # check if scrape button is pressed and scrape tweets    
    if st.session_state["scrape tweets"]:
        tweets = scrape_tweets(keyword, start_date, end_date, max_tweets)
        df = pd.DataFrame(tweets)
        data_dict = df.to_dict("records")
        csv = df.to_csv(index=False)
        json=df.to_json()
        
        # add tabs to display data in csv and json formats
        if st.sidebar.button("View data"):
            tab1, tab2 = st.tabs(["csv", "json"])
            with tab1:
                st.dataframe(df)
            with tab2:  
                st.json({"Scraped Word" : keyword,
                             "Scraped Date" : str(datetime.date.today()),
                             "Scraped Data":data_dict})
        # add button to store scraped data in MongoDB
        if st.sidebar.button('Store in MongoDB'):
            store_tweets_in_mongodb(keyword,data_dict)
            # add a spinner to show progress
            with st.spinner('Wait for it...'):
                time.sleep(5)
            st.success('Successfully Uploaded to Database!', icon="✅")
        # add download buttons to download data as csv or json files
        if st.sidebar.download_button('Download data asCSV', data=csv, file_name=f'{keyword}_tweets.csv', mime='text/csv'):
            with st.spinner('Wait for it...'):
                time.sleep(5)
            st.success("Your csv file succesfully Downloaded",icon="✅")
        if st.sidebar.download_button(label="Download data as json",data=json,file_name=f'{keyword}_Tweets.json',mime='json'):
            with st.spinner('Wait for it...'):
                time.sleep(5)
            st.success("Your json file succesfully Downloaded",icon="✅")
      
app()

