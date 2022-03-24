from flask import Flask, render_template, request, url_for, redirect, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from flask_bcrypt import Bcrypt

if __name__ == "__main__":
    from forms import (ContactForm,
                       RegisterForm,
                       MessageForm,
                       TevasForm,
                       VaikasForm,
                       RegistracijosForma,
                       PrisijungimoForma,
                       PaskyrosAtnaujinimoForma,
                       UzklausosAtnaujinimoForma,
                       SlaptazodzioAtnaujinimoForma)

import secrets
from PIL import Image
from flask_mail import Message, Mail

from email_settings import MAIL_USERNAME, MAIL_PASSWORD
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'my_site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)
mail = Mail(app)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(80), nullable=False)
    autorius_id = db.Column(db.Integer, db.ForeignKey("vartotojas.id"))
    autorius = db.relationship("Vartotojas")
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

class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Vartotojas.query.get(user_id)

    def __repr__(self):
        return self.vardas


class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.el_pastas == "admin"

admin = Admin(app)
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Message, db.session))
admin.add_view(ManoModelView(Vartotojas, db.session))


@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/straipsniai')
@login_required
def index():
    # page = request.args.get('page', 1, type=int)
    # straipsniai = Article.query.filter_by(autorius_id=current_user.id).paginate(page=page, per_page=5)
    straipsniai = Article.query.all()
    return render_template('index.html', straipsniai=straipsniai)


@app.route('/straipsniai/<int:id>')
def article(id):
    straipsnis = Article.query.get(id)
    return render_template('article.html', straipsnis=straipsnis)


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == "POST":
        autorius = current_user
        # autorius = request.form['autorius']
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


@app.route("/edit_parent/<int:id>", methods=['GET', 'POST'])
def edit_parent(id):
    form = TevasForm()
    tevas = Tevas.query.get(id)
    if form.validate_on_submit():
        tevas.vardas = form.vardas.data
        tevas.pavarde = form.pavarde.data
        tevas.vaikas_id = form.vaikas.data.id
        db.session.commit()
        return redirect(url_for('parents'))
    return render_template("parent_edit.html", form=form, tevas=tevas)

@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas=form.el_pastas.data, slaptazodis=koduotas_slaptazodis)
        db.session.add(vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('home'))
    return render_template('registruotis.html', title='Register', form=form)


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            flash('Prisijungti pavyko!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/paskyra", methods=['GET', 'POST'])
@login_required
def paskyra():
    form = PaskyrosAtnaujinimoForma()
    if form.validate_on_submit():
        if form.nuotrauka.data:
            nuotrauka = save_picture(form.nuotrauka.data)
            current_user.nuotrauka = nuotrauka
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Tavo paskyra atnaujinta!', 'success')
        return redirect(url_for('paskyra'))
    elif request.method == 'GET':
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    nuotrauka = url_for('static', filename='profilio_nuotraukos/' + current_user.nuotrauka)
    return render_template('paskyra.html', title='Account', form=form, nuotrauka=nuotrauka)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Vartotojas.verify_reset_token(token)
    if user is None:
        flash('Užklausa netinkama arba pasibaigusio galiojimo', 'warning')
        return redirect(url_for('reset_request'))
    form = SlaptazodzioAtnaujinimoForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        user.slaptazodis = hashed_password
        db.session.commit()
        flash('Tavo slaptažodis buvo atnaujintas! Gali prisijungti', 'success')
        return redirect(url_for('prisijungti'))
    return render_template('reset_token.html', title='Reset Password', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    # msg = Message('Slaptažodžio atnaujinimo užklausa',
    #               sender='pythonkursascodeacademy@gmail.com',
    #               recipients=[user.el_pastas])
    # msg.body = f'''Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    # {url_for('reset_token', token=token, _external=True)}
    # Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
    # '''
    # mail.send(msg)
    print(f'''Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    {url_for('reset_token', token=token, _external=True)}
    Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
    ''')

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UzklausosAtnaujinimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        send_reset_email(user)
        flash('Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.', 'info')
        return redirect(url_for('prisijungti'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/atsijungti")
def atsijungti():
    logout_user()
    flash('Atsijungti pavyko!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=True)
