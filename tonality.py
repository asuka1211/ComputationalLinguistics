from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from pymongo import MongoClient

def getTonality(messages):
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    results = model.predict(messages, k=2)
    #вывод результата
    for message, sentiment in zip(messages, results):
        print(message, '->', sentiment)

if __name__ == "__main__":
    client = MongoClient("mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
    db = client.newsDB
    arr= list(db.Tomito.find({}, {"_id": 0, "text": 1}).limit(50))
    print("Отношения высказываний: ")
    for it in arr:
        tmp = [it.get("text")]
        getTonality(tmp)

