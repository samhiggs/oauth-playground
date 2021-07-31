# Practicing how an OAuth App works using wine reviews

## Installation

1. Download data into `data/` if not available in repo from [kaggle](https://www.kaggle.com/zynicide/wine-reviews?select=winemag-data_first150k.csv)

2. Setup your environment
    ```
    python3.8 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    ```
3. Setup account and configure random aliases to play with on [simplelogin](https://simplelogin.io/)
4. Create and add credentials and play account email addresses to configuration.yml file

```{yaml}
simplelogin:
  CLIENT_ID: XXXXX
  CLIENT_SECRET: XXXXXXX
  accounts:
    - a@b.com
    - b@b.com
```

5. Setup database which pulls in the wine reviews and adds a private vs public setting.

```{bash}
python create_db.py
```

