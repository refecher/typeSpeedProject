import random
from database import list_of_texts


class ChooseText:
    def __init__(self):
        self.index_text = random.randint(0, len(list_of_texts) - 1)
        self.text = list_of_texts[self.index_text]
