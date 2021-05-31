from typing import Dict
import yaml
import random
from errors import NoMoreQuestions


class GdalQuiz:

    def __init__(self, yaml_path: str):
        self.qpath = yaml_path
        self.asked = []
        self.qdata = self.load_yaml()
        sefl.n_correct = 0

    def add_tag(self):
        pass

    def load_yaml(self) -> Dict:
        with open(self.qpath, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_random_q(self):
        try:
            _q = random.choice(list(self.qdata.values()))
            return self.qdata.pop(self.key_by_value(_q))
        except NoMoreQuestions:
            print('no questions left')

    def check_answer(question: dict, answerkey: str) -> bool:
        return question['correct'] == answerkey

    @staticmethod
    def progress(i: int) -> str:
        s = [f"{v}0..." for v in range(10)]
        s.append("100 - done.")
        return "".join(s[:i+1])


