import json

from collections import defaultdict
from .trigram import Trigram

class Model(object):    
    def __init__(self, name = None, freq = None, total = None):
        self.freq = defaultdict(int)
        
        if freq is not None:
            self.freq.update(freq)

        if total is None:
            total = [0] * 3

        self.name = name
        self.total = total

    def add(self, gram):
        # check name and gram
        if self.name is None or gram is None: 
            return
        # get length of gram
        length = len(gram)
        # check if gram length is valid
        if length < 1 or length > 3:
            return
        self.total[length - 1] += 1
        self.freq[gram] += 1

    def update(self, text):        
        # check if text is valid
        if text is None:
            return
        # create gram
        gram = Trigram()
        
        for char in text:
            # add char to gram
            gram.add_char(char)
            for n in range(1,4):
                # add gram to model
                self.add(gram.get(n))

    def serialize(self):
        json_data = json.dumps({"name":self.name , "freq" : self.freq, "total" : self.total})
        return json_data
