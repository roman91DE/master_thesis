import json
from scipy.stats import mannwhitneyu as mwu
from statistics import median
from os.path import join

RESULTS = {
    "airfoil_1hl" : "/Users/rmn/github/master_thesis/data/airfoil_1hl_maxIndSize_fullRun_30gens",
    "airfoil_2hl" : "/Users/rmn/github/master_thesis/data/airfoil_2hl_maxIndSize_fullRun_30gens",
    "bostonHousing": "/Users/rmn/github/master_thesis/data/bostonHousing_2hl_maxIndSize_fullRun_30gens",
    "energyCooling": "/Users/rmn/github/master_thesis/data/energyCooling_2hl_FullRun_30gens"
}

FILENAME="best_final_fitness.json"

def getPVal(sampleA, sampleB):
    stats, pval = mwu(sampleA, sampleB)
    if pval <= 0.01:
        return f"{pval:.6f}***"
    elif pval <= 0.05:
        return f"{pval:.6f}**"
    elif pval <= 0.1:
        return f"{pval:.6f}*"
    else:
        return f"{pval:.6f}"


csv_string = "Problem,Hidden_Layer,Dataset,DAE-GP,Pre-Trained_DAE-GP,P_Value\n"

for problem,path in RESULTS.items():
    d = json.load(open(join(path, FILENAME),"r",encoding="utf-8"))

    reg_med_train = median(d["DAE-GP (train)"])
    pt_med_train = median(d["Pre-Trained (train)"])
    reg_med_test = median(d["DAE-GP (test)"])
    pt_med_test = median(d["Pre-Trained (test)"])

    assert d["DAE-GP (train)"] != d["Pre-Trained (train)"]
    assert d["DAE-GP (test)"] != d["Pre-Trained (test)"]

    d["hiddenLayer"]



    csv_string += f"{d['problem']},{d['hiddenLayer']},Train,{reg_med_train},{pt_med_train},{getPVal(d['DAE-GP (train)'], d['Pre-Trained (train)'])}\n,{d['hiddenLayer']},Test,{reg_med_test},{pt_med_test},{getPVal(d['DAE-GP (test)'], d['Pre-Trained (test)'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_final_fit.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)