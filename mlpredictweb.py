import sys
import os
from flask import Flask, jsonify, render_template, request
from MalayalamMarkovChain import MalayalamMarkov

os.chdir(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")


@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html',)

@app.route("/api/predict", methods=['GET'])
def do_generate():
    start = request.args.get('start')
    number_words = request.args.get('w')
    if not number_words:
        number_words = 2
    number_results = request.args.get('c')
    if not number_results:
        number_results = 1
    mlmarkov = MalayalamMarkov(input_db='./malayalam.db')
    results = mlmarkov.predict(start, int(number_words), int(number_results))
    return jsonify(word=start, predictions=results)


if __name__ == "__main__":
    app.run()
