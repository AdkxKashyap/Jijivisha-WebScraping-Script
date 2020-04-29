import datetime
from mongoengine import *


class IndiaCovidData(Document):
  
    published = StringField(default=str(datetime.datetime.now()))
    covid_data=ListField(required=True)