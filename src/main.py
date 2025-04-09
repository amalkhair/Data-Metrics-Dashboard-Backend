import json
import os
import sqlite3

import tomli
from fastapi import FastAPI, HTTPException
from typing import List, Optional # to use List and Optional
from uuid import UUID, uuid4 # to generate unique ids
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

with open('../pyproject.toml', 'rb') as file:
    toml_data = tomli.load(file)

DATABASE_URL = os.path.abspath("../data/db/cookie.db")

CREATE_PUBLICATION_TABLE = ("CREATE TABLE publication (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "publication_year INTEGER, amount INTEGER, created_at DATETIME);")
CREATE_FILE_LOCATION_TABLE = "CREATE TABLE file_location (id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING UNIQUE, path STRING UNIQUE );"



def execute_query(query):

    # Connect to the SQLite database
    connection = sqlite3.connect(DATABASE_URL)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a SELECT query
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Process the results

    for row in rows:
        print(row)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return rows


app = FastAPI(title=toml_data['project']['title'], desription=toml_data['project']['description'], version= toml_data['project']['version'])
# creates an instance of FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/publication/bygroup/{group_name}")
def read_publication_by_group(group_name: str):
    query_all_names = f"SELECT name FROM file_location"
    rows = execute_query(query_all_names)
    all_names = [item[0] for item in rows] # ['license','languages']
    avaible_groups = group_name in all_names
    if not avaible_groups:
        return HTTPException(status_code=404, detail=f"Group {group_name} not found")

    query = f"SELECT path FROM file_location WHERE name = '{group_name}'"
    print(query)
    files_path_record = execute_query(query)
    file_path = files_path_record[0][0]
    abs_file_path = os.path.abspath(file_path)
    if not os.path.exists(abs_file_path):
        return HTTPException(status_code=404, detail=f"File {abs_file_path} not found")

    with open(abs_file_path, 'r') as file:
        licenses = json.load(file)
    return licenses

@app.get("/publication/by_year")
def read_publication_by_year():
    query = f"SELECT publication_year, amount FROM publication"
    rows = execute_query(query)


    return  [{"year": item[0], "amount": item[1]} for item in rows]

@app.get("/availabe_group")
def read_all_group():
    query_all_names = f"SELECT name FROM file_location"
    rows = execute_query(query_all_names)
    all_names = [item[0] for item in rows]

    return {"available_group": all_names}



# this runs the api
if __name__ == "__main__": # checks if we're excecuting the main file and not another file

    import uvicorn # uvicorn in a simple webserver to run the api

    print(f'abs_path: {DATABASE_URL}')

    # Check if the database file exists
    if not os.path.exists(DATABASE_URL):
        print(f'Creating database file: {DATABASE_URL}')
        execute_query(DATABASE_URL, CREATE_PUBLICATION_TABLE)
        execute_query(DATABASE_URL, CREATE_FILE_LOCATION_TABLE)
    else:
        print(f"Database file found: {DATABASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port= 1945)