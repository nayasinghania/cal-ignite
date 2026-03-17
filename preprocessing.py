import pandas as pd

df = pd.read_csv("data.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M")
df.sort_values(by=["timestamp"], inplace=True)
df.reset_index(drop=True, inplace=True)

df = df.dropna()

print(df.shape)
print(df.head(5))
print(df.tail(5))
