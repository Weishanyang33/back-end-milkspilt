from app import db

class Answer_Vote(db.Model):
    answer_vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    answer_id = db.Column(db.Integer,db.ForeignKey('answer.answer_id'))