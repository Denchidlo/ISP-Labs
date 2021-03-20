# import tasks.AbstractTask as base
import copy

class Task1:
    def __init__(self):
        self.text_dict = dict() 
        return
    
    def run_task(self):
        self.get_text_info()

    def set_text(self, text):
        self.text = text
        return

    def analyse(self):
        sentences = self.__split_in_sentences(self.__format_text(self.text, "\r\t\n"), ".?!")
        sentence_dict = {"word_count":[], "text":[], "length":0}
        for sentence in sentences:
            counter = 0
            formated_sentence = self.__format_text(sentence, "{\\}|<>#^,.!&?[]():;\'\"-*@\n\t\r")
            formated_sentence = formated_sentence.lower()
            for word in formated_sentence.split(" "):
                if word == '':
                    continue
                else:
                    counter += 1
            sentence_dict["text"].append(sentence)
            sentence_dict["word_count"].append(counter)
            sentence_dict["length"] = len(sentences)
        self.text_dict.update({"sentences":sentence_dict})
        for i in range(sentence_dict["length"]):
            print("{word_amount} {sentence}".format(word_amount=self.text_dict["sentences"]["word_count"][i], sentence=self.text_dict["sentences"]["text"][i]))
        return

    def get_text_info(self):
        
        print(self.text_dict["sentences"])
        return

    def word_statistic(self):
        word_dict = {}
        formated_text = self.__format_text(self.text, "{\\}|<>#^,.!&?():;\'\"-*@\n\t\r")
        formated_text = formated_text.lower()
        for word in formated_text.split(" "):
            if word == '':
                continue
            else:
                if word_dict.get(word) != None:
                    word_dict.update({word:word_dict[word] + 1})
                else:
                    word_dict.update({word:1})
        print(word_dict)
        return 

    def __format_text(self, text, sym_ignored):
        result = text
        for sym in sym_ignored:
            result = result.replace(sym, "")
        return result

    def __split_in_sentences(self, text, sep_list):
        sentence_sequence = [text]
        for sep in sep_list:
            subsequences = []
            temp_sequence = []
            for sentence in sentence_sequence:
                subsequences.append(sentence.split(sep + " "))
            for seq in subsequences:
                temp_sequence += seq
            sentence_sequence = temp_sequence
        return sentence_sequence