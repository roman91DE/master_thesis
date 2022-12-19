#!/usr/bin/env bash

# bash config
set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

PROJECT_DIR="/Users/rmn/github/master_thesis"
cd $PROJECT_DIR


# render document to pdf
Rscript -e "rmarkdown::render('paper.Rmd',  encoding = 'UTF-8')"

# clean up
mv *.tex tex

# push to github repo
git add * ; git commit -m "...knitted document..." ; git push  

# open file with default application
open paper.pdf
