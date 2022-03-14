from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email


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