import random

random.seed(42)


def introduce_typos(sentence, error_rate=0.1):
    words = sentence.split()
    for i in range(len(words)):
        if random.random() < error_rate:
            # Randomly choose to misspell the word
            if len(words[i]) > 1:  # Avoid one-letter words
                typo_index = random.randint(0, len(words[i]) - 1)
                typo_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                # Create a typo by replacing one character
                words[i] = words[i][:typo_index] + typo_char + words[i][typo_index + 1:]
    return ' '.join(words)


res = ""
with open("data/sentences/data.dat", 'r') as fl:
    for line in fl.readlines():
        res += introduce_typos(line, 0.2) + "\n"

with open("data/sentences/data_error.dat", "w") as fl:
    fl.write(res)
