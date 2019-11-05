import os
import pickle

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, request, url_for
from flask import render_template, redirect

from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__, template_folder='html')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config.from_object(Config)
Bootstrap(app)


class TextForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Get Result')


class Response(FlaskForm):
    score = StringField('Score', validators=[DataRequired()])
    sentiment = StringField('Sentiment', validators=[DataRequired()])
    submit = SubmitField('Try Again')


def score_text(text):
    try:
        model = pickle.load(open("logreg.pkl", "rb"))
        tfidf = pickle.load(open("tf-idf.pkl", "rb"))

        score = model.predict_proba(tfidf.transform([text]))[0][1]
        sentiment = 'positive' if score > 0.5 else 'negative'
    except Exception as e:
        print(str(e))
        score, sentiment = 0.0, 'unknown'

    return score, sentiment


@app.route('/')
@app.route('/index')
def get_index():
    return '<html><center><script>document.write("Hello, i`am Flask Server!")</script></center></html>'


@app.route('/result', methods=['GET', 'POST'])
def get_result():
    response = Response()

    if response.validate_on_submit():
        return redirect(url_for('get_text_score'))

    score = request.args.get('score')
    sentiment = request.args.get('sentiment')

    response.score.data = score
    response.sentiment.data = sentiment

    return render_template('from_form.html', form=response)


@app.route('/sentiment', methods=['GET', 'POST'])
def get_text_score():
    form = TextForm()
    if form.validate_on_submit():
        score, sentiment = score_text(form.text.data)
        form.text.data = 'ytkkava'
        return redirect(url_for('get_result', score=score, sentiment=sentiment))

    return render_template('from_form.html', form=form)


