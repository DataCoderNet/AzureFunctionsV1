import logging
import json 
import azure.functions as func
import pyodbc
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.warning('Python trigger DatabaseSelectFunctionOld function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    connectionString = os.environ['ODBCConnectionString']

    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    if name:
        cursor.execute("SELECT * FROM dbo.OnlineCourses where Instructor = ?", name)
    else:
        cursor.execute("SELECT * FROM dbo.OnlineCourses")

    records = list(cursor.fetchall())

    logging.info(records)

    # return_body = ' \n'.join([str(elem) for elem in records])
    records = [tuple(record) for record in records]
    return_body = json.dumps(obj=records, indent=2) 

    cursor.close()
    conn.close()

    logging.warning('SQL Database connection closed')
    
    return func.HttpResponse(
        body = return_body,
        status_code=200
    ) 
