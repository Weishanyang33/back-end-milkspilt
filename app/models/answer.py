from app import db
from datetime import datetime

class Answer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String)
    date_answered = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    
    def to_json(self):
        return {
            "answer_id": self.answer_id,
            "content": self.content,
            "date_answered": self.date_answered,
            "author_id": self.author_id,
            "question_id": self.question_id
        }