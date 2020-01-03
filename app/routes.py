from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
def main():
    user = {'username': 'Alex'}
    return render_template('index.html', title='My', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Sign In requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/index")
def index():
    user = {'username': 'Alex'}
    posts = [
        {
            'author': {'username': 'Mike'},
            'body': 'Good Luck!'
        },
        {
            'author': {'username': 'Jonh'},
            'body': 'Good Game!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)