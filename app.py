from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

import spravakonta

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html", prihlaseny=True)

@app.route('/odhlasit')
def odhlasit():
    hl_stranka = make_response(redirect(url_for('index')))
    hl_stranka.delete_cookie('SessionID')
    return hl_stranka

@app.route('/prihlasovanie', methods=['GET'])
def prihlasovanie():
    if request.method == 'GET':
        if len(request.args) == 4:
            try:
                request.get_data()
                data = dict()
                data["meno"] = request.args.get('meno')
                data["heslo"] = request.args.get('heslo')
                data["trvaly"] = request.args.get('trvaly')
                hl_stranka = make_response(redirect(url_for('index')))
                hl_stranka.set_cookie('SessionID', "test", max_age=30*24*60*60)
                return hl_stranka
            except:
                return redirect(url_for('index'))
        return render_template('prihlasovanie.html')

@app.route('/registrovanie')
def registrovanie():
    if len(request.args) == 3:
        try:
            meno = request.args.get('meno')
            heslo = request.args.get('heslo')
            email = request.args.get('email')
            # todo registracia uzivatela
            if True: # uspesna registracia
                konto = make_response(redirect(url_for('konto')))
                konto.set_cookie('SessionID', "test", max_age=30*24*60*60)
                return konto
            else:
                return render_template('registrovanie.html', neuspesne=True, chyba='text chyby')
        except:
            redirect(url_for('registrovanie'))
    return render_template('registrovanie.html')

@app.route('/konto')
def konto():
    return render_template('konto.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/prispevok')
def prispevok():
    return render_template('prispevok.html')

@app.route('/sprava')
def sprava():
    return render_template('sprava.html')

@app.route('/spravy')
def spravy():
    return render_template('spravy.html')

@app.route('/vyhladavanie')
def vyhladavanie():
    return render_template('vyhladavanie.html')

@app.route('/navody')
def navody():
    return redirect(url_for('index'))

@app.route('/navod')
def navod():
    return redirect(url_for('index'))

@app.route('/blog')
def blog():
    return redirect(url_for('index'))

@app.route('/blogy')
def blogy():
    return redirect(url_for('index'))