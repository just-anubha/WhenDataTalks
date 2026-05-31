import pickle
import numpy as np

MODEL_FILE = r'C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\model.pkl'
META_FILE  = r'C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\model_meta.pkl'

with open(MODEL_FILE, 'rb') as f: model = pickle.load(f)
with open(META_FILE,  'rb') as f: meta  = pickle.load(f)

GENRES     = ['Action','Adventure','Animation','Drama','Horror','Romance','Science Fiction','Thriller','Family']
INDUSTRIES = ['Bollywood','Hollywood']
MONTHS     = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

print()
print('=' * 50)
print('  WhenDataTalks - Day 6')
print('  Hit or Flop Predictor')
print(f'  Model accuracy: {meta[chr(97)+chr(99)+chr(99)+chr(117)+chr(114)+chr(97)+chr(99)+chr(121)]*100:.1f}%')
print('=' * 50)

while True:
    print()
    print('  Enter movie details:')

    ind = ''
    while ind not in INDUSTRIES:
        ind = input('  Industry (Bollywood/Hollywood): ').strip().title()

    genre = ''
    print(f'  Genres: {", ".join(GENRES)}')
    while genre not in GENRES:
        genre = input('  Genre: ').strip().title()

    try:
        gross = float(input('  Box office gross in crore INR: '))
        budget = float(input('  Budget in USD (e.g. 15000000): '))
        runtime = int(input('  Runtime in minutes: '))
        popularity = float(input('  Popularity score 0-100: '))
        month = int(input('  Release month 1-12: '))
    except:
        print('  Invalid input, try again.')
        continue

    encoders = meta['encoders']
    ind_enc   = encoders['industry'].transform([ind])[0]   if 'industry' in encoders else 0
    genre_enc = encoders['genre'].transform([genre])[0]    if 'genre'    in encoders else 0

    row = [ind_enc, gross, genre_enc, budget, runtime, popularity, month]
    X   = np.array(row).reshape(1,-1)

    pred   = model.predict(X)[0]
    proba  = model.predict_proba(X)[0]
    conf   = proba[int(pred)] * 100
    bar    = chr(9608) * int(conf/5) + chr(9617) * (20 - int(conf/5))

    print()
    print('  ' + '=' * 46)
    if pred == 1:
        print('    PREDICTION :  HIT  ')
    else:
        print('    PREDICTION :  FLOP  ')
    print(f'    Confidence :  {conf:.1f}%')
    print(f'    [{bar}]')
    print(f'    Industry   :  {ind}')
    print(f'    Genre      :  {genre}')
    print(f'    Gross      :  {gross} crore')
    print(f'    Release    :  {MONTHS.get(str(month), str(month))}')
    print('  ' + '=' * 46)

    again = input('  Predict another? (y/n): ').strip().lower()
    if again != 'y':
        print()
        print('  Thanks! Day 6 complete!')
        break
