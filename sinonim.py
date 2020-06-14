from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2VecModel
from pyspark.ml.feature import Word2Vec
from pprint import pprint
import re
import os
import datetime

PATH1 = '/home/vagrant/models/w2v'

spark = SparkSession \
    .builder \
    .appName("SimpleApplication") \
    .getOrCreate()

model = Word2VecModel.load(PATH1)


def get_synonyms(elements, count, model, spark_session):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame([
                (element.lower().split(" "),)], ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(
                transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append("Ничего не найдено")

    return result

with open("places.txt", "r") as myfile:
    data = myfile.readlines()
    for it in data:
        it = it.replace('\n', '')    

for it in data:
    it = str(it)
    print(it + " ".join(get_synonyms(it,5,model,spark)))

spark.stop()
