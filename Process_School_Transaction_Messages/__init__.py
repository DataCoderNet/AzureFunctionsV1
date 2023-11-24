import logging
import json 
import azure.functions as func
import pyodbc
import os
import smtplib 
import ssl 

def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    
    #Grabbing the message from queue and converting it to JSON
    message_json_string = msg.get_body().decode('utf-8')
    json_data = json.loads(message_json_string)

    #Getting values out of JSON object
    user = json_data["user"]
    course = json_data["course"]
    status = json_data["status"]
    email = json_data["email"]


    #Save data to SQL Database
    connectionString = os.environ["ODBCConnectionString"]
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    if status == 'SUCCESS' or  status == 'success':
       cursor.execute(f"INSERT INTO dbo.StudentsData (user_name, course_id, transaction_status, user_email) VALUES ( '{user}', '{course}', '{status}', '{email}' )")

    else:
       cursor.execute(f"INSERT INTO dbo.FailedToConvert (user_name, course_id, transaction_status, user_email) VALUES ( '{user}', '{course}', '{status}', '{email}' )")

    cursor.commit()

    cursor.close()
    conn.close()

    # # Sending email
    # mailTo = email
    # if status == "SUCCESS" or status == "success":
    #     subject = "Good News | you are in"
    #     content = "your request is successfully accepted \n Welcome to Hector's course \n Regards"
    # else:
    #     subject = "Transaction Declined"
    #     content = "Apologies. Transaction failed \n We will get back to you soon \n Regards"        

    # smtp_server_domain_name = "smtp.gmail.com"
    # port=465
    # sender_email = "EMAIL@gmail.com"
    # password = "@@@PASSWORD"

    # # Sending Email using gmail smtp server
    # ssl_context = ssl.create_default_context()
    # service = smtplib.SMTP_SSL(smtp_server_domain_name, port, context=ssl_context)
    # service.login(sender_email, password)
    # result = service.sendmail(sender_email, mailTo, f"Subject: {subject}\n{content}")




