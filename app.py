from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer 
from pyspark.ml.feature import StopWordsRemover 
from pyspark.ml.feature import CountVectorizer 
from pyspark.ml.feature import IDF 
from pyspark.ml.feature import Word2VecModel
from pyspark.ml.feature import Word2Vec 
import re
import string
import os
import datetime

PATH1 = '/home/vagrant/models/w2v'

def remove_punctuation(text):
    """
    Удаление пунктуации из текста
    """
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_linebreaks(text):
    """
    Удаление разрыва строк из текста
    """
    return text.replace("\\n", "")

def get_only_words(tokens):
    """
    Получение списка токенов, содержащих только слова
    """
    return list(filter(lambda x: re.match('[а-яА-Я]+', x), tokens))

def start():

    spark = SparkSession \
        .builder \
        .appName("SimpleApplication") \
        .getOrCreate()

    input_file = spark.sparkContext.textFile('/home/vagrant/part2kursach/samples/*.txt')

    prepared = input_file.map(lambda x: ([x])).map(lambda x: (x[0],remove_punctuation(x[0]))).map(lambda x: (x[0],remove_linebreaks(x[0])))
    df = prepared.toDF()
    prepared_df = df.selectExpr('_2 as text') 
    df.show() 

    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)
    words.show() 

    filtered_words_data = words.rdd.map(lambda x: (x[0], get_only_words(x[1])))
    filtered_df = filtered_words_data.toDF().selectExpr('_1 as text', '_2 as words')

    stop_words = StopWordsRemover.loadDefaultStopWords('russian') 
    remover = StopWordsRemover(inputCol="words",
    outputCol="filtered", stopWords=stop_words)
    filtered = remover.transform(filtered_df)
    filtered.show() 

    vectorizer = CountVectorizer(inputCol="filtered",
    outputCol="raw_features").fit(filtered)
    featurized_data = vectorizer.transform(filtered)
    featurized_data.cache() 
    featurized_data.show()

    idf = IDF(inputCol='raw_features', outputCol='features')
    idf_model = idf.fit(featurized_data)
    rescaled_data = idf_model.transform(featurized_data) 
    rescaled_data.show()

    word2Vec = Word2Vec(vectorSize=50, inputCol='words', outputCol='result', minCount=2)
    model = word2Vec.fit(words)
    w2v_df = model.transform(words) 

    today = datetime.datetime.today() 
    model_name = today.strftime("/home/vagrant/models/w2v") 
    model.write().overwrite().save(model_name) 

    spark.stop()