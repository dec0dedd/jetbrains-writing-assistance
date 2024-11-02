
import pandas as pd

df = pd.DataFrame()


def parse(filepath):
    data = {}
    c_key = None

    with open(filepath, 'r') as file:
        for ln in file:
            ln = ln.strip()

            if ln.startswith('$'):
                c_key = ln[1:]
                data[c_key] = []
            else:
                assert c_key is not None
                data[c_key].append(ln)

    return data


dic = parse("data/wikipedia/data.dat")

i = 1
for key in dic.keys():
    for mis in dic[key]:
        df = pd.concat(
            [
                df,
                pd.DataFrame({"id": i, "wrong": mis.lower(), "correct": key.lower()}, index=[0])
            ]
        )

        i += 1

df.set_index('id', inplace=True)
print(df)

df.to_csv("data/wikipedia.csv", index=True)
