from app import db

class Question_Vote(db.Model):
    question_vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    question_id = db.Column(db.Integer,db.ForeignKey('question.question_id'))