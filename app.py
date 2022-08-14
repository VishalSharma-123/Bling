from email.mime import image
import re
from termios import B0
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.Date, nullable=False,
                            default=datetime.now().date())
    image = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return 'Blog Post' + str(self.id)

# db.create_all()


@app.route('/')
def index():
    all_posts = BlogPost.query.all()

    return render_template('index.html', posts=all_posts)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        author_content = request.form['author']
        f = request.files['image']

        # when saving the file
        t = datetime.now()
        ext = f.filename.split(".")[-1]
        print(os.getcwd())
        fileName = secure_filename(t.strftime("%m-%d-%Y, %H:%M:%S")+"."+ext)
        f.save(os.path.join(os.getcwd(),
               'static/images/posts', fileName))
        new_post = BlogPost(
            title=post_title,
            content=post_content,
            author=author_content,
            image=fileName)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts=all_posts)


@ app.route('/post/<id>')
def post(id):
    posts = BlogPost.query.all()
    post = BlogPost.query.get(id)
    return render_template("post.html", post=post, posts=posts)


@ app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return "Hello World " + name + str(id)


@ app.route('/onlyget', methods=['get'])
def get_req():
    return 'You can only get this web page'


@ app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@ app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        f = request.files['image']

        # when saving the file
        t = datetime.now()
        ext = f.filename.split(".")[-1]
        # print(os.getcwd())
        fileName = secure_filename(t.strftime("%m-%d-%Y, %H:%M:%S")+"."+ext)
        f.save(os.path.join(os.getcwd(),
               'static/images/posts', fileName))

        # post.image = os.path.join(os.getcwd(),
        #                           'static/images/posts/'+fileName)
        post.image = fileName
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)
