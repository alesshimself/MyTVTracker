import json

from flask import render_template, flash, redirect, url_for, request

import app
from app import milvus_collection
from app.milvus_utils import insert_vectors
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verifica se l'utente esiste già
        results = milvus_collection.query(f"username == '{username}' or email == '{email}'")
        if results:
            flash('Username or email already exists.')
            return redirect(url_for('register'))

        # Crea nuovo utente
        new_user = User(username, email)
        new_user.set_password(password)

        # Inserisci l'utente in Milvus
        user_data = json.dumps({
            'username': new_user.username,
            'email': new_user.email,
            'password_hash': new_user.password_hash
        })
        insert_vectors(milvus_collection, [[0] * 1024], [user_data])  # Usiamo un vettore di zeri come placeholder

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register')
