"""abstract Preprocessor class and inheriting EMSPreprocessor"""
from abc import ABC, abstractmethod

class Preprocessor(ABC):

    @abstractmethod
    def process(self, text):
        """method that contains runs all components of specified pipeline on inputted text"""
        pass



class EMSPreprocessor(Preprocessor):

    def process(self, text):
        return super().process(text)

    # convert numbers to words
    # convert words with numbers in them --> SPO2 = SPO two
    # 






        