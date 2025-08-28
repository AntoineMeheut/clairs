# clairs
Angular front-end and back-end application skeleton using the Django framework (Python)

# How it works

## Prerequisites
Ensure you have Python 3 and Node.js installed on your system. The current project dependency versions are:
- Python 3.10
- Node.js 18.5.0

## Installation
### 1. Frontend: Choose 1 of 2 ways below:
- Install frontend dependencies and start frontend locally:
```shell
npm --prefix=clairs-frontend install
```

```shell
npm --prefix=clairs-frontend start
```

This command will install and start the Angular development server. You can access the Angular application through your web browser at `http://localhost:4200`.

### 2. Backend:
- Set up a virtual environment
```shell
python3 -m venv .clairs
```

```shell
source .clairs/bin/activate
```

- Install backend dependencies:
```shell
pip install -r clairs-backend/requirements.txt
```

- Apply database migrations:
```shell
python3 clairs-backend/manage.py migrate
```

- Run the Django development server:
```shell
python3 clairs-backend/manage.py runserver
```

Now, your local server should be running, and you can access this Django/Angular application through your web browser at http://localhost:8000.
