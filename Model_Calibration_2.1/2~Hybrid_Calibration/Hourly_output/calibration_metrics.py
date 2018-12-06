import pandas as pd
import numpy as np

def get_NMBE(v_truth, v_predict):
    return abs(np.sum(v_truth - v_predict) / ((len(v_truth) - 1) * np.mean(v_truth))) * 100

def get_CV_RMSE(v_truth, v_predict):
    from math import sqrt
    return sqrt(np.sum((v_truth - v_predict) ** 2 / (len(v_truth) - 1))) / np.mean(v_truth) * 100


# df = pd.read_csv("hourly_conusmption.csv")
df = pd.read_csv("hourly_conusmption_no_HM.csv")

print(df.columns)


v_e_c = df['Electricity-calibrated']
v_e_t = df['Electricity-truth']

v_g_c = df['Gas-calibrated']
v_g_t = df['Gas-truth']

print(get_NMBE(v_e_c, v_e_t))
print(get_CV_RMSE(v_e_c, v_e_t))
print(get_NMBE(v_g_c, v_g_t))
print(get_CV_RMSE(v_g_c, v_g_t))