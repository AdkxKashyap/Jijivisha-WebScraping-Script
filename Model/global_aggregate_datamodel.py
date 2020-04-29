import datetime
from mongoengine import *

class AggregateGlobalData(Document):
    published=StringField(default=str(datetime.datetime.now()))
    agg_covid_data=DictField(required=True)