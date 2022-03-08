from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
