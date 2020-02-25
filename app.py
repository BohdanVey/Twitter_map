import create_map
from flask import Flask, render_template, request
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class LoginForm(FlaskForm):
    username = StringField('Screen name', validators=[DataRequired()])
    submit = SubmitField('Build map')

@app.route('/', methods=['POST','GET'])
def screen_name():
    form = LoginForm()
    if request.method == 'POST':
        print(request.form.get('username'))
        print(create_map.create_map(request.form.get('username')))
        return create_map.create_map(request.form.get('username'))
    else:
        return render_template('login.html', title='Map', form=form)



if __name__ == '__main__':
    name = ''
    app.run(port=3008)
