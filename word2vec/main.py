import pymongo
import json
import re
from pymongo import MongoClient
import os
import datetime
import glob
import app
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer 
from pyspark.ml.feature import StopWordsRemover 
from pyspark.ml.feature import CountVectorizer 
from pyspark.ml.feature import IDF 
from pyspark.ml.feature import Word2VecModel
from pyspark.ml.feature import Word2Vec 
from pathlib import Path

client = MongoClient(
    "mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
db = client.newsDB

arr = list(db.news.find({}, {"_id": 0, "discription": 1}))
print(len(arr))

PATH = "/home/vagrant/samples/"
if not os.path.exists(PATH):
    os.makedirs(PATH)

files = glob.glob('/home/vagrant/samples/*.txt')
for f in files:
    os.remove(f)

d = 0
name = PATH + "news" + str(d)
i = 0
f = open(name + ".txt", "w")
for it in arr:
    if i == 500:
        f.close()
        name = PATH  + "news" + str(d)
        f = open(name + ".txt", "w")
        i = 0
        d+=1
    i+=1
    f.write(json.dumps(it.get("discription"), ensure_ascii=False))
f.close()

app.start()