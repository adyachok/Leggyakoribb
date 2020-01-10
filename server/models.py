import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)


class WordsList(db.Model):
    __tablename__ = 'words_lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(250))
    words = db.relationship("Word", back_populates="words_list")
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    hu_szo = db.Column(db.String(250), nullable=False)
    ua_szo = db.Column(db.String(250), nullable=False)
    words_list_id = db.Column(db.Integer, db.ForeignKey('words_lists.id'))
    words_list = db.relationship("WordsList", back_populates="words")


class WordLearningProgress(db.Model):
    __tablename__ = 'words_learning_progress'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), primary_key=True)
    words_list_id = db.Column(db.Integer, db.ForeignKey(WordsList.id),
                              primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', foreign_keys='WordLearningProgress.user_id')
    word = db.relationship('Word', foreign_keys='WordLearningProgress.word_id')
    words_list = db.relationship(
        'WordsList', foreign_keys='WordLearningProgress.words_list_id')