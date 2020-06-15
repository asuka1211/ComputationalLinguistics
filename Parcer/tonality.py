from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
result = []
def getTonality(messages):
    
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(messages, k=2)
    #вывод результата
    for message, sentiment in zip(messages, results):
        string = str(sentiment)
        
        
        client.newsDB.Tonality.insert_one({
           'message': message,
           'tonality': string
            })
    

