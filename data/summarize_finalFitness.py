import json
from scipy.stats import mannwhitneyu
from statistics import median

RESULTS = {
    "airfoil_1hl" : "/Users/rmn/github/master_thesis/data/airfoil_1hl_maxIndSize_fullRun_30gens",
    "airfoil_2hl" : "/Users/rmn/github/master_thesis/data/airfoil_2hl_maxIndSize_fullRun_30gens",
    "bostonHousing": "/Users/rmn/github/master_thesis/data/bostonHousing_2hl_maxIndSize_fullRun_30gens",
    "energyCooling": "/Users/rmn/github/master_thesis/data/energyCooling_2hl_FullRun_30gens"
}

FILENAME="best_final_fitness.json"


csv_string = "Problem?Set?Median_RMSE?P_Value?Significance\n"

for problem,path in RESULTS.keys():
    d = json.load()
    csv_string += f"{problem},"
