from flask import Flask, render_template, make_response, jsonify
from flask_restful import Api
from werkzeug.utils import redirect
from data import db_session, jobs_api, users_resource

from data import db_session
from data.LoginForm import LoginForm
from data.job_form import JobForm
from data.jobs import Jobs
from data.user_form import RegisterForm
from data.users import User

from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

    app.run(port=5022)
    # user = User()
    # user.surname = 'Scott'
    # user.name = "Ridley"
    # user.age = 21
    # user.speciality = 'research engineer'
    # user.address = 'module_1'
    # user.email = "scott_chief@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.surname = 'Scott1'
    # user.name = "Ridley1"
    # user.age = 211
    # user.speciality = 'research engineer1'
    # user.address = 'module_2'
    # user.email = "scott_chief@mars.org1"
    # db_sess.add(user)
    # db_sess.commit()
    # app.run()
    #
    # user = User()
    # user.surname = 'Scott2'
    # user.name = "Ridley2"
    # user.age = 29
    # user.speciality = 'engineer'
    # user.address = 'module_1'
    # user.email = "scott@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    #
    # user = User()
    # user.surname = 'Niggeril'
    # user.name = "Lol1"
    # user.age = 32
    # user.speciality = 'space_engineer'
    # user.address = 'module_5'
    # user.email = "scott_goooohoh@mars.org"
    # db_sess.add(user)
    # db_sess.commit()
    # app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.name.data,
            age=form.name.data,
            position=form.name.data,
            Speciality=form.name.data,
            Address=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='ДОБАВЛЕНИЕ РАБОТЫ', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
