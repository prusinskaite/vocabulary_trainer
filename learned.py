import json


# TODO: save words that I got right 10 times, calculate % of learned words for each category


class ProgressHandler():

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.load_data()

    def load_data(self):
        with open('learned_words.json') as json_file:
            self.json_data = json.load(json_file)
            self.words = self.json_data["learned_words"]
            self.categories = self.json_data["categories_score"]
           
    def dump_data(self):
        with open('learned_words.json', "w") as jsonFile:
            self.json_data["learned_words"] = self.words
            self.json_data["categories_score"] = self.categories
            json.dump(self.json_data, jsonFile, sort_keys=True, indent=4)

    def update_word(self, word):
        ex = self.words.get(word)
        self.words[word] = (ex if ex else 0) + 1
        self.dump_data()

    def update_progress(self):
        for category in self.dictionary:
            _words = self.dictionary.get(category).keys()
            score = 0
            for word in self.words.keys():
                if word in _words:
                    word_score = self.words.get(word)
                    if word_score and word_score>=0:
                        if word_score and word_score >= 10:
                            score += 1
                        else:
                            score += (word_score/10)
            if score:
                self.categories[category] = "%.1f" % (score*100/len(_words))
        self.dump_data()


    def get_progress(self, category):
        self.update_progress()
        progress = self.categories.get(category)
        return progress or 0
