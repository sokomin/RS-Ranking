@echo off
git pull origin main > log/exec.log

If not exist log mkdir log


git add out/jpn_lv/*.csv >> log/exec.log
git add out/jpn_gh_2024/*.csv >> log/exec.log
git add out/jpn_detective/*.csv >> log/exec.log
git commit -m "[auto commit]daily japan ranking updated."

rem "pushだけはすると事故る"
rem "git push origin main"
git push origin main >> log/exec.log
