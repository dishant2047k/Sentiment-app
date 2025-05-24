import streamlit as st
from review_scraper import scrape_reviews
from sentiment_model import analyze_sentiment

st.title("🛍️ Product Review Sentiment Analyzer")

product_link = st.text_input("Enter Product Link:")

if st.button("Analyze"):
    if not product_link:
        st.warning("Please enter a valid product link.")
    else:
        reviews = scrape_reviews(product_link)
        st.write("### Sentiment Analysis Results")
        for i, review in enumerate(reviews):
            sentiment = analyze_sentiment(review)
            st.write(f"**Review {i+1}:** {review}")
            st.write(f"Sentiment: `{sentiment}`")
            st.markdown("---")
