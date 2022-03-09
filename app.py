from flask import Flask, render_template, request, url_for, redirect
from forms import ContactForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'my_site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(80), nullable=False)
    autorius = db.Column(db.String(120), unique=True, nullable=False)
    pavadinimas = db.Column(db.String(120), unique=True, nullable=False)
    tekstas = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(120), default="published")

    def __init__(self, data, autorius, pavadinimas, tekstas):
        self.data = data
        self.autorius = autorius
        self.pavadinimas = pavadinimas
        self.tekstas = tekstas

    def __repr__(self):
        return f'{self.data} - {self.pavadinimas}'

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/straipsniai')
def index():
    straipsniai = Article.query.all()
    return render_template('index.html', straipsniai=straipsniai)


@app.route('/straipsniai/<int:id>')
def article(id):
    straipsnis = Article.query.get(id)
    return render_template('article.html', straipsnis=straipsnis)


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == "POST":
        autorius = request.form['autorius']
        pavadinimas = request.form['pavadinimas']
        date = request.form['date']
        tekstas = request.form['tekstas']
        article = Article(date, autorius, pavadinimas, tekstas)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_article.html')

@app.route('/delete_article/<int:id>')
def delete_article(id):
    straipsnis = Article.query.get(id)
    db.session.delete(straipsnis)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('contact_success.html', form=form)
    return render_template('contact_us.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template('success.html', form=form)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=True)
