import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"C:\Users\KIIT\Desktop\WHENDATATALKS\data\combined.csv")

def extract_number(s):
    s = str(s).strip().replace('crore','').replace('$','').strip()
    m = re.search(r'[\d.]+', s)
    return float(m.group()) if m else None

def clean_gross(raw, ind):
    if pd.isna(raw): return np.nan
    raw = re.sub(r'[A-Za-z]+\$', '$', str(raw))
    raw = re.sub(r'\[.*?\]', '', raw).replace('₹','').replace(',','').strip()
    raw = raw.replace('–','-').replace('—','-')
    parts = raw.split('-') if '-' in raw else [raw]
    nums = [extract_number(p) for p in parts]
    nums = [n for n in nums if n]
    v = np.mean(nums) if nums else np.nan
    if v and ind=='Hollywood' and v>10000: v=(v*83)/1e7
    return round(v,2) if v else np.nan

GENRES = {
    'Action':['war','tiger','jawan','animal','salaar','devara','simmba','saaho','vikram','leo','coolie','border','spider','skyfall','rogue','deadpool','captain','iron man','transformers','batman'],
    'Adventure':['avengers','star wars','jurassic','pirates','furious','top gun'],
    'Animation':['toy story','frozen','minions','aladdin','lion king','moana','incredibles','mario','inside out','zootopia'],
    'Drama':['titanic','joker','pk','3 idiots','dangal','sanju','secret superstar','andhadhun','kalki','chhaava'],
    'Horror':['bhool bhulaiyaa','stree'],
    'Romance':['chennai express','barbie','padmaavat'],
    'Science Fiction':['avatar','2.0','brahmastra','ne zha'],
    'Thriller':['dhoom','baahubali','rrr','pushpa','kgf','kantara','ponniyin','harry potter']
}

def get_genre(t):
    t = t.lower()
    for g, kws in GENRES.items():
        if any(k in t for k in kws): return g
    return 'Action'

df['year'] = pd.to_numeric(df['year'].astype(str).apply(lambda x: re.sub(r'\[.*?\]','',x).strip()), errors='coerce')
df['gross_crore'] = df.apply(lambda r: clean_gross(r['worldwide_gross'], r['industry']), axis=1)
df.dropna(subset=['gross_crore'], inplace=True)

try:
    en = pd.read_csv(r"C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\movies_ml.csv")
    en = en[['title','genre','budget_usd','runtime','popularity','month']]
    df = df.merge(en, on='title', how='left')
    print(f"Merged existing TMDB data")
except:
    df['genre']=np.nan; df['budget_usd']=0; df['runtime']=0; df['popularity']=0; df['month']=6

df.loc[df['genre'].isna(), 'genre'] = df.loc[df['genre'].isna(), 'title'].apply(get_genre)

for col in ['budget_usd','runtime','popularity','month']:
    for ind in df['industry'].unique():
        mask = (df['industry']==ind) & (df[col].isna() | (df[col]==0))
        df.loc[mask, col] = df.loc[df['industry']==ind, col].median()

df['label'] = 0
for ind in df['industry'].unique():
    mask = df['industry'] == ind
    df.loc[mask & (df['gross_crore'] >= df.loc[mask,'gross_crore'].median()), 'label'] = 1

final = df[['title','industry','year','gross_crore','genre','budget_usd','runtime','popularity','month','label']].copy()
final.dropna(subset=['gross_crore','genre'], inplace=True)
final.reset_index(drop=True, inplace=True)
final.to_csv(r"C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\movies_ml.csv", index=False)

print("=" * 55)
print("  Day 6 - Dataset Ready!")
print("=" * 55)
print(f"  Rows   : {len(final)}")
print(f"  Hits   : {int(final.label.sum())}  ({final.label.mean()*100:.0f}%)")
print(f"  Flops  : {int((final.label==0).sum())}  ({(1-final.label.mean())*100:.0f}%)")
print()
print(final[['title','industry','genre','gross_crore','label']].head(10).to_string(index=False))
print("=" * 55)
print("Done! Run train.py next.")
