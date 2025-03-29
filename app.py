import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# Title
st.title("📊 Social Media Analytics Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Data:")
    st.dataframe(df.head())
    
    # Check if expected columns exist
    if {'Likes', 'Comments', 'Shares', 'Post_Content'}.issubset(df.columns):
        
        # Engagement Metrics
        st.subheader("Engagement Metrics")
        likes = df['Likes'].sum()
        comments = df['Comments'].sum()
        shares = df['Shares'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Likes", likes)
        col2.metric("Total Comments", comments)
        col3.metric("Total Shares", shares)
        
        # Sentiment Analysis
        st.subheader("Sentiment Analysis of Posts")
        df['Sentiment'] = df['Post_Content'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df['Sentiment_Label'] = df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
        
        # Sentiment Visualization
        st.write("### Sentiment Distribution")
        sentiment_counts = df['Sentiment_Label'].value_counts()
        fig, ax = plt.subplots()
        sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        ax.set_title("Sentiment Analysis of Posts")
        st.pyplot(fig)
        
        # Engagement Trends
        st.subheader("Engagement Trends Over Time")
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df_grouped = df.groupby('Date').sum()
            st.line_chart(df_grouped[['Likes', 'Comments', 'Shares']])
        else:
            st.warning("No 'Date' column found. Add a Date column for trend analysis.")
        
    else:
        st.error("CSV file must contain 'Likes', 'Comments', 'Shares', and 'Post_Content' columns!")
