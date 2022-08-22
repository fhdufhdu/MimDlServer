from elasticsearch import Elasticsearch
from konlpy.tag import Mecab
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

with open('./config', 'r', encoding="utf-8") as file:
    config = json.load(file)

es = Elasticsearch(config['es'])
model = SentenceTransformer(config['model'])


def es_search(size, query, fields):
    docs = es.search(index='movie',
                     body={
                         "size": size,
                         "query": {
                             "multi_match": {
                                 "query": query,
                                 "fields": fields
                             }
                         }
                     })
    docs = docs['hits']['hits']
    return list(map(lambda x: x['_source'], docs))


def scean_search(query):
    result_dict = {'data': []}
    try:
        mecab_tokenizer = Mecab()
        nouns_list = mecab_tokenizer.nouns(query)
        query_after = ''
        for noun in nouns_list:
            if noun in ["영화", "장면"]:
                continue
            query_after += noun + ' '
        query = query.replace('영화', '').replace('장면', '')
        query_after += query

        docs = es_search(10, query_after, [
                         "caption", "director", "actor", "synopsis", "feature", "genre", "title", "subtitle", 'translation'])

        for doc in docs:
            result_dict['data'].append(doc['id'])

    except Exception as e:
        print(e)


def line_search(query):
    result_dict = {'data': []}
    try:
        docs = es_search(10, query, ["title", "subtitle", 'translation'])
        query_embedding = model.encode([query], convert_to_numpy=True)
        for i in range(len(docs)):
            datatitle = docs[i]['datatitle']
            subtitle_embeddings = np.load(
                f'./data/{datatitle}/embeded.npy')
            cosine_scores = util.pytorch_cos_sim(
                query_embedding, subtitle_embeddings)[0]
            subtitles = []
            for j in cosine_scores.argsort(descending=True)[0:5]:
                subtitles.append(
                    docs[i]['translation'][j])
            result = {
                "title": docs[i]['title'],
                "subtitle": subtitles
            }

            result_dict['data'].append(result)

    except Exception as e:
        print(e)
