# bookmeter

読書メータの読んだ本のリストを csv および json でエキスポートします

## 概要

読んだ本の記録管理に[読書メータ](https://bookmeter.com/) 
を便利に利用させてもらっています。
読んだ本の一覧をダウンロード（エキスポート）したいのですが、
カウント設定からインポートタブできるようなのですが、
エキスポートはなさそうなので、そのための Python スクリプトを作成してみました。

## 使い方

### 外部ライブラリの準備

次の外部ライブラリを使用するので pip で事前にインストールしてください。

* requests
* lxml

次の2行を順に実行すれば良いはずです。
```
pip install requests
pip install lxml
```

### 自分のユーザ ID の確認

エキスポートには自分のユーザ ID が必要です。
次の方法で確認してください。

1. 読書メータにログインする
2. 読書管理タブから読んだ本を選択する
3. ここで表示される URL が<br> ```https://bookmeter.com/users/<user_id>/books/read```<br> のようになっているので、```<user_id>``` の数字列をメモしておきます。

### 読んだ本の一覧のエキスポート

ユーザ ID を引数として、get_bookmeter.py を実行します。
暫くして終了するとカレントディレクトリに

* ```bookmeter_<年月日>.csv```
* ```bookmeter_<年月日>.json```

の 2つのファイルが作成されているので、あとは自由に利用してください。

* サーバ負荷を下げるためデータ取得間隔を開けています。のんびり待ってください。
* csv ファイルは BOM 付き UTF-8 です。

__実行例(ユーザ ID はダミーです)__
```
> python get_bookmeter.py 999999
page: 1 , status_code: 200
page: 2 , status_code: 200
page: 3 , status_code: 200
page: 4 , status_code: 200
page: 5 , status_code: 200
page: 6 , status_code: 200
page: 7 , status_code: 200
page: 8 , status_code: 200
page: 9 , status_code: 200
page: 10 , status_code: 200
page: 11 , status_code: 200
page: 12 , status_code: 200
page: 13 , status_code: 200
page: 14 , status_code: 200
242 books in total
save to bookmeter_200510.json
save to bookmeter_200510.csv
```



## その他のリストのエキスポート

読書メータでは読んだ本以外に、読んでる本、積読本、読みたい本を管理できます。
それらのリストを取得する場合は、```get_bookmeter.py``` の base_url 
を該当のものに変更すれば、おそらくエキスポートできるはずです。
(動作未確認）

|種類| ```base_url```|
|-- |--|
| 読んだ本 | ```f"https://bookmeter.com/users/{user_id}/books/read?display_type=grid"```|
| 読んでる本  | ```f"https://bookmeter.com/users/{user_id}/books/reading?display_type=grid"``` |
| 積読本 | ```f"https://bookmeter.com/users/{user_id}/books/stacked?display_type=grid"``` |
| 読みたい本 | ```f"https://bookmeter.com/users/{user_id}/books/wish?display_type=grid"```|


## ライセンス

[MIT ラセンス](license) です。
