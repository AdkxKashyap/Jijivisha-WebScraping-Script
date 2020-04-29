import datetime
from mongoengine import *


class GlobalNews(Document):
  
    published = StringField(default=str(datetime.datetime.now()))
    news_data=ListField(required=True)