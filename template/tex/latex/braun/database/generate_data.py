import pandas as pd

thermochemical_df = pd.read_csv('braundb/braundb.modules/braundb.data/thermochemical.csv', index_col=0)

for substance, properties in thermochemical_df.iterrows():
    print(properties)