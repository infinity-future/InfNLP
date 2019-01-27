
from flask import Flask, jsonify, request
from hanlp_backend import HanLP

hanlp_nlp = HanLP()
app = Flask(__name__)


@app.route('/')
def main():
    return 'INF NLP Server'


@app.route('/hanlp/<function>', methods=['POST'])
def hanlp_backend(function=None):
    """
    curl -H 'Content-Type: application/json' \
        -X POST 'localhost:5000/hanlp/tokenize' \
        -d '{"content": "我爱北京天安门"}' | jq .
    """
    if not isinstance(function, str):
        return jsonify(
            success=False,
            error='Unknown Function'
        )

    params = request.get_json()
    if function == 'tokenize':
        print('start tokenize')
        r = hanlp_nlp.tokenize(**params)
        print('end tokenize')
        return jsonify(
            success=True,
            result=r
        )
    return jsonify(
        success=False,
        error='Unknown Function "{}"'.format(function)
    )


app.run(processes=1, threaded=False)
# app.run(debug=False)
