# RS-Ranking
レッドストーンのレベルランキングとか

## 動かし方
放置しとけばGitHubActionが1日2回取得しにいってくれます。


## トラブルシュート
- auto commitで事故った時は
  - `git log`でcommit番号調べる
  - `git reset <コミットID>`
  - リバートだと打消しcommitにしかならず、rebaseだと運用が面倒