@echo off
git pull origin main

python ranking_lv_jpn.py
python ranking_gh_jpn.py

git add out/jpn_lv/*.csv
git add out/jpn_gh/*.csv
git commit -m "test commit"

rem "pushだけはすると事故る"
rem "git push origin main"

