import sys

from eppy import modeleditor
from eppy.modeleditor import IDF
import eppy.run_functions as rf



idd_file = 'C:/EnergyPlusV8-9-0/Energy+.idd'
idf_file = 'C:/Users/Han/Documents/GitHub/SDI/batch_run/python/in.idf'
epw_file = 'C:/Users/Han/Documents/GitHub/SDI/batch_run/python/in.epw'

IDF.setiddname(idd_file)
idf1 = IDF(idf_file, epw_file)
idf2 = IDF(idf_file, epw_file)
idf3 = IDF(idf_file, epw_file)
idf4 = IDF(idf_file, epw_file)

# help(idf.run)

# idf.run(output_prefix = 'new_', output_directory = './out')
# idf.save('in.idf')


if __name__ == '__main__':
    run_dict = {
        "idf": None,
        "weather": None,
        "output_directory": '',
        "annual": False,
        "design_day": False,
        "idd": None,
        "epmacro": False,
        "expandobjects": False,
        "readvars": False,
        "output_prefix": None,
        "output_suffix": None,
        "version": False,
        "verbose": 'v',
        "ep_version": None
    }

    job_list = [
        [idf1, run_dict],
        [idf2, run_dict],
        [idf3, run_dict],
        [idf4, run_dict]
    ]

    rf.runIDFs(job_list)



