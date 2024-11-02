from symspellpy import SymSpell, Verbosity
import pandas as pd
from tqdm import tqdm
import pkg_resources
from Levenshtein import distance

import os
from datetime import datetime

symspell = SymSpell()

dict_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)

symspell.load_dictionary(dict_path, 0, 1)

files = [
    'aspell.csv',
    'birkbeck.csv',
    'holbrook.csv',
    'wikipedia.csv',
    'sentences.csv'
]

tqdm.pandas()


def correction(x):
    lst = symspell.lookup(x['wrong'], Verbosity.ALL, max_edit_distance=2)

    if len(lst):
        return lst[0].term
    else:
        return "$"


def dist(x):
    return distance(x['wrong'], x['correct'])


metrics = pd.DataFrame()


for i, fn in enumerate(files):
    path = os.path.join('data', fn)
    df = pd.read_csv(path, index_col='id')
    df = df.sample(min(df.shape[0], 1500))

    start = datetime.now()
    df['correction'] = df.progress_apply(correction, axis=1)
    end = datetime.now()

    df['edit'] = df.progress_apply(dist, axis=1)
    df['ans'] = df['correct'] == df['correction']
    df['cor_len'] = df['correct'].progress_apply(len)

    m_df = pd.DataFrame(
        {
            "latency": ((end-start)/df.shape[0]).total_seconds(),
            "accuracy": df['ans'].sum()/df.shape[0],
            "lev_edit_mean": (df['edit']/df['cor_len']).mean(),
            "lev_edit_median": (df['edit']/df['cor_len']).quantile(0.5)
        },
        index=[0]
    )

    m_df['dataset'] = fn
    m_df['id'] = i

    m_df.set_index('id', inplace=True)
    metrics = pd.concat([metrics, m_df])


metrics.to_csv('metric_data/symspell.csv', index=True)
print(metrics)
