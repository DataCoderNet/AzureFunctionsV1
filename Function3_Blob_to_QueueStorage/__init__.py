import logging
import azure.functions as func
from shared_code.common_functions import delete_blob

def main(myblob: func.InputStream, outputQueueItem: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    clear_text = myblob.read().decode('utf-8')

    sendMessageOut = "Processed by Func3 \n"+clear_text

    outputQueueItem.set(sendMessageOut)

    logging.warning('Processed by Function 3')


    #Fetching the name of the blob
    tmp = (myblob.name).split("/")
    containerName = tmp[0]
    blobName = tmp[1]

    logging.warning(f'Calling Method do delete blob {blobName}')

    delete_blob(containerName, blobName)