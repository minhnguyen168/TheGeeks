import pandas as pd
import uuid
from datetime import date, timedelta, datetime
from newsapi import NewsApiClient


class News():

    def get_financial_news(self):
        # Get news of today
        current_date = date.today()
        final_news = []
        news_api_key = "0387fd5051164389965c08f7bc4274d8"
        targeted_keywords = [
            "Singtel",
            "Singapore Airlines",
        ]
        # Get news data from News API
        for keyword in targeted_keywords:
            newsapi = NewsApiClient(api_key=news_api_key)
            articles = newsapi.get_everything(
                q=keyword,
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
        return news_df
    


