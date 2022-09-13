from flask import Flask, request
from flask_restx import Api
from flask_cors import CORS
import urllib
from movie_search import scean_search, line_search

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JSON_AS_ASCII'] = False


@app.route('/search', methods=["GET"])
def search():
    type = request.args.get('type', '')
    question = request.args.get('query', '')

    if type == 'SCENE':
        resp = scean_search(question)
    else:
        resp = line_search(question)

    return resp


# authbind 써서 권한 문제 해결할 수 있음
if __name__ == "__main__":
    app.run(host=("0.0.0.0"), debug=True, port=8000)
# GET, PUT, DELETE -> request.args.get('key)
# POST -> request.get_json()
# State Code -> 200 : sucees
# 400 : not variable parapeter or false request
# 401 : not aloow access
# 403 : ban access
# 404 : Not found resource
# 500 : internal serverl error
