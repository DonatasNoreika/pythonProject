from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     SelectField,
                     BooleanField)
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed


class ContactForm(FlaskForm):
    name = StringField('Vardas', [DataRequired()])
    email = StringField('El.paštas', [Email(message=('Neteisingas adresas.')), DataRequired()])
    body = TextAreaField('Jūsų pranešimas', [DataRequired(),
                                        Length(min=10,
                                        message=('Per trumpas tekstas.'))])
    submit = SubmitField('Pateikti')


class RegisterForm(FlaskForm):
    email = StringField('Vardas', [Email(message=('Neteisingas adresas.')), DataRequired(message='Lauką būtina užpildyti')])
    password = PasswordField('Slaptažodis', validators=[Length(min=8, message=('Per mažai simbolių!')), DataRequired(message='Lauką būtina užpildyti')])
    address1 = StringField('Adresas (pirma eilutė)', validators=[DataRequired(message=('Lauką būtina užpildyti')), Length(min=4, message=('Per mažai simbolių!'))])
    address2 = StringField('Adresas (antra eilutė)', validators=[Length(min=4, message=('Per mažai simbolių'))])
    city = StringField('Miestas', validators=[DataRequired(message='Lauką būtina užpildyti'), Length(min=4, message=('Per mažai simbolių'))])
    state = SelectField('Rajonas', choices=[('vln', 'Vilniaus'), ('kns', 'Kauno'), ('klp', 'Klaipėdos')], validators=[DataRequired(message='Lauką būtina užpildyti')])
    zip_code = StringField('Pašto kodas', validators=[DataRequired(message='Lauką būtina užpildyti'), Length(min=4, message=('Per mažai simbolių'))])
    agree = BooleanField('Sutinku gauti šlamštą')
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    fname = StringField('Vardas', [DataRequired()])
    lname = StringField('Pavardė', [DataRequired()])
    comment = TextAreaField('Komentaras')
    submit = SubmitField('Pasirašyti')


import app

def vaikas_query():
    return app.Vaikas.query

class TevasForm(FlaskForm):
    vardas = StringField('Numeris', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    vaikas = QuerySelectField(query_factory=vaikas_query, allow_blank=True, get_label="vardas", get_pk=lambda obj: str(obj))
    submit = SubmitField('Įvesti')


class VaikasForm(FlaskForm):
    vardas = StringField('Numeris', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    submit = SubmitField('Įvesti')


class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El. paštas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    patvirtintas_slaptazodis = PasswordField("Pakartokite slaptažodį", [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = app.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Šis vardas panaudotas. Pasirinkite kitą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = app.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')


class PaskyrosAtnaujinimoForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El. paštas', [DataRequired()])
    nuotrauka = FileField('Atnaujinti profilio nuotrauką', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atnaujinti')

    def tikrinti_varda(self, vardas):
        if vardas.data != app.current_user.vardas:
            vartotojas = app.Vartotojas.query.filter_by(vardas=vardas.data).first()
            if vartotojas:
                raise ValidationError('Šis vardas panaudotas. Pasirinkite kitą.')

    def tikrinti_pasta(self, el_pastas):
        if el_pastas.data != app.current_user.el_pastas:
            vartotojas = app.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
            if vartotojas:
                raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')

class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField("Prisiminti mane")
    submit = SubmitField('Prisijungti')

class UzklausosAtnaujinimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', validators=[DataRequired(), Email()])
    submit = SubmitField('Gauti')

    def validate_email(self, el_pastas):
        user = app.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if user is None:
            raise ValidationError('Nėra paskyros, registruotos šiuo el. pašto adresu. Registruokitės.')

class SlaptazodzioAtnaujinimoForma(FlaskForm):
    slaptazodis = PasswordField('Slaptažodis', validators=[DataRequired()])
    patvirtintas_slaptazodis = PasswordField('Pakartokite slaptažodį',
                                             validators=[DataRequired(), EqualTo('slaptazodis')])
    submit = SubmitField('Atnaujinti Slaptažodį')