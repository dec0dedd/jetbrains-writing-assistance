# Improving Writing Assistance at JetBrains AI

This project aims to explore and evaluate existing spell checking tools on various data.

## 1. Data sources

1. Birkbeck Spelling Error Corpus - [Source](https://www.dcs.bbk.ac.uk/~roger/corpora.html)
2. Holbrook Corpus - [Source](https://www.dcs.bbk.ac.uk/~roger/holbrook-tagged.dat)
3. Aspell Testing Corpus - [Source](https://www.dcs.bbk.ac.uk/~roger/aspell.dat)
4. Wikipedia Misspelings Dataset - [Source](https://www.dcs.bbk.ac.uk/~roger/wikipedia.dat)
5. English Sentences (with randomly introduced errors) - [Source](https://www.kaggle.com/datasets/nikitricky/random-english-sentences)

## 2. Metrics

1. Accuracy
2. Mean Levenshtein distance
3. Median Levenshtein distance
4. Latency
5. Precision
6. Recall
7. $F_{1}$-score

## 3. Tools used for comparison

1. `pyspellchecker` - python spell checker based on Levenshtein distance. [Source](https://github.com/barrust/pyspellchecker?tab=readme-ov-file)
2. `Hunspell` -  an open-source spell checker that supports complex languages and is popular in LibreOffice, OpenOffice, Firefox, and Chrome. It allows custom dictionaries and handles compound words, which makes it suitable for languages with complex morphology. [Source](https://github.com/hunspell/hunspell)
(Note: In order to use it with Python, I've used library `pyhunspell` available [here](https://github.com/pyhunspell/pyhunspell))
3. Vennify's T5 Grammar Correction transformer - [Source](https://huggingface.co/vennify/t5-base-grammar-correction)
4. `SymSpell` - [Source](https://github.com/wolfgarbe/SymSpell)
5. `TextBlob` - [Source](https://github.com/sloria/TextBlob)

## 4. Results

- .
- .
- .