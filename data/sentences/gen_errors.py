import random

random.seed(42)


def introduce_typos(sentence, error_rate):
    words = sentence.split()
    for i in range(len(words)):
        if random.random() < error_rate:
            if (len(words[i])) <= 1:
                continue

            idx = random.randint(0, len(words[i]) - 1)
            char = str(random.choice('abcdefghijklmnopqrstuvwxyz'))
            words[i] = words[i][:idx] + char + words[i][idx + 1:]
    return ' '.join(words)


res = ""
with open("data/sentences/data.dat", 'r') as fl:
    for line in fl.readlines():
        res += introduce_typos(line, 0.25) + "\n"

with open("data/sentences/data_error.dat", "w") as fl:
    fl.write(res)
