import requests
from tqdm import tqdm
from func import load_text, save_json, save_text, load_json

url_dict_list = load_json(
    '/home/fhdufhdu/code/mim-dl-server/netflix-data.json')['data']

for content in tqdm(url_dict_list):
    # rating_id = None
    # try:
    #     if content["관람등급"] == "전체":
    #         rating_id = 1
    #     elif content["관람등급"] == "12세이상관람가":
    #         rating_id = 2
    #     elif content["관람등급"] == "15세이상관람가":
    #         rating_id = 3
    #     elif content["관람등급"] == "청소년관람불가":
    #         rating_id = 4
    #     else:
    #         rating_id = 5
    # except:
    #     rating_id = 5
    data_ = {
        "actors": ', '.join(content["출연"]) if "출연" in content else None,
        "directors": ', '.join(content["감독"]) if "감독" in content else None,
        "features": ', '.join(content["영화 특징"]) if "영화 특징" in content else None,
        "genres": ', '.join(content["장르"]) if "장르" in content else None,
        "dirName": '/home/fhdufhdu/code/movie-image/movie_image' + content["데이터제목"] if "데이터제목" in content else None,
        "engTitle": content["영제"] if "영제" in content else None,
        "runningTime": content["시간"] if "시간" in content else None,
        "synopsis": content["시놉시스"] if "시놉시스" in content else None,
        "title": content["제목"] if "제목" in content else None,
        "releaseYear": content["연도"] if "연도" in content else None,
        "movieRating": content["관람등급"] if "관람등급" in content else None,
        "writers": ', '.join(content["각본"]) if "각본" in content else None
    }

    url = 'http://localhost:8080/movies'
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.post(url, json=data_, headers=headers)
