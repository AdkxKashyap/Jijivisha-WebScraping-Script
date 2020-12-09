from environs import Env

from mongoengine import *


try:
    env=Env()
    env.read_env("config/env.env")
    mongo_url=env("MONGO_URL")
    
    connect("Jijivisha",host=mongo_url)
    
except Exception as err:
    print(err)

