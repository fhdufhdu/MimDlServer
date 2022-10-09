from func import load_json, load_pickle, load_text, add_text_on_file, save_json, save_pickle
from tqdm import tqdm
from elasticsearch import Elasticsearch
import json

es = Elasticsearch("http://localhost:9200/")

es.indices.delete(index="movie", ignore=[400, 404])

es.indices.create(
    index='movie',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "tokenizer": "nori_tokenizer"
                }
            }
        }
    }
)


es = Elasticsearch("http://localhost:9200/")
URL = "./final_data.json"
with open(URL, "r") as json_file:
    json_data = json.load(json_file)
body = ""
count = 0
for j in tqdm(json_data['data']):
    if (j['title'] == '검은 사제들'):
        print(j['title'])
    count += 1
    # body = body + json.dumps({"index": {"_index": 'movie'}}) + '\n'
    # body = body + json.dumps(j, ensure_ascii=False) + '\n'
    es.index(index="movie", body=j)

    # if((count % 100 == 0) or (count == len(json_data['data']))):
        #es.bulk(body)
        # es.index(index="movie", body=j)
        #print(str(count) + " 데이터 입력")
        #es.indices.refresh(index="movie")
        #body = ""


print("done")


try:
    es = Elasticsearch("http://localhost:9200/")
    docs = es.search(index='movie',
                     body={
                         "size": 1,
                         "query": {
                             "multi_match": {
                                 "query": "검은 사제들",
                                 "fields": ["title"]
                             }
                         }
                     })
#    print(docs)
    for i in range(len(docs['hits']['hits'])):
        print(docs['hits']['hits'][i]['_source'])
except Exception as e:
    print(e)