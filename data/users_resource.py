from flask_restful import reqparse, abort, Api, Resource
from data import db_session
def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"Jobs {user_id} not found")