# Webhook Repo

Steps to running this project

*******************

## Setup

* Create a new virtual environment
```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
venv\Scripts\activate (for windows)
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application 

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```


*******************