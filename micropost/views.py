from flask import session, url_for, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash

from micropost import app, db
from micropost.forms import EditForm, EntryForm, LoginForm, UserRegisterForm
from micropost.models import User, Entry

@app.after_request
def max_age_headers(response):
    response.headers['Cache-Control'] = 'max-age=300'
    return response

@app.route('/')
def index():
    user = None
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    if not session.get('user_id', None):
        session['user_id'] = None
    else:
        user = User.query.filter_by(id=session['user_id']).first()
    return render_template('index.html', entries=entries, user=user)

@app.route('/add', methods=('GET', 'POST'))
def add_entry():
    form = EntryForm()
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect(url_for('login'))
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(id=user_id).first()
            title = form.title.data
            body =  form.body.data
            entry = Entry(
                user=user,
                title=title,
                body=body
                )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_entry.html', form=form)

@app.route('/delete/<int:post_id>')
def delete_entry(post_id):
    entry = Entry.query.filter_by(id=post_id).first()
    user_id = session.get('user_id', None)
    if user_id == entry.user_id:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit_entry(post_id):
    form = EditForm()
    user_id = session.get('user_id', None)
    entry = Entry.query.filter_by(id=post_id).first()
    if not user_id:
        return redirect(url_for('login'))
    else:
        form.title.data = entry.title
        form.body.data = entry.body
    
    if form.validate_on_submit() and user_id == entry.user_id:
        entry.title = form.title.data
        entry.body = form.body.data
        db.session.commit()
    return render_template('edit_entry.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if session.get('user_id'):
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if session.get('user_id', None):
        session['user_id'] = None
    return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = UserRegisterForm()
    if session.get('user', None):
        return redirect(url_for('index'))
    if form.validate_on_submit():
        username = form.username.data
        pw_hash = generate_password_hash(form.password.data)
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password_hash=pw_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            #TODO: create warning
            pass
    return render_template('register.html', form=form)
