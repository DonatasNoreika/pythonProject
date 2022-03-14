from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime

if __name__ == "__main__":
    from forms import ContactForm, RegisterForm, MessageForm, TevasForm, VaikasForm

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


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime)
    comment = db.Column(db.Text, nullable=False)

    def __init__(self, fname, lname, comment):
        self.fname = fname
        self.lname = lname
        self.comment = comment
        self.date = datetime.datetime.today()

    def __repr__(self):
        return f'{self.fname} - {self.lname}'


class Tevas(db.Model):
    __tablename__ = "tevas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String)
    pavarde = db.Column("Pavardė", db.String)
    vaikas_id = db.Column(db.Integer, db.ForeignKey("vaikas.id"))
    vaikas = db.relationship("Vaikas")


class Vaikas(db.Model):
    __tablename__ = "vaikas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String)
    pavarde = db.Column("Pavardė", db.String)


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
        print("Forma validuota")
        return render_template('success.html', form=form)
    return render_template('form.html', form=form)


@app.route('/petition', methods=['GET', 'POST'])
def petition():
    data = Message.query.all()[::-1]
    form = MessageForm()
    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        comment = form.comment.data
        entry = Message(fname=fname, lname=lname, comment=comment)
        db.session.add(entry)
        db.session.commit()
        data = Message.query.all()[::-1]
        stats = 20000 - len(data)
        return render_template('petition.html', form=False, data=data, stats = stats)
    return render_template('petition.html', form=form, data=data)

@app.route("/naujas_tevas", methods=["GET", "POST"])
def new_parent():
    form = TevasForm()
    if form.validate_on_submit():
        naujas_tevas = Tevas(vardas=form.vardas.data, pavarde=form.pavarde.data, vaikas_id=form.vaikas.data.id)
        db.session.add(naujas_tevas)
        db.session.commit()
        return redirect(url_for('parents'))
    return render_template("add_parent.html", form=form)


@app.route("/parents")
def parents():
    try:
        all_parents = Tevas.query.all()
    except:
        all_parents = []
    return render_template("parents.html", all_parents=all_parents)


@app.route('/delete_parent/<int:id>')
def delete_parent(id):
    tevas = Tevas.query.get(id)
    db.session.delete(tevas)
    db.session.commit()
    return redirect(url_for('parents'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=True)
