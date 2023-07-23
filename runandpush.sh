#/bin/bash
# Runs the main script that stores data
HOMEDIR=$(dirname `readlink -f "${BASH_SOURCE}"`)
python3 $HOMEDIR/main.py
ExchangeRatesByDate=$(awk -F "=" '/ExchangeRatesByDate/ {print $2}' $HOMEDIR/armcenban.config)
pushd $ExchangeRatesByDate
git add --all
ModifiedDate=$(ls -r1 [0-9]*.xml | head -1)
git commit -m "${ModifiedDate:0:8}"
git push origin master
popd