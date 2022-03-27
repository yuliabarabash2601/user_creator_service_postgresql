import json

from fastapi import FastAPI
import psycopg2
import sys
import uvicorn

app = FastAPI()



def create_table():
    connector = get_connector()
    try:
        cur = connector.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, name VARCHAR(255), surname  VARCHAR(255))")
        connector.commit()
        connector.commit()
        connector.close()
    except Exception as e:
        print(f"Error {e}")


def get_connector():
    connector = psycopg2.connect(database='postgres', user='postgres',
                                 password='my_password', port=5432, host="localhost")
    return connector


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ls")
async def say_hello():
    connector = get_connector()
    try:
        cursor = connector.cursor()
        cursor.execute("select * from users")
        rows = cursor.fetchall()
        connector.commit()
        connector.commit()
        connector.close()
        return json.dumps(rows)
    except Exception as e:
        print(f"Error {e}")


@app.get("/user")
async def create_user(name, surname):
    connector = get_connector()
    try:
        cursor = connector.cursor()
        cursor.execute(f"INSERT INTO users (name, surname) VALUES ('{name}', '{surname}')")
        connector.commit()
        connector.close()
        return dict(message=f"User is saved with name {name} and surname {surname}")
    except Exception as e:
        print(f"Error {e}")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)