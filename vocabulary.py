import random
import json
from learned import ProgressHandler

QUIT = "quit()"

total_attempts = 0
total_correct = 0


def print_session_stats():
    print("Goodbye!\n*******************\n")
    correct_p = int(total_correct*100/total_attempts) if total_attempts else 0
    print(f"""
        total attempts: {total_attempts}\n
        correct answers: {total_correct}\n
        correct answers %: {correct_p}%\n
    """)


# Load all words
with open('words.json') as json_file:
    dictionary = json.load(json_file)
    num_dict = list(enumerate(dictionary.keys()))
    handler = ProgressHandler(dictionary)

try:
    # Handle categories
    _contionue_categories = True
    while _contionue_categories:
        print("Select a category from the following:")
        for num, category in num_dict:
            print(f"{num}. {category}\t\t({len(dictionary.get(category))} w,\t{handler.get_progress(category)} %)")
        words = []
        while not words:
            try:
                selected_category_num = int(input("-- "))
                selected_category = num_dict[selected_category_num][1]
                words = dictionary.get(selected_category)
                print(f"""You selected \'{selected_category}\' which contains {len(dictionary.get(selected_category))} words.
                    \n--------------------------------------------
                    \n\nEnter the translation of the following words:
                """)
            except Exception:
                print("Enter the number of category to continue.")

        # Handle words of chosen category
        shuffled_keys = [k for k in words.keys()]
        _contionue_words = True

        while _contionue_words:
            count = 0
            score  = 0
            wrong_words = []
            random.shuffle(shuffled_keys)
            for key in shuffled_keys:
                count += 1
                print(f"{count}. {key}")
                translation_input = input (f"-- ").lower()
                correct_answer = words.get(key)
                if translation_input == QUIT:
                    _contionue_words = False
                    break
                elif translation_input == correct_answer.lower():
                    print("Correct!\n")
                    score += 1
                    total_correct += 1
                    handler.update_word(key)
                else:
                    print(f"Wrong: {correct_answer.upper()}\n")
                    wrong_words.append((key, translation_input))
                total_attempts += 1

            # Results
            total_words = len(wrong_words) + score
            score_p = int(score * 100/total_words) if total_words else 0
            print(f"\n\n*****************************\nDone! Your score is: {score}/{total_words} ({score_p}%)\nYou learned {handler.get_progress(selected_category)} % words in this category.")

            if len(wrong_words):
                print("\n\nHere are the words that you got wrong:\n")
                for guess in wrong_words:
                    print(f"{guess[0]}\nyou: {guess[1]}, correct:{words.get(guess[0])}\n")
            while True:
                desision = input(f"\'Y\' to continue, \'N\' to chose another category, \'{QUIT}\' to quit: ").lower().strip()
                if desision == "y":
                    break
                elif desision == "n":
                    _contionue_words = False
                    break
                elif desision == QUIT:
                    _contionue_words = False
                    _contionue_categories = False
                    print_session_stats()
                    break
                else:
                    continue
except KeyboardInterrupt:
    handler.dump_data()
    print_session_stats()
