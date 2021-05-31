
from typing import Dict, List
import yaml
import random

def dict_to_labellist(d: dict) ->list:
    return [{'label': v, 'value': k } for k, v in d.items()]


def list_to_labellist(l: dict) ->list:
    return [{'label': v, 'value': i } for i, v in enumerate(l)]


def load_yaml(yaml_path: str) -> Dict:
    with open(yaml_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def random_question(qdata: dict):
    return random.choice(list(qdata))


def add_bool_subkey(qdata: dict, key) -> dict:
    for k in qdata:
        qdata[k][key] = False
    return qdata


def not_asked(d: dict) -> dict or None:
    reduced_d = {}
    for k, v in d.items():
        if not d[k]['asked']:
            reduced_d[k] = v
    return reduced_d


def rm_ask(d: dict) ->dict:
    for k in d:
        d[k]['ask'] = False
    return d


def key_by_value(d: dict, val) -> str:
    for k, v in d.items():
        if val == v:
            return k


def n_asked_questions(d: dict) -> str:
    """ returns number of questions answered""" 
    _asked = 0
    for i in d:
        if d[i]['asked']:
            _asked += 1
    return _asked


def n_correct_answers(d: dict) -> str:
    """ returns number of questions answered""" 
    _iscorrect = 0
    for i in d:
        if d[i]['is_correct']:
            _asked += 1
    return _iscorrect


def get_question(d: dict) -> dict:
    for k, v in d.items():
        if d[k]['ask']:
            return d[k]


def progress(i: int) -> str:
    s = [f"{v}0..." for v in range(10)]
    s.append("100 - done.")
    return "".join(s[:i+1])


def check_answer(d: dict, answer_key: str) -> bool:
    """ """ 
    return d['correct'] == answer_key