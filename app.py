from flask import Flask, rander_tamplate

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Siema byniu</h1>'

@app.route('/index', methods=['GET','POST'])
def exchange():
    return render_template('exchange.html')

#if __name__ == '__main__':
#    app.run()