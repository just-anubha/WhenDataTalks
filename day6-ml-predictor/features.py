import numpy as np

def convert_budget_usd_to_inr(budget_usd):
    return budget_usd * 83

def compute_roi(gross, budget_inr):
    return gross / (budget_inr + 1e-6)

def runtime_score(runtime):
    if runtime < 80:
        return 0.3
    elif runtime <= 150:
        return 1.0
    elif runtime <= 180:
        return 0.8
    return 0.5

def month_score(month):
    return {
        1: 0.7, 2: 0.6, 3: 0.7, 4: 0.8,
        5: 0.9, 6: 0.8, 7: 1.0, 8: 0.9,
        9: 0.6, 10: 0.7, 11: 0.9, 12: 1.0
    }.get(month, 0.7)

def build_features(ind_enc, genre_enc, gross, budget_usd, runtime, popularity, month):

    budget_inr = convert_budget_usd_to_inr(budget_usd)
    profit = gross - budget_inr
    roi = compute_roi(gross, budget_inr)

    return np.array([[
        ind_enc,
        genre_enc,
        gross,
        budget_inr,
        profit,
        roi,
        runtime_score(runtime),
        popularity,
        month_score(month)
    ]])