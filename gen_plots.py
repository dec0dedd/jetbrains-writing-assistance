import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from pathlib import Path
import os

sns.set_theme()

df = pd.DataFrame()

metric_files = [
    f for f in os.listdir('metric_data') if os.path.isfile(os.path.join('metric_data', f))
]

data_files = [
    f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))
]

print(data_files)

metrics = {}

for file in metric_files:
    pth = os.path.join('metric_data', file)
    stm = Path(file).stem

    df = pd.read_csv(pth, index_col='id').fillna(0)
    metrics[stm] = df

print(metrics)


def generate_plot(mtr: str):
    fig, axs = plt.subplots(len(data_files), 1, figsize=(20, 15), constrained_layout=True)

    for i, file in enumerate(data_files):
        val_lst = []
        mdl_lst = metrics.keys()
        for k in metrics.keys():
            val_lst.append(
                metrics[k][metrics[k]['dataset'] == file][mtr].iloc[0]
            )

        sns.barplot(
            x=val_lst,
            y=mdl_lst,
            ax=axs[i],
            palette=sns.color_palette('deep', len(val_lst))
        )

    return fig, axs


lat_fig, lat_axs = generate_plot('latency')


lat_fig.suptitle('Latency [ms]')
lat_fig.savefig('plots/latency.png')

metr2plot = {
    'latency': 'Latency [ms]',
    'precision': 'Precision',
    'recall': 'Recall',
    'f1': '$F_{1}$ score'
}

for mtr in metr2plot.keys():
    fig, axs = generate_plot(mtr)
    fig.suptitle(metr2plot[mtr])
    fig.savefig(os.path.join('plots', mtr + '.png'))

plt.show()
