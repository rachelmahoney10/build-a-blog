from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text(), unique=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def route():
    return redirect('/blog')


@app.route('/blog', methods=['GET'])
def index():
    posts = blog.query.order_by('id DESC').all()
    blogid = request.args.get("id")

    if blogid != None:
        blogpost = blog.query.filter_by(id=blogid).first()
        return render_template('blog.html', blogid=blogpost.id, title=blogpost.title, body=blogpost.body)

    return render_template('blog.html', posts=posts, pagetitle="Build-A-Blog")

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == "":
            error = "Title can't be blank"
            return render_template('newpost.html', body=body, error_msg=error)
        if body == "":
            error = "Body can't be blank"
            return render_template('newpost.html', title=title, error_msg=error)
        newpost = blog(title, body)
        db.session.add(newpost)
        db.session.commit()
        lastid = blog.query.order_by('id DESC').first()
        return redirect('/blog?id='+str(lastid.id))

    return render_template('newpost.html', pagetitle="New Post")

    



if __name__ == '__main__':
    app.run()
