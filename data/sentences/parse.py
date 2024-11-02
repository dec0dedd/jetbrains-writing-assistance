from io import StringIO

import pandas as pd

res = pd.DataFrame()

with open('data/sentences/data_error.dat', 'r') as file:
    df = pd.read_csv(
        StringIO(
            file.read().replace('\n', ',').replace(',,', '\n')
        ),
        header=None
    ).T

    df = df[:df.shape[0]-1]
    res['wrong'] = df[0]

with open('data/sentences/data.dat', 'r') as file:
    df = pd.read_csv(
        StringIO(
            file.read().replace('\n', ',').replace(',,', '\n')
        ),
        header=None
    ).T

    df = df[:df.shape[0]-1]
    res['correct'] = df[0]

res['id'] = pd.RangeIndex(start=0, stop=res.shape[0])
res.set_index('id', inplace=True)

res.to_csv('data/sentences.csv', index=True)
print(res)
