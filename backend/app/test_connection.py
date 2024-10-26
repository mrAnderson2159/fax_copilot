# backend/app/test_connection.py
from sqlalchemy import text
from .database import engine


# Esegui una query di test
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM test"))
    for row in result:
        print(row)
