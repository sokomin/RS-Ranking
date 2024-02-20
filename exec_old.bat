@echo off
git pull origin main > log/exec.log

If not exist log mkdir log

@REM python ranking_lv_jpn.py >> log/exec.log
@REM python ranking_gh_jpn.py >> log/exec.log

git add out/jpn_lv/*.csv >> log/exec.log
@REM git add out/jpn_gh/*.csv >> log/exec.log
git commit -m "[auto commit]daily japan ranking updated."

rem "pushだけはすると事故る"
rem "git push origin main"
git push origin main >> log/exec.log
