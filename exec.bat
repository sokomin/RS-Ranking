@echo off
python ranking_lv_jpn.py
python ranking_gh_jpn.py

git add out/jpn_lv/*.csv
git commit -m "test commit"
git push origin main