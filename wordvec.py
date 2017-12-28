from gensim.models.keyedvectors import KeyedVectors
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

max_vec = 100000
vec_filepath = '/home/machlearn/dev/GoogleNews-vectors-negative300.bin'

print('Loading vectors...')
word_vectors = KeyedVectors.load_word2vec_format(vec_filepath, binary=True, limit=max_vec)
print('Done')


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'foo'

class Word2VecForm(Form):
    x1 = TextField('Man', validators=[validators.required(), validators.Length(min=1, max=35)])
    x2 = TextField('King', validators=[validators.required(), validators.Length(min=1, max=35)])
    y1 = TextField('Woman', validators=[validators.required(), validators.Length(min=1, max=35)])

@app.route("/", methods=['GET', 'POST'])
def get_mostsim_cosmul():
    form = Word2VecForm(request.form)

    def format_result(res):
        x = []
        for tup in res:
            val = str(tup[0])
            conf = str(tup[1])[:4]
            pad = ' ' * (40-len(val))
            x.append('Value:   {} {}   Match:   {}'.format( val, pad, conf ).encode("utf-8") )
        return x
     
    print form.errors
    if request.method == 'POST':
        x1=request.form['x1'].encode("utf-8")
        x2=request.form['x2'].encode("utf-8")
        y1=request.form['y1'].encode("utf-8")

        if form.validate:
            try:
                res = word_vectors.most_similar_cosmul(positive=[x2, y1], negative=[x1], topn=5)
                flash(format_result(res))
            except KeyError as err:
                flash('Error: ' + str(err).encode("utf-8"))
        else:
            flash('Error: All the form fields are required. ')

    return render_template('form.html', form=form)

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')



