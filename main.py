from flask import Flask, render_template, request
import markdown

import database.data as DB

app = Flask(__name__)
DB.initConnection(app)
DB.testConnection(app)

@app.route('/markdown', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['markdown']
        html = markdown.markdown(text)
        return render_template('markdown.html', markdown=text, html=html)
    return render_template('markdown.html')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/connexion", methods=['GET'])
def connexion():
    return render_template('connexion.html')

@app.route("/formConnexion", methods=['POST'])
def TryConnexion():
    DB.sendFormConnection(request_=request)
    return ("",204)
app.run(debug=True)