import os
import sys
from eppy.modeleditor import IDF


def run_single(idf_name, epw_name):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    idd_file = "C:/EnergyPlusV8-9-0/Energy+.idd"
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


def main():
    # run_single('original_CBES_model.idf', 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw')
    run_single('tweaked_CBES_model_v0.0.idf', 'USA_PA_Pittsburgh.Intl.AP.725200_TMY3.epw')


main()
