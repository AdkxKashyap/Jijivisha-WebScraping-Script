import datetime
from mongoengine import *


class MythBusters(Document):
  
    published = StringField(default=str(datetime.datetime.now()))
    myth_busters_data=ListField(required=True)