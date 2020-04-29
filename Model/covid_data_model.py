import datetime
from mongoengine import *


class GlobalData(Document):
  
    published = StringField(default=str(datetime.datetime.now()))
    covid_data=ListField(required=True)