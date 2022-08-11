import pandas as pd
import uuid
import re
from datetime import date, timedelta, datetime
from newsapi import NewsApiClient
from app.models import (Insight)
from app import db
#from gensim.summarization import summarize


class News():

    def get_financial_news(self):
        # Get news of today
        current_date = date.today()
        final_news = []
        news_api_key = "a14e56d586834fad9edf5cf23ad91032"
        # Get news data from News API
        newsapi = NewsApiClient(api_key=news_api_key)
        articles = newsapi.get_everything(
            q="finance OR business",
            from_param = current_date.isoformat(), 
            to = current_date.isoformat(), 
            language="en",
            sort_by="publishedAt")
        
        # Processing of news text data to form pandas dataframe
        for article in articles['articles']:
            description = "{}. {}".format(article['description'], article['title'])
            published_date = article['publishedAt'].replace('T', ' ').replace('Z', '')
            news_id = str(uuid.uuid4()).replace('-','')
            final_news.append((news_id, published_date, article['title'], description, article['content'], article['url']))

        news_df = pd.DataFrame(final_news, columns=['News_ID', 'Published_Date', 'News_Title', 'News_Description', 'News_Content', 'News_URL'])
        news_df['Published_Date'] = pd.to_datetime(news_df['Published_Date']).dt.date
        news_df['Published_Date'] = news_df['Published_Date'].apply(lambda x: int(x.strftime("%Y%m%d")))

        for index, row in news_df.iterrows():
            news = Insight(news_id=row['News_ID'], published_date=row['Published_Date'], news_title=row['News_Title'], news_description=row['News_Description'], news_content=row['News_Content'], news_url=row['News_URL'])
            db.session.add(news)
            db.session.commit()
        return news_df
    

    # def get_news_summary(self, filtered_news_df):
    #     news_summary = ""
    #     if len(filtered_news_df) > 0:
    #         combined_text = '. '.join(map(str, filtered_news_df["news_title"].tolist()))
    #         combined_text = combined_text.replace("..", ".")
    #         to_replace = ["[…]", "<ol>", "<li>", "</li>", "</ol>", "<ul>", "</ul>", "..."]
    #         for text in to_replace:
    #             combined_text = combined_text.replace(text, "")
    #         try:
    #             if len(filtered_news_df) > 15:
    #                 news_summary = summarize(combined_text, word_count=200)
    #             else:
    #                 news_summary = summarize(combined_text, ratio=0.2)
    #         except:
    #             news_summary = ""
    #     return news_summary