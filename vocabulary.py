import random

import json

with open('words.json') as json_file:
    words = json.load(json_file)

shuffled_keys = [k for k in words.keys()]
random.shuffle(shuffled_keys)
score  = 0
wrong_words = []
count = 0

for key in shuffled_keys:
    count += 1
    print(f"{count}. {key}")
    translation_input = input (f"-- ")
    correct_answer = words.get(key)
    if translation_input == "quit()":
        break
    elif translation_input.lower() == correct_answer.lower():
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong: {correct_answer.upper()}\n")
        wrong_words.append((key, translation_input))

total_words = len(wrong_words) + score
print(f"\n\n*****************************\nDone! Your score is: {score}/{total_words} ({int(score * 100/total_words)}%)")

if len(wrong_words):
    print("\n\nHere are the words that you got wrong:\n")
    for guess in wrong_words:
        print(f"{guess[0]}\nyou: {guess[1]}, correct:{words.get(guess[0])}\n")
