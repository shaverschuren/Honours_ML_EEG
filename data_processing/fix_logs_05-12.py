import pandas

data_path = '..\\data\\excluded\\logs_2020-05-12_13-13-26\\game.csv'

df = pandas.read_csv(data_path)
df_new = pandas.DataFrame()
df_new['TimeStamp'] = df['TimeStamp']
df_new['correct'] = df['correct']

for i in range(len(df_new)):
    df_new['TimeStamp'][i] = '2020-05-12 13:' + str(df['TimeStamp'][i])

df_new.to_csv(data_path[:-4]+'_2.csv', index=False)