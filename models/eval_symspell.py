from symspellpy import SymSpell, Verbosity
import pandas as pd
from tqdm import tqdm
import pkg_resources

from utils import get_matrix, dist

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
    res = []
    for word in x['wrong'].split():
        lst = symspell.lookup(word, Verbosity.ALL, max_edit_distance=2)

        if len(lst):
            res.append(lst[0].term)
        else:
            res.append('$')

    return ' '.join(res)


metrics = pd.DataFrame()


for i, fn in enumerate(files):
    path = os.path.join('data', fn)
    df = pd.read_csv(path, index_col='id')
    df = df.sample(min(df.shape[0], 5000))

    start = datetime.now()
    df['correction'] = df.progress_apply(correction, axis=1)
    end = datetime.now()

    df['edit'] = df.progress_apply(dist, axis=1)
    df['ans'] = df['correct'] == df['correction']
    df['cor_len'] = df['correct'].progress_apply(len)

    t_pos, f_pos, t_neg, f_neg = [[], [], [], []]
    for a, b, c, d in df.apply(get_matrix, axis=1):
        t_pos.append(a), f_pos.append(b), t_neg.append(c), f_neg.append(d)
    df['TP'], df['FP'], df['TN'], df['FN'] = t_pos, f_pos, t_neg, f_neg

    print(df)

    m_df = pd.DataFrame(
        {
            "latency": ((end-start)/df.shape[0]).total_seconds()/df.shape[0],
            "lev_edit_mean": (df['edit']/df['cor_len']).mean(),
            "lev_edit_median": (df['edit']/df['cor_len']).quantile(0.5),
            "TP": df['TP'].sum(),
            "FP": df['FP'].sum(),
            "TN": df['TN'].sum(),
            "FN": df['FN'].sum(),
        },
        index=[0]
    )

    m_df['precision'] = (m_df['TP'])/(m_df['TP']+m_df['FP'])
    m_df['recall'] = (m_df['TP'])/(m_df['TP']+m_df['TN'])
    m_df['f1'] = 2 * (m_df['precision']*m_df['recall'])/(m_df['precision']+m_df['recall'])
    m_df['accuracy'] = (m_df['TP']+m_df['TN'])/(m_df['TP']+m_df['TN']+m_df['FN']+m_df['FP'])

    m_df['dataset'] = fn
    m_df['id'] = i

    m_df.set_index('id', inplace=True)
    metrics = pd.concat([metrics, m_df])


metrics.to_csv('metric_data/symspell.csv', index=True)
print(metrics)
