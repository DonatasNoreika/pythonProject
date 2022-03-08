from flask import Flask, render_template, request, url_for, redirect
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'

straipsniai = [{
    'data': '2020 01 01',
    'autorius': 'Autorius 1',
    'pavadinimas': 'Apie nieką',
    'tekstas': 'Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit​​, morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris.',
    'status': 'published'
    },
    {
        'data': '2020 02 01',
        'autorius': 'KITAS AUTORIUS',
        'pavadinimas': 'Apie zombius',
        'tekstas': 'Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit​​, morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris. ',
        'status': 'published'
    },
    {
        'data': '2020 03 01',
        'autorius': 'Dar kažkas',
        'pavadinimas': 'Braiiins!',
        'tekstas': 'Zombie ipsum reversus ab viral inferno, nam rick grimes malum cerebro. De carne lumbering animata corpora quaeritis. Summus brains sit​​, morbo vel maleficia? De apocalypsi gorger omero undead survivor dictum mauris.',
        'status': 'unpublished'
    }]


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/straipsniai')
def index():
    return render_template('index.html', straipsniai=straipsniai)


@app.route('/straipsniai/<string:title>')
def article(title):
    return render_template('article.html', title=title, straipsniai=straipsniai)


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == "POST":
        autorius = request.form['autorius']
        pavadinimas = request.form['pavadinimas']
        date = request.form['date']
        tekstas = request.form['tekstas']
        straipsniai.append(
        {
            'data': date,
            'autorius': autorius,
            'pavadinimas': pavadinimas,
            'tekstas': tekstas,
            'status': 'published'
        }
        )
        return redirect(url_for('index'))
    return render_template('add_article.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        return render_template('contact_success.html', form=form)
    return render_template('contact_us.html', form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
