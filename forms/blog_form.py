from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class BlogForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('内容', validators=[DataRequired()])
    uploader = StringField('上传者', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('提交')

