# starting with Flask Jinja and templates
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# databases

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(25), nullable=False, default='N/A')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)


@app.route('/01')
def hello():
    return render_template("index.html")


# @app.route('/', methods=['GET', 'POST'])
# def limit():
#     return "This will limit to only get or only post"


# passing and accessing data in html
# data = [
#     {
#         'title': 'What is Lorem Ipsum?',
#         'author': 'Yakoov',
#         'content': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
#     },

#     {
#         'title': 'Why do we use it?',
#         'content': "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."

#     }
# ]


@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        newPost = BlogPost(
            title=post_title, content=post_content, author=post_author)

        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts')
    else:
        data = BlogPost.query.order_by(BlogPost.date).all()
        return render_template('post.html', posts=data)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):

    post=BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html' , post=post)

if __name__ == "__main__":
    app.run(debug = True)
