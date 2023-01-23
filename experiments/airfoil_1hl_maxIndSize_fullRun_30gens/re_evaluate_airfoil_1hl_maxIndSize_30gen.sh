#/usr/bin/env bash

# Re-Evaluate all results from airfoilFirstGen experiments

bash config
set -o errexit
set -o nounset
# set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

DIR="/Users/rmn/masterThesis/eda-gp-2020/experiments/airfoil_1hl_maxIndSize_fullRun_30gens"
PROG="/Users/rmn/masterThesis/eda-gp-2020/src/testing_evaluate.py"
ENV="/Users/rmn/miniconda3/envs/edaGP/bin/python"
JUPYTER="/Users/rmn/miniconda3/envs/dataScience/bin/jupyter"

NRUNS=10
MAXGEN=30


yes yes | $ENV $PROG -f $DIR -n $NRUNS -o "$DIR/results.csv"  -g $MAXGEN

$JUPYTER nbconvert --to html --execute "/Users/rmn/masterThesis/eda-gp-2020/experiments/airfoil_1hl_maxIndSize_fullRun_30gens/airfoil_1hl_maxIndSize_fullRun_30gens.ipynb"