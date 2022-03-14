from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность', validators=[DataRequired()])
    collaborators = StringField('Коллеги', validators=[DataRequired()])
    team_leader = IntegerField('ID руководителя', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')

    submit = SubmitField('Добавить')
