import flask
from flask import jsonify, request

from main import app
from . import db_session, jobs
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)

from data import db_session, jobs_api


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    print('OK')
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'team_leader',
                                    'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify ({'jobs': jobs.to_dict(only=('id', 'job', 'team_leader',
                                    'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished'))})

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finised=request.json['is_finished']
    )
    if db_sess.query(Jobs).get(jobs.id):
        return jsonify({'error': 'id already exist'})
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run()
