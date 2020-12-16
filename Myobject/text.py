import pandas as pd
house_data = pd.read_excel('./anjuke.xlsx')
# house_data['发布时间'].fillna(value=house_data['发布时间'].mode, inplace=True)
house_data['设施'].fillna(value=0,inplace=True)
house_data.info()