To initiate app
0. run ``python -m venv venv`` and ``pip install -r requirements.txt``
1. in terminal ``Docker Compose up``
2. open new terminal and enter ``alembic upgrade head``
3. run ``uvicorn app.main:app --reload``


To run tests
1. in terminal enter ``python -m pytest`` 