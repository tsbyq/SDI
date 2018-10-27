import pandas as pd
import numpy as np
from ggplot import *
import matplotlib.pyplot as plt


def get_NMBE(v_truth, v_predict):
    return abs(np.sum(v_truth - v_predict) / ((len(v_truth) - 1) * np.mean(v_truth))) * 100

def get_CV_RMSE(v_truth, v_predict):
    from math import sqrt
    return sqrt(np.sum((v_truth - v_predict) ** 2 / (len(v_truth) - 1))) / np.mean(v_truth) * 100


def plot_monthly_consumption(file_0, file_1, file_2):
    df_b = pd.read_csv(file_0)
    df_c = pd.read_csv(file_1)
    df_t = pd.read_csv(file_2)

    col_names = ['Month', 'Annual Electricity (kWh)','Annual Natural Gas (Therms)']
    df_b.columns = col_names
    df_c.columns = col_names
    df_t.columns = col_names

    df_b['Month'] = range(1,13)
    df_c['Month'] = range(1,13)
    df_t['Month'] = range(1,13)

    df_b['Model'] = 'Baseline'
    df_c['Model'] = 'Calibrating'
    df_t['Model'] = 'Target'

    df_b['Annual Electricity (kWh)'] /= 3600000
    df_b['Annual Natural Gas (Therms)'] *= 9.48043e-9
    df_c['Annual Electricity (kWh)'] /= 3600000
    df_c['Annual Natural Gas (Therms)'] *= 9.48043e-9
    df_t['Annual Electricity (kWh)'] /= 3600000
    df_t['Annual Natural Gas (Therms)'] *= 9.48043e-9

    df = df_b
    df = df.append(df_c, ignore_index=True)
    df = df.append(df_t, ignore_index=True)


    df_cc = df.loc[df['Model'] == 'Calibrating']
    df_tt = df.loc[df['Model'] == 'Target']

    v_target_E = np.array(df_tt['Annual Electricity (kWh)'])
    v_calibrating_E = np.array(df_cc['Annual Electricity (kWh)'])
    v_target_NG = np.array(df_tt['Annual Natural Gas (Therms)'])
    v_calibrating_NG = np.array(df_cc['Annual Natural Gas (Therms)'])

    NMBE_E = get_NMBE(v_target_E, v_calibrating_E)
    CV_RMSE_E = get_CV_RMSE(v_target_E, v_calibrating_E)

    NMBE_NG = get_NMBE(v_target_NG, v_calibrating_NG)
    CV_RMSE_NG = get_CV_RMSE(v_target_NG, v_calibrating_NG)


    # Plot
    # Electricity
    fig, ax = plt.subplots()
    fig.set_size_inches(7, 4)
    fig.suptitle('Monthly Electricity Consumption (kWh)')
    plt.title('NMBE = ' + str(round(NMBE_E, 1)) + '%,  CV(RMSE) = ' + str(round(CV_RMSE_E, 1)) + '%', fontsize=9)
    ax.plot( 'Month', 'Annual Electricity (kWh)', data=df_b, marker='o', color='#e24b0f', linewidth=2, label='Uncalibrated')
    ax.plot( 'Month', 'Annual Electricity (kWh)', data=df_c, marker='o', color='blue', linewidth=2, linestyle='dashed', label='Calibrating')
    ax.plot( 'Month', 'Annual Electricity (kWh)', data=df_t, marker='o', color='green', linewidth=2, label='Target')
    # ax.set_ylim(ymin=0)
    plt.xticks(np.array(df_t['Month']))
    ax.legend()
    plt.savefig('Electricity.png', bbox_inches='tight')


    # Natural Gas
    fig, ax = plt.subplots()
    fig.set_size_inches(7, 4)
    fig.suptitle('Monthly Natural Gas Consumption (Therms)')
    plt.title('NMBE = ' + str(round(NMBE_NG, 1)) + '%,  CV(RMSE) = ' + str(round(CV_RMSE_NG, 1)) + '%', fontsize=9)
    ax.plot( 'Month', 'Annual Natural Gas (Therms)', data=df_b, marker='o', color='#e24b0f', linewidth=2, label='Uncalibrated')
    ax.plot( 'Month', 'Annual Natural Gas (Therms)', data=df_c, marker='o', color='blue', linewidth=2, linestyle='dashed', label='Calibrating')
    ax.plot( 'Month', 'Annual Natural Gas (Therms)', data=df_t, marker='o', color='green', linewidth=2, label='Target')
    # ax.set_ylim(ymin=0)
    plt.xticks(np.array(df_t['Month']))
    ax.legend()
    plt.savefig('Natural Gas.png', bbox_inches='tight')

def main():

    file_b = 'C:/Users/Han/Documents/GitHub/SDI/Model_Calibration_2.0/baseline.csv'
    file_t = 'C:/Users/Han/Documents/GitHub/SDI/Model_Calibration_2.0/target_SKY.csv'
    file_c = 'C:/Users/Han/Documents/GitHub/SDI/Model_Calibration_2.0/baseline.csv'

    plot_monthly_consumption(file_b, file_c, file_t)

    # print(p_E)
    # print(p_NG)


main()