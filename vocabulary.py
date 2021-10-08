import random
import json
import os
from learned import ProgressHandler
from datetime import datetime


startTime = datetime.now()
total_attempts = 0
total_correct = 0
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def print_session_stats():
    print("Goodbye!\n*******************\n")
    correct_p = int(total_correct*100/total_attempts) if total_attempts else 0
    print(f"""
        total attempts: {total_attempts}\n
        correct answers: {total_correct}\n
        correct answers %: {correct_p}%\n
        time: {datetime.now() - startTime}
    """)

def reload_words_progress():
    num_dict = list(enumerate(sorted([(cat, float(handler.get_update_category_progress(cat))) for cat in dictionary.keys()], key=lambda tup: tup[1], reverse=True)))
    return num_dict

def handle_target(target, category, words):
    below_target_words = set(words.keys())
    below_target_words_copy = below_target_words.copy()
    while below_target_words:
        print(f"Remaining words:")
        for word in below_target_words:
            word_p = handler.get_word_progress(word)
            if (word_p >= target):
                below_target_words_copy.remove(word)
            else:
                print(f"{word}: {word_p}")
        print("\n")
        below_target_words = below_target_words_copy.copy()
        
        handle_translation_learn(list(below_target_words), target)
    print(f"Done! All words have {target} or more!")

def handle_words(keys):
    print(len(keys))
    count = 0
    score  = 0
    wrong_words = []
    global total_correct
    global total_attempts
    random.shuffle(keys)
    for key in keys:
        count += 1
        print(f"{count}. {key}")
        translation_input = input (f"-- ").lower()
        correct_answer = words.get(key)
        if translation_input == correct_answer.lower():
            print("Correct!\n")
            score += 1
            total_correct += 1
            handler.update_score(key)
        else:
            print(f"Wrong: {correct_answer.upper()}\n")
            wrong_words.append((key, translation_input))
            handler.update_score(key, correct=False)
        total_attempts += 1
    return wrong_words


def handle_translation_learn(keys, target):
    handle_words(keys)
    print(f"You are {handler.get_category_progress(selected_category, target=target)} % done")
    


def handle_translation_regular(keys):
    _contionue_words = True
    while _contionue_words:
        wrong_words = handle_words(keys)

        # Results
        total_words = len(wrong_words) + score
        score_p = int(score * 100/total_words) if total_words else 0
        print(f"\n\n*****************************\nDone! Your score is: {score}/{total_words} ({score_p}%)\nYou learned {handler.get_update_category_progress(selected_category)} % words in this category.")

        if len(wrong_words):
            print("\n\nHere are the words that you got wrong:\n")
            for guess in wrong_words:
                print(f"{guess[0]}\nyou: {guess[1]}, correct:{words.get(guess[0])}\n")
        while True:
            desision = input(f"\'Y\' to continue, \'N\' to chose another category: ").lower().strip()
            if desision == "y":
                break
            elif desision == "n":
                _contionue_words = False
                break
            else:
                continue



# Load all words
with open(__location__ + '/words.json') as json_file:
    dictionary = json.load(json_file)
    handler = ProgressHandler(dictionary)

try:
    # Handle categories
    _contionue_categories = True
    while _contionue_categories:
        print("Select a category from the following:")
        num_dict = reload_words_progress()
        for num, (category, score) in num_dict:
            print(f"{num}.\t({len(dictionary.get(category))} w,\t{score} %) \t{category}")
        words = []
        while not words:
            try:
                user_input = input("-- ").split()
                selected_category_num = int(user_input[0])
                selected_category = num_dict[selected_category_num][1][0]
                words = dictionary.get(selected_category)
            except Exception:
                continue
            if len(user_input) >= 2:
                option = user_input[1]
                if option.isnumeric():
                    target = int(option)
                    try:
                        handle_target(target=target, category=selected_category, words=words)
                        words = []
                        break
                    except KeyboardInterrupt:
                        words = []
                        break
                elif option == "scores":
                    for w in words:
                        print(f"{handler.get_word_progress(w)}:\t{w}")
                    input("")
                    words = []
                    break
                else:
                    words = []
                    break

            else:
                print(f"""You selected \'{selected_category}\' which contains {len(dictionary.get(selected_category))} words.
                    \n--------------------------------------------
                    \n\nEnter the translation of the following words:
                """)

        if words:
            # Handle words of chosen category
            shuffled_keys = [k for k in words.keys()]
            handle_translation_regular(shuffled_keys)

except KeyboardInterrupt:
    handler.dump_data()
    print_session_stats()


