"""abstract Preprocessor class and inheriting EMSPreprocessor"""
from abc import ABC, abstractmethod
from num2words import num2words

class Preprocessor(ABC):

    @abstractmethod
    def process(self, text):
        """method that contains runs all components of specified pipeline on inputted text"""
        pass



class EMSPreprocessor(Preprocessor):
    # dict containing common words that need to be transformed during preprocessing
    translation_dict={
        "mm": "MM",
        " x ": " times ",
        "mL": "ML",
        "Pt": "PT",
        "pt": "PT",
        "pT": "PT"
    }

    def process(self, text):
        arr = self.generate_word_arr(text)
        print("1: ", arr[0:15])
        arr = self.split_words_with_numbers(arr)
        print("2: ", arr[0:15])

        arr = self.split_abbreviations(arr)
        print("3: ", arr[0:15])

        arr = self.convert_numbers_to_words(arr)
        print("4: ", arr[0:15])


        arr = self.remove_blanks(arr)
        return arr


    def remove_blanks(self, arr):
        new_arr = []
        for elem in arr:
            if len(elem) > 0:
                new_arr.append(elem)
        return new_arr


    def translate(self, text):
        """converts keys of translation_dict into corresponding values"""
        for key in self.translation_dict.keys():
            val = self.translation_dict[key]
            text = text.replace(key, val)
        return text


    def generate_word_arr(self, text):
        """generate array of tokens from text"""
        translated_text = self.translate(text)
        without_punctuation = self.remove_punctuation(translated_text)
        return without_punctuation.split(" ")


    def remove_punctuation(self,text):
        """remove all punctuation except for ' . ? , (to hold pauses in text)"""
        punctuation_to_remove = '"#$%&()*+ -/:;<=>@[\]^_`{|}~'
        for char in punctuation_to_remove:
            text = text.replace(char, " ")
        return text


    def convert_numbers_to_words(self, arr):
        """convert numbers to english representation
        i.e. 42 --> fourty two
        """
        new_string_arr = []
        for token in arr:
            new_token = token
            if token.isnumeric():
                new_token = num2words(token)
            new_string_arr.append(new_token)
        return new_string_arr


    def split_words_with_numbers(self,arr):
        """i.e.
        SPO2 --> [S, P, O, 2]
        bp28y --> [b, p, 28, y]
        """
        new_arr = []
        for word in arr:
            if any([char.isdigit() for char in word]): # check if digit is present in arr
                i = 0
                current_number = ""
                while i < len(word):
                    if word[i].isdigit():
                        current_number += word[i]
                    else:
                        if len(current_number) > 0:
                            new_arr.append(current_number)
                        current_number = ""
                        new_arr.append(word[i])
                    i += 1
            else:
                new_arr.append(word)
        return new_arr


    def split_abbreviations(self, arr):
        """split abbrreviaitons into individual characters so it will be sounded out"""
        new_arr = []
        for word in arr:
            if word.isupper():  # all abbrerviations should be all uppercase by this point
                for char in word:
                    new_arr.append(char)
            else:
                new_arr.append(word)
        return new_arr
                
    # convert numbers to words
    # convert words with numbers in them --> SPO2 = SPO two
    # convert pt to PT
    # convert all capital words to SSML to spell out words --> EEG = E E G






        