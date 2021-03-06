import datetime
import os
import logging
import random

from flask import Flask, escape, request, jsonify, render_template, redirect, \
    session, abort
from flask_cors import CORS
from sqlalchemy import and_

from server.config import Config
from server.models import db, WordLearningProgress, User, Word, WordsList

app = Flask(__name__)
logger = logging.getLogger(__name__)


CORS(app,
     allow_headers=[
         "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True)

CONFIG = Config(app, db)

if os.getenv('RECREATE_DB') in ['True', 'true']:
    CONFIG.db.drop_all(app=app)
    CONFIG.db.create_all(app=app)


@app.route('/list/<words_list_id>', methods=['GET'])
def hello(words_list_id):
    email = session.get('user')
    if not email:
        return redirect('/login', code=302)
    user = User.query.filter(User.email == email).first()
    if not user:
        return redirect('/login', code=302)
    next_from = request.args.get('next_from')
    # words_list_id = request.args.get('words_list')
    result = []
    progress = []
    if next_from and words_list_id:
        try:
            next_from = int(next_from)
            result = Word.query.filter(and_(
                Word.id > next_from, Word.words_list_id==words_list_id)) \
                .limit(100).all()
            ids = [word.id for word in result]
            progress = WordLearningProgress.query \
                .filter(and_(WordLearningProgress.word_id.in_(ids),
                             WordLearningProgress.user_id==user.id)).all()
        except ValueError:
            print(f'Value error for {next_from}')
    elif words_list_id:
        result = Word.query.filter(and_(
            Word.words_list_id == words_list_id)).limit(100).all()
        ids = [word.id for word in result]
        progress = WordLearningProgress.query \
            .filter(and_(WordLearningProgress.word_id.in_(ids),
                         WordLearningProgress.user_id==user.id)).all()
    progress = {item.word_id: item.date.strftime("%b %d %Y %H:%M:%S")
                for item in progress}
    return render_template('index.html', result=result, progress=progress)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email==email).first()
        if user and user.password == password:
            # TODO: check later
            session['user'] = email
            return redirect("/", code=302)
    return render_template('login.html')


@app.route('/sync', methods=['POST'])
def sync():
    data = request.json
    email = session.get('user')
    if not email:
        return abort(404)
    user = User.query.filter(User.email==email).first()
    if not user:
        return abort(404)
    words_list_id = data.get('words_list_id')
    words_data = data.get('learned_words')
    for id_val, time_val in words_data.items():
        try:
            id_val = int(id_val)
            time_val = int(time_val)
            word_progres = WordLearningProgress()
            word_progres.word_id = id_val
            word_progres.date = datetime.datetime.utcfromtimestamp(time_val)
            word_progres.user_id = user.id
            word_progres.words_list_id = words_list_id
            CONFIG.db.session.add(word_progres)
            CONFIG.db.session.commit()
        except ValueError as e:
            print(e)
    return jsonify(list(words_data.keys()))


@app.route('/', methods=['GET'])
def get_words_lists():
    email = session.get('user')
    if not email:
        return redirect('/login', code=302)
    user = User.query.filter(User.email == email).first()
    if not user:
        return redirect('/login', code=302)
    words_lists = WordsList.query.all()
    return render_template('words-lists.html', words_lists=words_lists)


@app.route('/cards', methods=['GET'])
def get_cards():
    email = session.get('user')
    if not email:
        return redirect('/login', code=302)
    learned_words = WordLearningProgress.query.limit(20).all()
    all_words = Word.query.with_entities(Word.ua_szo).limit(80).all()
    all_words = [result[0] for result in all_words]
    quest_words = []
    for progress in learned_words:
        quest_word = {}
        quest_word['foreign_name'] = progress.word.hu_szo
        words = dict()
        # Have to add the right translation option
        true_translation = progress.word.ua_szo
        words[true_translation] = True
        while True:
            if len(words) == 4:
                break
            rand = random.randint(0, len(all_words) - 1)
            false_translation = all_words[rand]
            if false_translation == true_translation:
                continue
            else:
                words[false_translation] = False
        quest_word['translations'] = words
        shuffled_translations = list(words.keys())
        random.shuffle(shuffled_translations)
        quest_word['shuffled_translations'] = shuffled_translations
        quest_words.append(quest_word)
    return render_template('cards.html', quest_words=quest_words)


app.config['env_config'] = CONFIG
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
# app.register_blueprint(tasks, url_prefix='/task')
app.run('0.0.0.0', port=CONFIG.SERVICE_PORT, debug=CONFIG.SERVICE_DEBUG)
