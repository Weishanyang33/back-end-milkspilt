from app import db

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique = True)
    email = db.Column(db.String, unique = True)
    avatar = db.Column(db.String)
    questions = db.relationship('Question', backref = 'author', lazy = 'dynamic')
    answers = db.relationship('Answer', backref='author', lazy='dynamic')
    question_votes = db.relationship('Question_Vote', backref = 'author', lazy = 'dynamic')
    answer_votes = db.relationship('Answer_Vote', backref = 'author', lazy = 'dynamic')
    
    def to_json(self):
        return {
            "author_id": self.author_id,
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar
        }