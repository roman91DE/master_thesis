import json
from scipy.stats import mannwhitneyu as mwu
from cliffs_delta import cliffs_delta
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import style as mpl_style
from os.path import join, exists
from os import makedirs
from json import load


# matplotlib setup
MPL_CONFIG = load(
    open("/Users/rmn/masterThesis/eda-gp-2020/experiments/matplotlib_config.json", "r", encoding="utf-8")
)

mpl_style.use(MPL_CONFIG["mpl_style"])

# font sizes
SMALL=MPL_CONFIG["fonts"]["small"]
MID=MPL_CONFIG["fonts"]["mid"]
BIG=MPL_CONFIG["fonts"]["big"]

# color codes
C_REG=MPL_CONFIG["colors"]["dae-gp"]
C_PT=MPL_CONFIG["colors"]["pt_dae-gp"]

# marker codes
M_TRAIN=MPL_CONFIG["marker"]["train"]
M_TEST=MPL_CONFIG["marker"]["test"]

TRAIN_LINESTYLE=MPL_CONFIG["train_line_style"]

DPI=MPL_CONFIG["dpi"]


IMG_PATH=f"{MPL_CONFIG['image_base_path']}/symbolicRegressionSummarized"

def create_dir(dir_name):
    if not exists(dir_name):
        makedirs(dir_name)

create_dir(IMG_PATH)
BASE_TITLE="Symbolic Regression"


RESULTS = {
    "airfoil_1hl" : "/Users/rmn/github/master_thesis/data/airfoil_1hl_maxIndSize_fullRun_30gens",
    "airfoil_2hl" : "/Users/rmn/github/master_thesis/data/airfoil_2hl_maxIndSize_fullRun_30gens",
    "bostonHousing": "/Users/rmn/github/master_thesis/data/bostonHousing_2hl_maxIndSize_fullRun_30gens",
    "energyCooling": "/Users/rmn/github/master_thesis/data/energyCooling_2hl_FullRun_30gens",
    "concrete": "/Users/rmn/github/master_thesis/data/concrete_2hl_FullRun_30gens"
}

RESULTS_2hl = {
    "Airfoil" : "/Users/rmn/github/master_thesis/data/airfoil_2hl_maxIndSize_fullRun_30gens",
    "BostonHousing": "/Users/rmn/github/master_thesis/data/bostonHousing_2hl_maxIndSize_fullRun_30gens",
    "energyCooling": "/Users/rmn/github/master_thesis/data/energyCooling_2hl_FullRun_30gens",
    "Concrete": "/Users/rmn/github/master_thesis/data/concrete_2hl_FullRun_30gens"
}


gens = [x for x in range(0, 31)]


def cliffsDeltaPretty(*args):
    val,desc = cliffs_delta(*args)
    return f"{val:.2f}"

def getPVal(sampleA, sampleB):
    stats, pval = mwu(sampleA, sampleB)

    #assert len(sampleA) > 6 and len(sampleB) >= 8

    if pval <= 0.01:
        return f"{pval:.2f}***"
    elif pval <= 0.05:
        return f"{pval:.2f}**"
    elif pval <= 0.1:
        return f"{pval:.2f}*"
    else:
        return f"{pval:.2f}"


# Fitness
# ---

FILENAME="best_final_fitness.json"

# summarize by mean
csv_string = "Problem,Hidden_Layer,Dataset,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"




for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME),"r",encoding="utf-8"))

    # write csv data

    reg_mean_train = np.mean(d["DAE-GP (train)"])
    pt_mean_train = np.mean(d["Pre-Trained (train)"])
    reg_mean_test = np.mean(d["DAE-GP (test)"])
    pt_mean_test = np.mean(d["Pre-Trained (test)"])

    assert d["DAE-GP (train)"] != d["Pre-Trained (train)"]
    assert d["DAE-GP (test)"] != d["Pre-Trained (test)"]


    csv_string += f"{d['problem']},{d['hiddenLayer']},Train,{reg_mean_train},{pt_mean_train},{getPVal(d['DAE-GP (train)'], d['Pre-Trained (train)'])},{cliffsDeltaPretty(d['Pre-Trained (train)'], d['DAE-GP (train)'])}\n,{d['hiddenLayer']},Test,{reg_mean_test},{pt_mean_test},{getPVal(d['DAE-GP (test)'], d['Pre-Trained (test)'])},{cliffsDeltaPretty(d['Pre-Trained (test)'], d['DAE-GP (test)'])}\n"

with open("/Users/rmn/github/master_thesis/data/summary_table_final_fit_mean.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)

    
FILE_FULL_FITNESS_DATA = "full_fitness_data.json"

fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=False, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
# fig.suptitle(f"{BASE_TITLE} - Mean Best Fitness", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("RMSE", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILE_FULL_FITNESS_DATA),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.mean(d["DAE-GP (train)"], axis=0), color=C_REG, marker=M_TRAIN, linestyle=TRAIN_LINESTYLE, label="DAE-GP(Train)")
    ax.plot(gens, np.mean(d["DAE-GP (test)"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP(Test)")
    ax.plot(gens, np.mean(d["Pre-Trained (train)"], axis=0), color=C_PT, marker=M_TRAIN, linestyle=TRAIN_LINESTYLE, label="Pre-Trained(Train)")
    ax.plot(gens, np.mean(d["Pre-Trained (test)"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained(Test)")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/mean_fitness_byGens.png")

# summarize by median
csv_string = "Problem,Hidden_Layer,Dataset,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME),"r",encoding="utf-8"))

    reg_med_train = np.median(d["DAE-GP (train)"])
    pt_med_train = np.median(d["Pre-Trained (train)"])
    reg_med_test = np.median(d["DAE-GP (test)"])
    pt_med_test = np.median(d["Pre-Trained (test)"])

    assert d["DAE-GP (train)"] != d["Pre-Trained (train)"]
    assert d["DAE-GP (test)"] != d["Pre-Trained (test)"]


    csv_string += f"{d['problem']},{d['hiddenLayer']},Train,{reg_med_train},{pt_med_train},{getPVal(d['DAE-GP (train)'], d['Pre-Trained (train)'])},{cliffsDeltaPretty(d['Pre-Trained (train)'], d['DAE-GP (train)'])}\n,{d['hiddenLayer']},Test,{reg_med_test},{pt_med_test},{getPVal(d['DAE-GP (test)'], d['Pre-Trained (test)'])},{cliffsDeltaPretty(d['Pre-Trained (test)'], d['DAE-GP (test)'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_final_fit_median.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=False, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Median Best Fitness", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("RMSE", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILE_FULL_FITNESS_DATA),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.median(d["DAE-GP (train)"], axis=0), color=C_REG, marker=M_TRAIN, linestyle=TRAIN_LINESTYLE, label="DAE-GP(Train)")
    ax.plot(gens, np.median(d["DAE-GP (test)"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP(Test)")
    ax.plot(gens, np.median(d["Pre-Trained (train)"], axis=0), color=C_PT, marker=M_TRAIN, linestyle=TRAIN_LINESTYLE, label="Pre-Trained(Train)")
    ax.plot(gens, np.median(d["Pre-Trained (test)"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained(Test)")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/median_fitness_byGens.png")

# Solution Size
# ---

FILENAME_SIZE = "size_best_solution.json"
FILENAME_SIZE_FULL = "full_data_size_best_solution.json"



# summarize by mean
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_SIZE),"r",encoding="utf-8"))

    
    reg_mean = np.mean(d["DAE-GP"])
    pt_mean = np.mean(d["Pre-Trained"])


    csv_string += f"{d['problem']},{d['hiddenLayer']},{reg_mean},{pt_mean},{getPVal(d['DAE-GP'], d['Pre-Trained'])},{cliffsDeltaPretty(d['Pre-Trained'], d['DAE-GP'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_best_size_mean.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=False, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Mean Size of best Solution", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Size", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_SIZE_FULL),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.mean(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.mean(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/mean_bestSol_size_byGens.png")


# summarize by median
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_SIZE),"r",encoding="utf-8"))

    
    reg_mean = np.median(d["DAE-GP"])
    pt_mean = np.median(d["Pre-Trained"])


    csv_string += f"{d['problem']},{d['hiddenLayer']},{reg_mean},{pt_mean},{getPVal(d['DAE-GP'], d['Pre-Trained'])},{cliffsDeltaPretty(d['Pre-Trained'], d['DAE-GP'])}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_best_size_median.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)

fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=False, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Median Size of best Solution", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Size", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_SIZE_FULL),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.median(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.median(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/median_bestSol_size_byGens.png")


# Epochs Trained
# ---


FILENAME_EPOCHS="epochs_trained_perGen.json"


# summarize by mean
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_EPOCHS),"r",encoding="utf-8"))

    
    reg_mean = np.mean(np.array(d["DAE-GP"]), axis=0)
    pt_mean = np.mean(np.array(d["Pre-Trained"]), axis=0)

    mean_reg_mean = np.mean(reg_mean)
    mean_pt_mean = np.mean(pt_mean)


    csv_string += f"{d['problem']},{d['hiddenLayer']},{mean_reg_mean},{mean_pt_mean},{getPVal(reg_mean, pt_mean)},{cliffsDeltaPretty(pt_mean, reg_mean)}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_mean_epochsTrained.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Mean Epochs Trained", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Epochs trained", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_EPOCHS),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.mean(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.mean(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/mean_epochsTrained.png")


# summarize by median
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_EPOCHS),"r",encoding="utf-8"))

    
    reg_mean = np.median(np.array(d["DAE-GP"]), axis=0)
    pt_mean = np.median(np.array(d["Pre-Trained"]), axis=0)

    mean_reg_mean = np.mean(reg_mean)
    mean_pt_mean = np.mean(pt_mean)


    csv_string += f"{d['problem']},{d['hiddenLayer']},{mean_reg_mean},{mean_pt_mean},{getPVal(reg_mean, pt_mean)},{cliffsDeltaPretty(pt_mean, reg_mean)}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_median_epochsTrained.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Median Epochs Trained", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Epochs trained", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_EPOCHS),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.median(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.median(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/median_epochsTrained.png")

# Population Diversity (norm. Levenshtein Edit Distance)
# ---

# by mean

FILENAME_LEVDIV="lev_div_ovrGens.json"

# summarize by mean
csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_LEVDIV),"r",encoding="utf-8"))

    
    reg_mean = np.mean(np.array(d["DAE-GP"]), axis=0)
    pt_mean = np.mean(np.array(d["Pre-Trained"]), axis=0)

    mean_reg_mean = np.mean(reg_mean)
    mean_pt_mean = np.mean(pt_mean)


    csv_string += f"{d['problem']},{d['hiddenLayer']},{mean_reg_mean},{mean_pt_mean},{getPVal(reg_mean, pt_mean)},{cliffsDeltaPretty(pt_mean, reg_mean)}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_mean_LevDistance.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Mean Population Diversity", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Norm. Levenshtein Distance", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_LEVDIV),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.mean(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.mean(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/mean_levDistance_byGen.png")


# by median


csv_string = "Problem,Hidden_Layer,DAE-GP,Pre-Trained_DAE-GP,P_Value,Cliffs_Delta\n"

for problem,path in RESULTS.items():

    d = json.load(open(join(path, FILENAME_LEVDIV),"r",encoding="utf-8"))

    
    reg_mean = np.median(np.array(d["DAE-GP"]), axis=0)
    pt_mean = np.median(np.array(d["Pre-Trained"]), axis=0)

    mean_reg_mean = np.median(reg_mean)
    mean_pt_mean = np.median(pt_mean)


    csv_string += f"{d['problem']},{d['hiddenLayer']},{mean_reg_mean},{mean_pt_mean},{getPVal(reg_mean, pt_mean)},{cliffsDeltaPretty(pt_mean, reg_mean)}\n"


with open("/Users/rmn/github/master_thesis/data/summary_table_median_LevDistance.csv", "w", encoding="utf-8") as f:
    f.write(csv_string)


fig, ((ul, ur), (dl, dr)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, dpi=DPI, layout="constrained")
fig.set_size_inches(14,12)
#fig.suptitle(f"{BASE_TITLE} - Median Population Diversity", fontsize=BIG)
fig.supxlabel("Generations", fontsize=MID)
fig.supylabel("Norm. Levenshtein Distance", fontsize=MID)

for (problem,path), ax in zip(RESULTS_2hl.items(), (ul, ur, dl, dr)):

    d = json.load(open(join(path, FILENAME_LEVDIV),"r",encoding="utf-8"))
    ax.set_title(problem, fontsize=MID)
    ax.plot(gens, np.median(d["DAE-GP"], axis=0), color=C_REG, marker=M_TEST, label="DAE-GP")
    ax.plot(gens, np.median(d["Pre-Trained"], axis=0), color=C_PT, marker=M_TEST, label="Pre-Trained")
    ax.grid()

ur.legend(fontsize=MID)
fig.savefig(f"{IMG_PATH}/median_levDistance_byGen.png")