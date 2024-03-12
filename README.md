# CreateAWSOrgAccount
Organizationsでメンバーアカウントをまとめて作成して指定したOUに移動するスクリプトです。
AWS CloudShellへcreate_account.pyをダウンロードして実行します。

mail_prefix、mail_domain、source_parent_id、destination_parent_id、start、stopを環境にあわせて書き換えます。
ルートユーザーのメールアドレスアカウントはプレフィックスと数字です。

* mail_prefix
ルートユーザーのメールアカウントとアカウント名のプレフィックスです。

* mail_domain
ルートユーザーのメールドメインです。

* source_parent_id
Organizationsのr-xxxxのようなルートIDです。

* destination_parent_id
OUのou-xxxxxxのようなOUのIDです。

* start, stop
ルートユーザーのメールアカウントの数字のはじまりと終わりです。
1と50を指定すればアカウントが50作成されます。
AWSアカウントの制限値を超えることはできませんので、クォーターを確認して実行してください。

```
python3 create_account.py
```
