from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
from tqdm import tqdm
from Levenshtein import distance

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

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


def dist(x):
    return distance(x['wrong'], x['correct'])


metrics = pd.DataFrame()


for i, fn in enumerate(files):
    path = os.path.join('data', fn)
    df = pd.read_csv(path, index_col='id')
    df = df.sample(min(df.shape[0], 10))

    start = datetime.now()
    df['correction'] = df.progress_apply(correction, axis=1)
    end = datetime.now()

    df['edit'] = df.apply(dist, axis=1)
    df['ans'] = df['correct'] == df['correction']
    df['cor_len'] = df['correct'].apply(len)

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

metrics.to_csv('metric_data/t5.csv', index=True)
print(metrics)
