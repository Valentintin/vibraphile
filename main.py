from flask import Flask, render_template, request
import markdown

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['markdown']
        html = markdown.markdown(text)
        return render_template('index.html', markdown=text, html=html)
    return render_template('index.html')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)