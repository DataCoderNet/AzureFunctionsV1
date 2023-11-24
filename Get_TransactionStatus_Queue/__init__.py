import logging

import azure.functions as func


def main(req: func.HttpRequest, outputSbMsg: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Getting the parameter values from http request
        user = req.params.get('user')
        course = req.params.get('course')
        status = req.params.get('status')
        email = req.params.get('email')

        if user and course and status and email:
            addMsgToQueue = """{
                "user": "%s",
                "course": "%s",
                "status": "%s",
                "email": "%s"
            }""" % (user, course, status, email)

            logging.warning(addMsgToQueue)
            outputSbMsg.set(addMsgToQueue)
            return func.HttpResponse("Message Received")
        else:
            logging.warning("Request failed as one or more parameters are missing in the http call")
            return func.HttpResponse("Request failed as one or more parameters are missing in the http call")
    except:
        logging.warning("Something went wrong")
        return func.HttpResponse("Something went wrong")
    