import subprocess
import pymongo
import json
import re
from pymongo import MongoClient
import tonality

def start(text):
    
    client = MongoClient(
        "mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
    db = client.newsDB

    

    
    toParse = text.encode('utf-8', "strict")
    with subprocess.Popen(["tomita-parser", "config.proto"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        stdout, stderr = proc.communicate(toParse)
        stdout_formatted = stdout.decode("utf-8", "strict")
        result = re.search(r'Name = .*',stdout_formatted)
        if(result != None):
            tonality.getTonality([result.group(0)[7:]])
            result = { "text": result.group(0)[7:]}
            print(result)
            db.Tomito.insert_one(result)


