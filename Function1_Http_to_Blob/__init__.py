import logging

import azure.functions as func


def main(req: func.HttpRequest, outputBlob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    message = req.params.get('message')

    sendMessageOut = 'Processed by Func1 \n' + message

    outputBlob.set(sendMessageOut)

    logging.warning('Processed by Function 1')

    return func.HttpResponse('Thank you for your message')
