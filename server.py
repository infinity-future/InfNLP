
from flask import Flask, jsonify, request
from flask_cors import CORS
from hanlp_backend import HanLP

hanlp_nlp = HanLP()
app = Flask(__name__)
CORS(app)


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
    result = None
    if function == 'tokenize':
        result = hanlp_nlp.tokenize(**params)
    elif function == 'pos':
        result = hanlp_nlp.pos(**params)
    elif function == 'extract_keywords':
        result = hanlp_nlp.extract_keywords(**params)
    elif function == 'extract_summary':
        result = hanlp_nlp.extract_summary(**params)
    elif function == 'extract_phrase':
        result = hanlp_nlp.extract_phrase(**params)
    elif function == 'add':
        result = hanlp_nlp.add(**params)
    elif function == 'insert':
        result = hanlp_nlp.insert(**params)
    elif function == 'parse':
        result = hanlp_nlp.parse(**params)
    elif function == 'pinyin':
        result = hanlp_nlp.pinyin(**params)
    elif function == 's2t':
        result = hanlp_nlp.s2t(**params)
    elif function == 't2s':
        result = hanlp_nlp.t2s(**params)

    if result is not None:
        return jsonify(
            success=True,
            result=result
        )
    return jsonify(
        success=False,
        error='Unknown Function "{}"'.format(function)
    )


app.run(processes=1, threaded=False, host='0.0.0.0', port=5000)
# app.run(debug=False)
