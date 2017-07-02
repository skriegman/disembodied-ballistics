import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

sns.set(color_codes=True, context="poster")
sns.set_style("ticks", {'font.family': 'serif', 'font.serif': 'Times New Roman'})
sns.set_palette("Set2", 8)


results = pd.DataFrame()
for seed in range(1, 31):
    this_run = pd.read_csv("results/results_{}.csv".format(seed))
    results = pd.concat([results, this_run])

f, axes = plt.subplots(1, 1, figsize=(7, 6))

g = sns.tsplot(data=results, value="Time", condition="Group", unit="Run", time="Interval", ax=axes,
               err_style="unit_traces", estimator=np.median)

axes.legend([mpatches.Patch(color=sns.color_palette()[i]) for i in range(2)], [r'E', r'D'], loc=1)

axes.set_xlim([0, 2])
axes.set_xlabel(r"Half interval size $(\mathregular{I}/2)$")
axes.set_ylabel("Log Generations")
axes.set_yscale('log')

plt.title(r"Disembodied search in ${\rm I\!R}^{48}$")
sns.despine(ax=axes)
plt.tight_layout()
plt.savefig("plots/ballistic_search_log.pdf", bbox_inches='tight')
