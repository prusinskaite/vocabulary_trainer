import random
import json

QUIT = "quit()"

total_attempts = 0
total_correct = 0
words_learned = set()


def print_session_stats():
    print("Goodbye!\n*******************\n")
    correct_p = int(total_correct*100/total_attempts) if total_attempts else 0
    print(f"""
        total attempts: {total_attempts}\n
        correct answers: {total_correct}\n
        correct answers %: {correct_p}%\n
        # words learned: {len(words_learned)} ({words_learned})
    """)


# Load all words
with open('words.json') as json_file:
    dictionary = json.load(json_file)


# Handle categories
_contionue_categories = True
while _contionue_categories:
    print("Select a category from the following:")
    for category in dictionary.keys():
        print(f"{category} ({len(dictionary.get(category))})")
    words = []
    while not words:
        selected_category = input("-- ").lower()
        if selected_category == QUIT:
            _contionue_words = False
            _contionue_categories = False
            break
        words = dictionary.get(selected_category)
        if not words:
            print("Enter the name of category to continue.")


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
                words_learned.add(translation_input)
            else:
                print(f"Wrong: {correct_answer.upper()}\n")
                wrong_words.append((key, translation_input))
            total_attempts += 1

        # Results
        total_words = len(wrong_words) + score
        score_p = int(score * 100/total_words) if total_words else 0
        print(f"\n\n*****************************\nDone! Your score is: {score}/{total_words} ({score_p}%)")

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
            elif desision == QUIT:
                _contionue_words = False
                _contionue_categories = False
                print_session_stats()
                break
            else:
                continue


