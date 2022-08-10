import pandas as pd
import uuid
import re
import os
from datetime import date, timedelta, datetime
from app.models import (Insight)
from app import db

# News API and Summarisation
from newsapi import NewsApiClient
from gensim.summarization import summarize

# LDA Model
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import CoherenceModel

# Stop words
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Wordcloud for topic modelling
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors



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
    

    def get_news_summary(self, filtered_news_df):
        news_summary = ""
        if len(filtered_news_df) > 0:
            combined_text = '. '.join(map(str, filtered_news_df["news_title"].tolist()))
            combined_text = combined_text.replace("..", ".")
            to_replace = ["[…]", "<ol>", "<li>", "</li>", "</ol>", "<ul>", "</ul>", "..."]
            for text in to_replace:
                combined_text = combined_text.replace(text, "")
            try:
                if len(filtered_news_df) > 15:
                    news_summary = summarize(combined_text, word_count=200)
                else:
                    news_summary = summarize(combined_text, ratio=0.2)
            except:
                news_summary = ""
        return news_summary

    def remove_stopwords(self, text, stopwords_list, lemma):
        string = ""
        # Remove meaningless words for LDA
        # Common terms can also be removed
        common_terms = ["business", "finance", "financial", "investment", "planning"]
        text = simple_preprocess(str(text), deacc=True)
        for word in text.split():
            if word not in stopwords_list and word not in common_terms:
                string+=lemma.lemmatize(word)+" "
        return string

    def topic_modelling(self, news_df, num_topics):
        lemma=WordNetLemmatizer()
        # Remove meaningless words and common terms before LDA
        stopwords_list=stopwords.words('english')
        common_terms = [
            "business", "finance", "financial", "investment", "planning", "li", "latest",
            "best", "year", "inc", "today", "july", "pm"]
        stopwords_list.extend(common_terms)

        news_words_list = []
        for index, row in news_df.iterrows():
            string = ""
            words_list = simple_preprocess(str(row["news_description"]), deacc=True)
            for word in words_list:
                if word not in stopwords_list and word not in common_terms:
                    string += lemma.lemmatize(word) + " " 
            words_list = string.split()
            news_words_list.append(words_list)
        id2word = corpora.Dictionary(news_words_list)
        corpus = [id2word.doc2bow(x) for x in news_words_list]

        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='symmetric',
                                           iterations=100,
                                           per_word_topics=True)

        topics = lda_model.show_topics(formatted=False)
        return topics
    
    def topics_wordcloud(self, topics):
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
        for i, topic in enumerate(topics, start=1):
            wc = WordCloud(stopwords=set(STOPWORDS),
                            background_color='white',
                            width=2500,
                            height=1800,
                            max_words=10,
                            colormap='tab10',
                            color_func=lambda *args, **kwargs: cols[i],
                            prefer_horizontal=1.0)
            topic_words = dict(topics[i-1][1])
            wc.generate_from_frequencies(topic_words, max_font_size=300)
            img_folder_path = os.path.join('app', 'static', 'images')
            wc.to_file(os.path.join(img_folder_path, "wordcloud_{}.jpg".format(i)))
            
