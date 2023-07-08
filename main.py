import pandas as pd
import re
from sqlalchemy import create_engine

df = pd.read_csv('data.csv', header=None)  # Create dataframe
df.dropna(inplace=True)  # Delete Null elements from df
df.columns = ['brand', 'model', 'year', 'price']  # Create header of df


# Function of Fix format of CamelCase

def camel_case_change(s):
    s = re.sub(r"([a-zа-яё])([A-ZА-ЯЁ@%])", r"\1 \2", s)
    s = re.sub(r"([A-ZА-ЯЁ@%])([0-9])", r"\1 \2", s)
    s = re.sub(r"[@%]", "", s)
    s = re.sub(r"\b\d+\b", lambda m: m.group(0) + " ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"([a-zA-Zа-яА-ЯёЁ]+)([A-ZА-ЯЁ@%][a-zа-яё]+)", r"\1 \2", s)
    return s.strip()


# Function of Fix format of Price
def price_norm(s):
    exchange = 450  # tenge exchange rate
    if '$' in s:
        match = re.search(r'\$\s+(\d+)', s)
        if match:
            number = int(match.group(1))
            result = number * exchange
            return result
    else:
        match = re.search(r'(\d+)', s)
        if match:
            number = int(match.group(1))
            return number

    return None


# Function of Fix format of Year
def year_norm(s):
    match = re.search(r'(\d+)', s)
    if match:
        number = int(match.group(1))
        return number


# Use function of fix data to df
for index, row in df.iterrows():
    row['brand'] = camel_case_change(row['brand'])

    row['model'] = camel_case_change(row['model'])
    row['price'] = price_norm(row['price'])
    row['year'] = year_norm(row['year'])


brand_dict = df['brand'].drop_duplicates().reset_index(drop=True)
model_dict = df['model'].drop_duplicates().reset_index(drop=True)

model_dict_map = (model_dict.reset_index()
                  .assign(index=lambda x: x["index"] + 1)
                  .set_index('model')['index']
                  .to_dict())

brand_dict_map = (brand_dict.reset_index()
                  .assign(index=lambda x: x["index"] + 1)
                  .set_index('brand')['index']
                  .to_dict())

# # Engine for df to db
engine = create_engine('postgresql://user_avencom:@localhost/db_avencom')

# change the name in order to avoid the error

brand_dict.to_sql('brand', engine,  if_exists='append', index=False)
model_dict.to_sql('model', engine,  if_exists='append', index=False)


df['model'] = df['model'].map(model_dict_map)
df['brand'] = df['brand'].map(brand_dict_map)

df.to_sql('auto', engine, if_exists='append', index=False)

print(model_dict.to_string())
print(brand_dict.to_string())