import pandas as pd
import glob

files = glob.glob('data/daily_sales_data_*.csv')
dfs = []
for f in files:
    dfs.append(pd.read_csv(f))

df = pd.concat(dfs, ignore_index=True)
df = df[df['product'] == 'pink morsel'].copy()
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['sales'] = df['price'] * df['quantity']
df = df[['sales', 'date', 'region']]
df.to_csv('output.csv', index=False)
