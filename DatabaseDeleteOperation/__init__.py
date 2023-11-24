import datetime
import logging
import azure.functions as func
import pyodbc
import os

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
   
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.warning('Python timer trigger function ran at %s', utc_timestamp)

    connectionString = os.environ["ODBCConnectionString"]
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM StudentReviews WHERE ReviewText = 'BAD RECORD'")
    conn.commit()

    logging.warning("Rows Deleted = %s", cursor.rowcount)
    logging.warning('Scheduled task completed')

    cursor.close()
    conn.close()

  