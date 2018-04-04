from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import requests

app = Flask(__name__)
app.secret_key = '\xabs\n\x91B\nI\x9f\x89Y\xc5H\xe5\x9c\xde\x8fGV\xf8\x0f\x92[L\xae'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

SUPER_SECRET_PASSWORD = 'youshallnotpass'


class GuestUser(UserMixin):
    id = 'guest'


@login_manager.user_loader
def get_user(user):
    if user != GuestUser.id:
        return None
    else:
        return GuestUser()


@app.route('/__logout__', methods=['GET', 'POST'])
def logout():
    logout_user()
    return "You've been succesfully logged out"


@app.route('/__login__', methods=['GET', 'POST'])
def login():
    if request.values.get('password') == SUPER_SECRET_PASSWORD:
        login_user(GuestUser())

        next = request.values.get('next')
        return redirect(next)

    flash('Your credentials are invalid.')
    return render_template('redirect.html')


@app.route('/')
@app.route('/<path:path>')
@login_required
def proxy(path):
    return "okay, I'll proxy you to /" + path


if __name__ == '__main__':
    app.run(port=5000, debug=True)
