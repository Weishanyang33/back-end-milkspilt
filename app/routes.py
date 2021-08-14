from flask import Blueprint, request, jsonify, make_response, session
from app import db
from app.models.author import Author
from app.models.question import Question
from app.models.answer import Answer
from app.models.question_vote import Question_Vote
from app.models.answer_vote import Answer_Vote
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()

####################### Blueprints ########################
questions_bp = Blueprint("questions", __name__, url_prefix="/questions")
answers_bp = Blueprint("answers", __name__, url_prefix="/answers")
login_bp = Blueprint("login", __name__)
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@login_bp.route("/login", methods=["POST"], strict_slashes=False)
def login():
    request_body = request.get_json()
    token = request_body["token"]
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    r = requests.Request()
    user = id_token.verify_oauth2_token(token,r,GOOGLE_CLIENT_ID)
    if user["email_verified"]:
        user_id = user["sub"]
        user_email = user["email"]
        picture = user["picture"]
        user_name = user["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    current_user = Author.query.filter_by(email=user_email).first()
    if not current_user:
        new_author = Author(username=user_name, email=user_email, avatar=picture)
        db.session.add(new_author)
        db.session.commit()
        current_user = Author.query.filter_by(email=user_email).first()
    session['user_id'] = current_user.author_id
    session['user_name'] = current_user.username
    session['user_avatar'] = current_user.avatar
    return {
            "current_user": current_user.to_json()
        }, 201
    
@login_bp.route("/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    session.clear()
    return {
        "message": "Logged out successfully"
    }, 200
    
# search
@login_bp.route("/search", methods=["POST"], strict_slashes=False)
def search():
    request_body = request.get_json()
    search_value = request_body["search_str"]
    search = f"%{search_value}%"
    search_results = Question.query.filter(Question.content.like(search) or Question.title.like(search)).all()
    if search_results:
        search_response = []
        for question in search_results:
            answers = Answer.query.filter_by(question_id=question.question_id).all()
            votes = Question_Vote.query.filter_by(question_id=question.question_id).all()
            answer_list = [answer.answer_id for answer in answers]
            vote_list = [vote for vote in votes]
            search_response.append(question.to_json(answer_list, vote_list))
        return jsonify(search_response), 200
    return jsonify({
            "error": 'No match found!'
        }), 404
    
    
# get query params based questions or all questions
@questions_bp.route("", methods=["GET"], strict_slashes=False)
def get_question():
    age_query = request.args.get("age")
    cat_query = request.args.get("category")
    if age_query and cat_query:
        questions = Question.query.filter_by(age_tag=age_query, cat_tag=cat_query).all()
    elif age_query:
        questions = Question.query.filter_by(age_tag=age_query).all()
    elif cat_query:
        questions = Question.query.filter_by(cat_tag=cat_query).all()
    else:
        questions = Question.query.all()
    question_response = []
    for question in questions:
        answers = Answer.query.filter_by(question_id=question.question_id).all()
        votes = Question_Vote.query.filter_by(question_id=question.question_id).all()
        answer_list = [answer.answer_id for answer in answers]
        vote_list = [vote for vote in votes]
        question_response.append(question.to_json(answer_list, vote_list))
    return jsonify(question_response), 200

# get question by id
@questions_bp.route("/<question_id>", methods=["GET"], strict_slashes=False)
def get_one_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return {"error": "Question not exist"}, 404
    answers = Answer.query.filter_by(question_id=question_id).all()
    answer_list = [answer.answer_id for answer in answers]
    votes = Question_Vote.query.filter_by(question_id=question.question_id).all()
    vote_list = [vote.author_id for vote in votes]
    question.views += 1
    question_response = question.to_json_detail(answer_list, vote_list)
    db.session.commit()
    return jsonify(question_response), 200

# post a question
@questions_bp.route("", methods=["POST"], strict_slashes=False)
def ask_question():
    # current_user = session['user']
    request_body = request.get_json()
    if all(request_body[key].strip() for key in ("title", "content", "age_tag", "cat_tag")):
        new_question = Question(title=request_body["title"],
                                content=request_body["content"],
                                age_tag=request_body["age_tag"],
                                cat_tag=request_body["cat_tag"],
                                author_id=request_body["author_id"],
                                username=request_body["username"],
                                avatar=request_body["avatar"]
                                )
        db.session.add(new_question)
        db.session.commit()
        return {
                "question": new_question.to_dict()
        }, 201
    else:
        return {"error": "Please include all the information needed to post a question."}, 400

# answer a question   
@questions_bp.route("/<question_id>/answer", methods=["POST"], strict_slashes=False)
def answer_question(question_id):
    question = Question.query.get(question_id)
    # current_user = session['user']
    if not question:
        return jsonify({
            "error": 'Question doesn\'t exist'
        }), 404
    request_body = request.get_json()
    if request_body["content"].strip():
        new_answer = Answer(content=request_body["content"],
                            question_id=question_id,
                            author_id=request_body["author_id"],
                            username=request_body["username"],
                            avatar=request_body["avatar"])
        db.session.add(new_answer)
        db.session.commit()
        return {
                "answer": new_answer.to_json()
        }, 201
    else:
        return {"error": "Invalid data"}, 400
    
# delete a question
@questions_bp.route("/<question_id>", methods=["DELETE"], strict_slashes=False)
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({
            "error": 'Question doesn\'t exist'
        }), 404
    db.session.delete(question)
    db.session.commit()
    return {
              "details": f"Question {question.question_id} {question.title} successfully deleted"
        }
    
# vote a question
@questions_bp.route("/<question_id>/vote", methods=["POST"], strict_slashes=False)
def vote_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({
            "error": 'Question doesn\'t exist'
        }), 404
    request_body = request.get_json()
    new_vote = Question_Vote(question_id=question_id, author_id=request_body["author_id"])
    db.session.add(new_vote)
    db.session.commit()
    return {
            "vote": new_vote.to_json()
    }, 201
    
    
# get an answer
@answers_bp.route("/<answer_id>",methods=["GET"], strict_slashes=False)
def get_one_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer:
        return jsonify(answer.to_json()),200
    else:
        return jsonify(None), 404

# get all answers or a list of answers 
@answers_bp.route("",methods=["GET"], strict_slashes=False)
def get_answers():
    params = request.args.get("params")
    answer_response = []
    if params and len(params) != 0:
        for param in params.split(','):
            if param.isnumeric():
                answer = Answer.query.get(param)
                answer_response.append(answer.to_json())
    elif len(params) == 0:
        answer_response = []
    else:
        answers = Answer.query.all()
        answer_response = [answer.to_json() for answer in answers]
    return jsonify(answer_response), 200
   
# get one author information 
@authors_bp.route("/<author_id>",methods=["GET"], strict_slashes=False)
def get_one_author(author_id):
    author = Author.query.get(author_id)
    if author:
        return jsonify(author.to_json(),200)
    else:
        return jsonify(None), 404
        

        
        

