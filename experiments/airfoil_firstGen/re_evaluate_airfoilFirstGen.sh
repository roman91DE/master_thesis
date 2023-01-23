#/usr/bin/env bash

# Re-Evaluate all results from airfoilFirstGen experiments

bash config
set -o errexit
set -o nounset
# set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

DIR="/Users/rmn/masterThesis/eda-gp-2020/experiments/airfoil_firstGen"
PROG="/Users/rmn/masterThesis/eda-gp-2020/src/testing_evaluate.py"
ENV="/Users/rmn/miniconda3/envs/edaGP/bin/python"

NRUNS=10
MAXGEN=1

COUNTER=0

# Find all subdirectories of DIR
for SUBDIR in $(find "$DIR" -type d -maxdepth 1); do
  if [ "$SUBDIR" = "$DIR" ]; then
      continue
    fi
  if [[ "$SUBDIR" == *".ipynb_checkpoints"* ]]; then
    continue
  fi
  yes yes | $ENV $PROG -f $SUBDIR -n $NRUNS -o "$SUBDIR/results.csv"  -g $MAXGEN
  ((COUNTER++))

done

echo "Done - Evaluated $COUNTER Experiments!"

JUPYTER="/Users/rmn/miniconda3/envs/dataScience/bin/jupyter"

$JUPYTER nbconvert --to html --execute "/Users/rmn/masterThesis/eda-gp-2020/experiments/airfoil_firstGen/airfoil_1gen_combined_layers.ipynb"
$JUPYTER nbconvert --to html --execute "/Users/rmn/masterThesis/eda-gp-2020/experiments/airfoil_firstGen/airfoil_1gen_combined_neurons.ipynb"
