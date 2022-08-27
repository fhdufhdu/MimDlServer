import json
import pickle
from tqdm import tqdm


def save_json(file_name, dict_):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(dict_, file, indent='\t', ensure_ascii=False)


def load_json(file_name):
    dict_ = None
    with open(file_name, 'r', encoding='utf-8') as file:
        dict_ = json.load(file)
    return dict_


def save_text(file_name, text=''):
    f = open(file_name, 'w', encoding='utf-8')
    f.write(text)
    f.close()


def save_text_list(file_name, text_list):
    f = open(file_name, 'w', encoding='utf-8')
    if text_list != None:
        for text_elem in text_list:
            f.write(text_elem)
            f.write('\n')
    f.close()


def load_text(file_name) -> list:
    text_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            text_list.append(line)
        f.close()
    return text_list


def add_text_on_file(file_name, text):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(text)
        f.close()


def save_pickle(file_name, obj):
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
        return obj


def returnPreSubject(korean_word):
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ',
                    'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ',
                     'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ',
                     'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    NUMBER_LIST = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    ENG_LIST = ['에이', '비', '씨', '디', '이', '에프', '지', '에이치', '아이', '제이', '케이', '엘',
                '엠', '엔', '오', '피', '큐', '알', '에스', '티', '유', '브이', '더블유', '엑스', '와이', '제트']
    if korean_word is not None and len(korean_word) > 0:
        w = korean_word[len(korean_word)-1]  # 마지막 글자 획득

        # 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가'))//588
            # 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            if ch3 == 0:
                return '는'
            else:
                return '은'
        elif '0' <= w <= '9':  # 숫자일 경우
            return returnPreSubject(NUMBER_LIST[ord(w)-ord('0')])
        elif type(w) is int and 0 <= w <= 9:
            return returnPreSubject(NUMBER_LIST[w])
        elif 'a' <= w <= 'z':  # 영문일 경우
            return returnPreSubject(ENG_LIST[ord(w)-ord('a')])
        elif 'A' <= w <= 'Z':
            return returnPreSubject(ENG_LIST[ord(w)-ord('A')])
        else:
            return returnPreSubject(korean_word[:len(korean_word)-1])

    return '는'  # 디폴트로 '는' 리턴


def remove_bracket(doc):
    remove_list = []

    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '(':
            start_idx = i
        if start_idx != -1 and doc[i] == ')':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1
    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '[':
            start_idx = i
        if start_idx != -1 and doc[i] == ']':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1
    start_idx = -1
    for i in range(len(doc)):
        if doc[i] == '{':
            start_idx = i
        if start_idx != -1 and doc[i] == '}':
            remove_list.append(doc[start_idx:i+1])
            start_idx = -1

    for remove_word in remove_list:
        doc = doc.replace(remove_word, '')

    return doc


def remove_duplicated_keyword(keywords):
    temp_dict = {}
    for k in keywords:
        temp_dict[k] = 0
    keywords = list(temp_dict.keys())
    return keywords
