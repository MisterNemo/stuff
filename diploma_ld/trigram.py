class Trigram(object):
    def __init__(self):
        self.grams = ' '
        self.capital_word = False

    def add_char(self, char):
        # normalize character
        char = self.normalize(char)
        
        last_char = self.grams[-1]

        if last_char == ' ':
            self.grams = ' '
            self.capital_word = False
            if char == ' ':
                return
        elif len(self.grams) >= 3:
            self.grams = self.grams[1:]
        self.grams += char

        if char.isupper():
            if last_char.isupper():
                self.capital_word = True
        else:
            self.capital_word = False

    def get(self, n):
        if self.capital_word:
            return
        if n < 1 or n > 3 or len(self.grams) < n:
            return
        if n == 1:
            char = self.grams[-1]
            if char == ' ':
                return
            return char
        else:
            return self.grams[-n:]
    
    def normalize(self, char):
        code = ord(char)
        
        if not((code >= 0x0041 and code <= 0x005A) or 
               (code >= 0x0061 and code <= 0x007A) or 
               (code >= 0x00C0 and code <= 0x00D6) or
               (code >= 0x00D8 and code <= 0x00F6) or
               (code >= 0x00F8 and code <= 0x00FF) or
               (code >= 0x0400 and code <= 0x04FF) or
               (code >= 0x0500 and code <= 0x052F)):
            return ' '
        return char
