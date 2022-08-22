from flask import Flask, request
from flask_restx import Api
from flask_cors import CORS
import urllib
from movieSearch import MoiveSearch

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['JSON_AS_ASCII'] = False

movieSearch = MoiveSearch()


@app.route('/search', methods=["GET", "POST"])
def qna():
    if request.method == "POST":
        data = request.get_json()

        key_list = list(data.keys())

        is_scene = data[key_list[0]]
        question = data[key_list[1]]

        resp = movieSearch.get_search_result(question, is_scene)

        return resp

    elif request.method == "GET":
        data = urllib.parse.urlencode(request.args, doseq=True)
        decoded_data = urllib.parse.parse_qs(data, encoding='utf-8')


if __name__ == "__main__":
    app.run(host=("0.0.0.0"), debug=True, port=443)
# GET, PUT, DELETE -> request.args.get('key)
# POST -> request.get_json()
# State Code -> 200 : sucees
# 400 : not variable parapeter or false request
# 401 : not aloow access
# 403 : ban access
# 404 : Not found resource
# 500 : internal serverl error
