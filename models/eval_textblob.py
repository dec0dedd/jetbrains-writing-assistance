from textblob import TextBlob
import pandas as pd
from tqdm import tqdm

from utils import get_matrix, dist

import os
from datetime import datetime

files = [
    'aspell.csv',
    'birkbeck.csv',
    'holbrook.csv',
    'wikipedia.csv',
    'sentences.csv'
]

tqdm.pandas()


def correction(x):
    res = [i.lower() for i in TextBlob(x['wrong']).correct().split()]
    return ' '.join(res)


metrics = pd.DataFrame()


for i, fn in enumerate(files):
    path = os.path.join('data', fn)
    df = pd.read_csv(path, index_col='id')
    df = df.sample(min(df.shape[0], 5000))

    start = datetime.now()
    df['correction'] = df.progress_apply(correction, axis=1)
    end = datetime.now()

    df['edit'] = df.apply(dist, axis=1)
    df['ans'] = df['correct'] == df['correction']
    df['cor_len'] = df['correct'].apply(len)

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
            "FN": df['FN'].sum()
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

metrics.to_csv('metric_data/textblob.csv', index=True)
print(metrics)
