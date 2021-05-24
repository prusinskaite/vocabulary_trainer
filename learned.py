import json

LEARNED_WORDS_FILE = 'learned_words.json'
LEARNED_WORDS = "learned_words"
CATEGORY_SCORE = "categories_score"
LEARNED_THRESHOLD = 10
MAX_SCORE = 12
MIN_SCORE = 0

class ProgressHandler():

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.load_data()

    def load_data(self):
        with open(LEARNED_WORDS_FILE) as json_file:
            self.json_data = json.load(json_file)
            self.words = self.json_data[LEARNED_WORDS]
            self.categories = self.json_data[CATEGORY_SCORE]
           
    def dump_data(self):
        with open(LEARNED_WORDS_FILE, "w") as jsonFile:
            self.json_data[LEARNED_WORDS] = self.words
            self.json_data[CATEGORY_SCORE] = self.categories
            json.dump(self.json_data, jsonFile, sort_keys=True, indent=4)

    def update_score(self, word, correct=True):
        current_score = self.words.get(word)
        if correct:
            if current_score and current_score < MAX_SCORE:
                self.words[word] = current_score + 1
            elif not current_score:
                self.words[word] = 1
        else:
            if current_score and current_score > MIN_SCORE:
                self.words[word] = current_score - 1
            elif current_score != None and current_score == (MIN_SCORE + 1):
                del self.words[word]
        self.dump_data()

    def update_progress(self):
        for category in self.dictionary:
            _words = self.dictionary.get(category).keys()
            score = 0
            for word in self.words.keys():
                if word in _words:
                    word_score = self.words.get(word)
                    if word_score and word_score >= MIN_SCORE:
                        if word_score and word_score >= LEARNED_THRESHOLD:
                            score += 1
                        else:
                            score += (word_score/LEARNED_THRESHOLD)
            if score:
                self.categories[category] = "%.1f" % (score*100/len(_words))
        self.dump_data()


    def get_progress(self, category):
        self.update_progress()
        progress = self.categories.get(category)
        return progress or MIN_SCORE
