from flask import Flask, render_template
import csv
app = Flask(__name__)



with open('dinosaurs.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinosaurs = {row['slug']:{'name':row['name'],'description':row['description'],'image':row['image'],'image-credit':row['image-credit'],'source-url':row['source-url'],'source-credit':row['source-credit']} for row in data}

@app.route('/')
def index():
    return render_template('index.html', dinosaurs=dinosaurs)


with open('top10.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinos = {row['rank']:{'name':row['name'], 'votes':row['votes']} for row in data}
    
@app.route('/favorite')
def favorite():
    return render_template('favorite.html', dinos=dinos)



# def hello_world():
#     return 'Hello World!'
