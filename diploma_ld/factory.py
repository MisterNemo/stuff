import os
import sys
import json
import re
import random
import six
import json

from os import path
from six.moves import zip, xrange

from .detector import Detector
from .model import Model
from .trigram import Trigram

models_dir = path.join(path.dirname(__file__), 'models')

class Factory(object):
    
    def __init__(self):
        self.lang_list = []
        self.gram_lang_prob_map = {}

    def load_models(self):
        list_of_models = os.listdir(models_dir)
        if not list_of_models:
            print("models not found")
            return

        size = len(list_of_models)
        index = 0

        for filename in list_of_models:
            filename = path.join(models_dir,filename)

            if not path.isfile(filename):
                continue
            
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    model = Model(**json_data)
                    #print(model.serialize())
                    self.set_model(model, index, size)
                    index += 1
            except:
                pass
                    
    def set_model(self, model, index, size):
        lang = model.name
        if lang in self.lang_list:
            return

        self.lang_list.append(lang)
        
        for gram in model.freq:
            if gram not in self.gram_lang_prob_map:
                self.gram_lang_prob_map[gram] = [0.0] * size
            length = len(gram)
            if 1 <= length <= 3:
                prob = 1.0 * model.freq.get(gram) / model.total[length - 1]
                self.gram_lang_prob_map[gram][index] = prob

    def create_model(self,lang):
        model = Model(lang)
        
        with open(path.join(models_dir,lang+".json"), "w") as f:
            f.write(model.serialize())
    
    def detect(self,text):
        formatted_text = ""
        last_char = 0
        for i in xrange(min(len(text), 10000)):
            char = text[i]
            if char != ' ' or last_char != ' ':
                formatted_text += char
            last_char = char;
        
        grams = []
        trigram = Trigram()
        for char in formatted_text:
            trigram.add_char(char)
            if trigram.capital_word:
                continue
            for n in range(1,4):
                if len(trigram.grams) < n:
                    break;
                g = trigram.grams[-n:]
                if g and g != ' ' and g in self.gram_lang_prob_map:
                    grams.append(g)

        if not grams:
            return "Hell Yeah!"

        lang_prob = [0.0] * len(self.lang_list)

        random.seed()

        for t in range(7):
            prob = [1.0 / len(self.lang_list)] * len(self.lang_list)
            alpha = 0.5 + random.gauss(0.0, 1.0) * 0.05
            i = 0
            while True:
                gram = random.choice(grams)
                lang_prob_map = self.gram_lang_prob_map[gram]
                weight = alpha / 10000
                for j in xrange(len(prob)):
                    prob[j] *= weight + lang_prob_map[j]
                if i % 5 == 0:
                    max_prob, sum_prob = 0.0, sum(prob)
                    for j in xrange(len(prob)):
                        p = prob[j] / sum_prob
                        if max_prob < p:
                            max_prob = p
                        prob[j] = p
                    if max_prob > 0.99999 or i >= 1000:
                        break
                i += 1
            for j in xrange(len(lang_prob)):
                lang_prob[j] += prob[j] / 7
        
        result = [{'lang':lang,'prob':prob} for lang, prob in zip(self.lang_list,lang_prob)] 
        
        json_data = json.dumps(result)
        return json_data

    def train(self, lang, text):
        filename = path.join(models_dir,lang+".json")
        #print(filename)
        try:
            with open(filename, "r+") as f:
                json_data = json.load(f)
                #print(json_data)
                model = Model(**json_data)
                model.update(text)
                #print(model.serialize())
                f.seek(0)
                f.write(model.serialize())
                f.truncate()

            return True
        except:
            return False

def create_model(lang):
    factory = Factory()
    factory.create_model(lang)

def detect(text):
    factory = Factory()
    factory.load_models()
    return factory.detect(text)
    
def train(lang, text):
    factory = Factory()
    factory.load_models()
    return factory.train(lang, text)

