from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Length, DataRequired


class AlbumForm(FlaskForm):
    photo = FileField("photo", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])])
    description = TextAreaField("图片的描述", validators=[DataRequired(), Length(max=256)])
    uploader = StringField("上传者", validators=[DataRequired(), Length(max=10)])
    submit = SubmitField("提交")

