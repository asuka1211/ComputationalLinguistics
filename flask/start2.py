from flask import Flask, render_template, request, jsonify, make_response
import random
import time
import pymongo
import datetime


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Admin:12345@db1-9o4za.mongodb.net/db1?retryWrites=true&w=majority")
db1 = client.newsDB



res = db1.news.find().count()

app.config['JSON_AS_ASCII'] = False

all_items = db1.news.find().sort('date', pymongo.DESCENDING)

all_items2 = db1.Tonality.find().sort('_id', pymongo.DESCENDING)
all_items3 = db1.Word2vecv2.find().sort('_id', 1)



db = []  
db2 = []
db3 = []
posts = res  

quantity = 10  
for y in all_items2:
    message = y['message']
    tonality = y['tonality']
    db2.append(["".join(message), "".join(tonality)])

for x in all_items:

    news_title = x['title']
    news_discription = x['discription']
    news_link = x['link']
    news_img = x['img']
    news_date = x['date']
    
    news_date = datetime.datetime.strftime(news_date, "%Y %m %d")

    

    db.append(["".join(news_title), "".join(news_discription), "".join(news_link), "".join(news_img), "".join(news_date)])

for z in all_items3:
    name = z['name']
    sinonim = z['sinonim']
    db3.append(["".join(name), "".join(sinonim)])


@app.route("/")
def index():
    """ Route to render the HTML """
    return render_template("index.html")

@app.route("/tonality", methods=['GET', 'POST'])
def tomito():
    return render_template("tonality.html")

@app.route("/sinonim", methods=['GET', 'POST'])
def sinonim():
    return render_template("sinonim.html")

@app.route("/load")
def load():
    """ Route to return the posts """

    time.sleep(0.2) 

    if request.args:
        counter = int(request.args.get("c"))  

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
           
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
           
            res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res
@app.route("/load1")
def load1():
    """ Route to return the posts """

    time.sleep(0.2)  

    if request.args:
        counter = int(request.args.get("c"))  

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            
            res = make_response(jsonify(db2[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            
            res = make_response(jsonify(db2[counter: counter + quantity]), 200)
    return res

@app.route("/load2")
def load2():
    """ Route to return the posts """

    time.sleep(0.2)  

    if request.args:
        counter = int(request.args.get("c"))  

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            
            res = make_response(jsonify(db3[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            
            res = make_response(jsonify(db3[counter: counter + quantity]), 200)
    return res
if __name__ == '__main__':
    app.run(debug=True)