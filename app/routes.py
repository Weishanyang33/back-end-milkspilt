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

@questions_bp.route("", methods=["GET"], strict_slashes=False)
def get_question():
    question_query = request.args.get("age")
    questions = Question.query.all()
    question_response = []
    for question in questions: 
        question_response.append(question.to_json())
    return jsonify(question_response), 200


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
