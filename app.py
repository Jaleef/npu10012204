from datetime import date, datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from forms.album_form import AlbumForm
from forms.blog_form import BlogForm
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['BLOG_UPLOAD_FOLDER'] = 'static/blogImg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(50), index=True, unique=False)
    description = db.Column(db.String(100), index=True, unique=False)
    date = db.Column(db.Date, index=True, unique=False)
    uploader = db.Column(db.String(10), index=True, unique=False)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), index=True, unique=False, default="无标题")
    text = db.Column(db.Text, index=True, unique=False)
    date = db.Column(db.Date, index=True, unique=False)
    uploader = db.Column(db.String(10), index=True, unique=False, default="匿名")


#------------------------------------
if os.path.exists("instance/myDB.db"):
    os.remove("instance/myDB.db")

with app.app_context():
    db.create_all()
    photo1 = Photo(id=1, filename="班级合照.png", description="大二新班级的第一次班会", date=datetime.strptime("2023-09-10", "%Y-%m-%d"), uploader="闫佳乐")
    db.session.add(photo1)

    post1 = Blog(id=1, title="这是标题", text="## 这是文章内容", date=datetime.strptime("2024-01-06", "%Y-%m-%d"), uploader="闫佳乐")
    db.session.add(post1)
    db.session.commit()
#-----------------------------------


@app.route('/')
def index():
    return render_template("index.html", PageName="主页")


@app.route('/home')
def home():
    posts = Blog.query.order_by(Blog.date.desc()).all()
    return render_template("home.html", PageName="主页", posts=posts)


@app.route('/home/<int:post_id>')
def post(post_id):
    post = Blog.query.get_or_404(post_id)
    return render_template("post.html", PageName="Blog", post=post)


@app.route('/home/editor', methods=['GET', 'POST'])
def edit_post():
    if request.method == 'GET':
        return render_template("editor.html", PageName="Markdown")
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        uploader = request.form.get('uploader')
        load_date = date.today()

        if not title:
            flash("请一定输入标题！", 'error')
            return redirect(url_for('edit_post'))

        post = Blog(title=title, text=text, date=load_date, uploader=uploader)
        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('home'))


@app.route('/home/editor/imgUpload', methods=['POST'])
def imgUpload():
    try:
        photo = request.files.get('editormd-image-file')
        photo_name = secure_filename(photo.filename)
        ext = photo_name.rsplit('.')[-1]
        # 生成一个uuid作为文件名
        new_name = str(uuid.uuid4()) + "." + ext
        photo_path = os.path.join(app.config["BLOG_UPLOAD_FOLDER"], new_name)
        photo.save(photo_path)
        return {
            'success': 1,
            'message': '上传成功!',
            'url': "/" + photo_path
        }
    except Exception:
        return {
            'success': 0,
            'message': '上传失败'
        }


@app.route('/album', methods=['GET'])
def album():
    album = Photo.query.all()
    return render_template("album.html", PageName="相册", album=album)


@app.route('/album/upload', methods=['GET', 'POST'])
def uploadAlbum():
    albumForm = AlbumForm()
    if albumForm.validate_on_submit():
        photo = request.files.get("photo")
        photo_name = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))
        new_photo = Photo(filename=photo_name, description=request.form.get("图片的描述"), date=date.today(), uploader=request.form.get("上传者"))
        db.session.add(new_photo)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('album'))

    return render_template("uploadPhoto.html", PageName="上传图片", albumForm=albumForm)


@app.route('/album/<string:filename>')
def checkPhoto(filename):
    print(filename)
    return render_template("photo.html", filename=filename)


@app.route('/tools/<tool>')
def tools(tool):

    return render_template("")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("404.html"), 500


if __name__ == "__main__":
    app.run()
