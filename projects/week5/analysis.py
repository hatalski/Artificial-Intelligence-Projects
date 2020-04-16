import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')

df_2048 = pd.read_csv("_moves_1584858945.0303512.csv")

print(df_2048.info())
features = df_2048[["monotonic", "merge_score",
         "center_edges_diff", "max_tile_in_corner"]]
features_perc = features.divide(features.sum(axis=1), axis=0)
print(features_perc.head())
#df_2048["total"].plot(kind="line")
features_perc.plot.area(stacked=False)
plt.show()
