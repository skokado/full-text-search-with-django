# full-text-search-with-django

OpenSearch で全文検索を実施するための Webアプリケーションサンプル。w/Django

```sh
$ tree
├── config               # Django プロジェクトディレクトリ
├── full_text_search     # ヘルパー、ユーティリティ (NOT Django application)
│   ├── helpers.py   
│   ├── mappings/base.py # マッピング定義の基底クラス
├── myapp
│   ├── mappings         # マッピング定義（≒ OpenSearch Index のスキーマ定義）
│   ├── models.py        # Django's ORM
```

# Demo

![](./docs/img/demo.gif)

# Setup

```sh
# Install
$ create-your-virtualenv-and-activate
(.venv) $ uv sync

# Start OpenSearch
(.venv) $ docker compsoe up -d
(.venv) $ docker compsoe ps

# Database migrate and seed test data
(.venv) $ python manage.py migrate
(.venv) $ python manage.py shell < scripts/seed_data.py

# Start
(.venv) $ python manage.py runserver
# => Access to http://localhost:8000
```

また http://localhost:5601 で OpenSearch Dashboards へアクセスできます。
