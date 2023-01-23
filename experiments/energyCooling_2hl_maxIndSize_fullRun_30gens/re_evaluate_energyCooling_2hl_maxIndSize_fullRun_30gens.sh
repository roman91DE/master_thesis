#/usr/bin/env bash

# Re-Evaluate all results from energyCooling_2hl_maxIndSize_fullRun_30gens

bash config
set -o errexit
set -o nounset
# set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

DIR="/Users/rmn/masterThesis/eda-gp-2020/experiments/energyCooling_2hl_maxIndSize_fullRun_30gens"
PROG="/Users/rmn/masterThesis/eda-gp-2020/src/testing_evaluate.py"
ENV="/Users/rmn/miniconda3/envs/edaGP/bin/python"
JUPYTER="/Users/rmn/miniconda3/envs/dataScience/bin/jupyter"

NRUNS=10
MAXGEN=30


yes yes | $ENV $PROG -f $DIR -n $NRUNS -o "$DIR/results.csv"  -g $MAXGEN

$JUPYTER nbconvert --to html --execute "/Users/rmn/masterThesis/eda-gp-2020/experiments/energyCooling_2hl_maxIndSize_fullRun_30gens/energyCooling_2hl_maxIndSize_fullRun_30gens.ipynb"
