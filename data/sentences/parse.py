import pandas as pd

res = pd.DataFrame()

with open('data/sentences/data_error.dat', 'r') as file:
    lst = []
    for ln in file.readlines():
        lst.append(ln.replace('\n', '').lower())

    res['wrong'] = lst

with open('data/sentences/data.dat', 'r') as file:
    lst = []
    for ln in file.readlines():
        lst.append(ln.replace('\n', '').lower())

    res['correct'] = lst

res['id'] = pd.RangeIndex(start=0, stop=res.shape[0])
res.set_index('id', inplace=True)

res.to_csv('data/sentences.csv', index=True)
print(res)
