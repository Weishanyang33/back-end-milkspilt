from flask import Blueprint, request, jsonify, make_response, session
from app import db
from app.models.author import Author
from app.models.question import Question
from app.models.answer import Answer
from app.models.question_vote import Question_Vote
from app.models.answer_vote import Answer_Vote
import os
from dotenv import load_dotenv

load_dotenv()

####################### Blueprints ########################
questions_bp = Blueprint("questions", __name__, url_prefix="/questions")




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
    for question in questions:
        answers = Answer.query.filter_by(question_id=question.question_id).all()
        votes = Question_Vote.query.filter_by(question_id=question.question_id).all()
        answer_list = [answer for answer in answers]
        vote_list = [vote for vote in votes]
    question_response = [question.to_json(answer_list, vote_list) for question in questions]
    return jsonify(question_response), 200

# post a question
@questions_bp.route("", methods=["POST"], strict_slashes=False)
def ask_question():
    # current_user = session['user']
    request_body = request.get_json()
    if all(key in request_body for key in ("title", "content", "age_tag", "cat_tag")):
        new_question = Question(title=request_body["title"],
                                content=request_body["content"],
                                age_tag=request_body["age_tag"],
                                cat_tag=request_body["cat_tag"],
                                author_id=request_body["author_id"])
        db.session.add(new_question)
        db.session.commit()
        return {
                "question": new_question.to_json()
        }, 201
    else:
        return {"error": "Invalid data"}, 400
