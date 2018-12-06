import os
import sys
from eppy.modeleditor import IDF

from multiprocessing import Process


def run_single(idf_name, epw_name, n = None):
    print('Simulation ' + str(n) + ' starts.')
    dir_name = os.path.dirname(os.path.realpath(__file__))
    idd_file = "C:/EnergyPlusV9-0-0/Energy+.idd"
    IDF.setiddname(idd_file)

    idf_path = dir_name + '/' + idf_name
    epw_path = dir_name + '/' + epw_name

    out = dir_name + '/out_' + idf_name.split('.idf')[0]

    idf = IDF(idf_path, epw_path)

    idf.run(
        output_directory = out, 
        readvars = True,
        output_prefix = idf_name.split('.idf')[0],
        output_suffix = 'D'
        )

    print('Simulation ' + str(n) + ' ends.')


def main(run = False):
    # search all available idf and epw files to runsimulations
    dir_name = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(dir_name)

    run_files = ['Tweaked.idf']
    # run_files = ['Baseline_HM.idf']
    # run_files = ['Calibrating.idf']

    i = 0
    for file in files:
        if file.endswith('.epw'):
            weather_file = file
    for file in files:
        if file in run_files:
            i += 1
            try:
                run_single(file, weather_file, i)
            except IndexError:
                continue
        else:
            print('Not a idf file')

if __name__ == '__main__':
    main(run=True)



