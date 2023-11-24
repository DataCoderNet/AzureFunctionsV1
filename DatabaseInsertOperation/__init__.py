import logging
import azure.functions as func
import pyodbc
import os 
from multiprocessing import connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    connectionString = os.environ["ODBCConnectionString"]
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    ReviewText = req.params.get('review')
    if not ReviewText:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ReviewText = req_body.get('review')

    if ReviewText:
        cursor.execute(f"INSERT INTO StudentReviews (ReviewTime, ReviewText) VALUES (CURRENT_TIMESTAMP, '{ReviewText}')")
    else:
        cursor.execute("INSERT INTO StudentReviews (ReviewTime, ReviewText) VALUES (CURRENT_TIMESTAMP, 'BAD RECORD')")

    conn.commit()    
    
    cursor.close()
    conn.close()

    logging.warning('Your request is processed')

    return func.HttpResponse(
             "Your request is processed",
             status_code=200
        )
          