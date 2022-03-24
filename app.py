from flask import Flask, render_template, request, redirect, url_for
import csv
app = Flask(__name__)

DINO_PATH = app.root_path + '/dinosaurs.csv'
TOP_10 = app.root_path + '/top10.csv'
DINO_KEYS = ['slug', 'name', 'description', 'image', 'image-credit', 'source-url', 'source-credit']

with open(DINO_PATH, 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinosaurs = {row['slug']:{'name':row['name'],'description':row['description'],'image':row['image'],'image-credit':row['image-credit'],'source-url':row['source-url'],'source-credit':row['source-credit']} for row in data}

def get_dinos():
    try:
        with open(DINO_PATH, 'r') as csvfile:
            data = csv.DictReader(csvfile)
            dinosaurs = {}
            for dino in data:
                dinosaurs[dino['slug']] = dino
    except Exception as e:
        print(e)
    return dinosaurs

def set_dinos(dinosaurs):
    try:
        with open(DINO_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=DINO_KEYS)
            writer.writeheader()
            for dino in dinosaurs.values():
                writer.writerow(dino)
    except Exception as err:
        print(err)

@app.route('/')
@app.route('/dino')
@app.route('/dino/<dino>')
def index(dino=None):
    print(dino)
    if dino and dino in dinosaurs.keys():
        dinosaur = dinosaurs[dino]
        return render_template('dino.html', dinosaur=dinosaur)
    else:
        return render_template('index.html', dinosaurs=dinosaurs)



with open('top10.csv', 'r') as csvfile:
    data = csv.DictReader(csvfile)
    dinos = {row['rank']:{'name':row['name'], 'votes':row['votes']} for row in data}
    
@app.route('/favorite')
def favorite():
    return render_template('favorite.html', dinos=dinos)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add-dino', methods=['GET', 'POST'])
def add_dino():
    if request.method == 'POST':
        dinosaurs = get_dinos()
        newDino = []

        newDino['slug'] = request.form['slug']
        newDino['name'] = request.form['name']
        newDino['description'] = request.form['description']
        newDino['image'] = request.form['image']
        newDino['image-credit'] = request.form['image-credit']
        newDino['source-url'] = request.form['source-url']
        newDino['source-credit'] = request.form['source-credit']

        dinosaurs[request.form['name']] = newDino
        set_dinos(dinosaurs)

        return redirect(url_for('index'))
    else:
       return render_template('add_dino.html')

@app.route('/dino-quiz', methods=['GET', 'POST'])
@app.route('/quiz-results', methods=['GET', 'POST'])
def dino_quiz():
   # if POST request received (form submitted)
    if request.method == 'POST':
        quizGuesses = {}
        quizGuesses['q1'] = request.form['continents']
        quizGuesses['q2'] = request.form.get('eggs', 'false')
        quizGuesses['q3'] = request.form.getlist('herbivores')
        quizGuesses['q4'] = request.form['extinct']

        #quizGuesses['q3'] == quizGuesses['q3'].join()
        
        quizAnswers = {
            'q1' : 'North America',
            'q2' : 'true',
            'q3' : ['stego', 'tri'],
            'q4' : '66'
       }
           
        print(quizGuesses)
       
        return render_template('quiz-results.html', quizGuesses = quizGuesses, quizAnswers=quizAnswers)

    else:   
        return render_template('dino-quiz.html')
