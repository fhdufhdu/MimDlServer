from encodings import search_function
from elasticsearch import Elasticsearch
from konlpy.tag import Mecab
from sentence_transformers import SentenceTransformer, util
import numpy as np


class MoiveSearch:
    def __init__(self) -> None:
        self.es = Elasticsearch("http://localhost:9200/")
        self.model = SentenceTransformer('./models/training_sts')

    def get_search_result(self, query, is_scene: bool):
        resultDict = {'data': []}
        if is_scene:
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

                docs = self.es.search(index='movie',
                                            body={
                                                "size": 10,
                                                "query": {
                                                    "multi_match": {
                                                        "query": query_after,
                                                        "fields": ["caption", "director", "actor", "synopsis", "feature", "genre", "title", "subtitle", 'translation']
                                                    }
                                                }
                                            })
                for doc in docs['hits']['hits']:
                    resultDict['data'].append(doc['_source']['title'])

            except Exception as e:
                print(e)
        else:
            try:
                docs = self.es.search(index='movie',
                                      body={
                                          "size": 10,
                                          "query": {
                                              "multi_match": {
                                                  "query": query,
                                                  "fields": ["title", "subtitle", 'translation']
                                              }
                                          }
                                      })
                query_embedding = self.model.encode(
                    [query], convert_to_numpy=True)
                doc_result = docs['hits']['hits']
                for i in range(len(doc_result)):
                    datatitle = doc_result[i]['_source']['datatitle']
                    subtitle_embeddings = np.load(
                        f'./data/{datatitle}/embeded.npy')
                    cosine_scores = util.pytorch_cos_sim(
                        query_embedding, subtitle_embeddings)[0]
                    subtitles = []
                    for j in cosine_scores.argsort(descending=True)[0:5]:
                        subtitles.append(
                            doc_result[i]['_source']['translation'][j])
                    result = {
                        "title": doc_result[i]['_source']['title'],
                        "subtitle": subtitles
                    }

                    resultDict['data'].append(result)

            except Exception as e:
                print(e)

        return resultDict
