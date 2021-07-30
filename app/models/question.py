from app import db
from datetime import datetime

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    age_tag = db.Column(db.String)
    cat_tag = db.Column(db.String)
    views = db.Column(db.Integer)
    date_asked = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    question_votes = db.relationship('Question_Vote', backref = 'question', lazy = 'dynamic')
    
    
    def to_dict(self):
        return {
            "question_id": self.question_id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "age": self.age_tag,
            "category": self.cat_tag,
            "views": self.views,
            "date_asked": self.date_asked
        }
        
    def to_json(self,answer,vote):
        return {
            "question_id": self.question_id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "age": self.age_tag,
            "category": self.cat_tag,
            "views": self.views,
            "date_asked": self.date_asked,
            "answer": answer,
            "vote": len(vote)
        }
        
    def to_json_detail(self,answer,vote):
        return {
            "question_id": self.question_id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "age": self.age_tag,
            "category": self.cat_tag,
            "views": self.views,
            "date_asked": self.date_asked,
            "answer": answer,
            "vote": vote
        }
