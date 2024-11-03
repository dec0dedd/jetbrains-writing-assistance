from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
from tqdm import tqdm

from utils import dist, get_matrix

import os
import time

files = [
    'aspell.csv',
    'birkbeck.csv',
    'holbrook.csv',
    'wikipedia.csv',
    'sentences.csv'
]

tqdm.pandas()

tokenizer = T5Tokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = T5ForConditionalGeneration.from_pretrained("vennify/t5-base-grammar-correction")


def correction(x):
    input_ids = tokenizer(
        "correct: " + x['wrong'],
        return_tensors="pt"
    ).input_ids

    output_ids = model.generate(
        input_ids,
        max_length=512,
        num_beams=4,
        early_stopping=True
    )

    res = tokenizer.decode(output_ids[0], skip_special_tokens=True).replace('correct: ', '').lower()
    return res


metrics = pd.DataFrame()


for i, fn in enumerate(files):
    path = os.path.join('data', fn)
    df = pd.read_csv(path, index_col='id')
    df = df.sample(min(df.shape[0], 50)).dropna(axis=0)

    start = time.time_ns()
    df['correction'] = df.progress_apply(correction, axis=1)
    end = time.time_ns()

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
            "latency": ((end-start)/df.shape[0])/(10**6),
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

metrics.to_csv('metric_data/t5.csv', index=True)
print(metrics)
