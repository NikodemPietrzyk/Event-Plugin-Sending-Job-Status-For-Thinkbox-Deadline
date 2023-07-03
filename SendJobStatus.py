from Deadline.Events import *
import os
import sys
import logging
PATH_TO_LOGGING = 
API_ENDPOINT = 
API_KEY = 
USER =
try:
    import httplib
except ImportError:
    try:
        import http.client as httplib
    except ImportError:
        logging.debug("Failed to import httplib")
        httplib = None
try:
    import json
except ImportError:
    logging.debug("Failed to import json")
    json = None
    
logging.basicConfig(filename=pathToLogging, encoding='utf-8', level=logging.DEBUG)


def send_put_request(url, data):
    conn = httplib.HTTPConnection(url)
    url = "/api/v1/jobStatus"
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer {}".format(API_KEY)
    }
    conn.request("PUT", url, json.dumps(data), headers=headers)
    response = conn.getresponse()
    logging.debug(response)
    return response.read()
    

class MyEvent(DeadlineEventListener):
    def __init__(self):
        self.OnJobFinishedCallback += self.OnJobFinished
        self.OnJobFailedCallback += self.OnJobFailed
        self.OnJobDeletedCallback += self.OnJobDeleted
        self.OnJobSuspendedCallback += self.OnJobSuspended
        self.OnJobStartedCallback += self.OnJobStarted

    def OnJobFinished(self, job):
        self.SendJobStatus(job, "completed")

    def OnJobFailed(self, job):
        self.SendJobStatus(job, "failed")

    def OnJobDeleted(self, job):
        self.SendJobStatus(job, "deleted")
        
    def OnJobSuspended(self, job):
        self.SendJobStatus(job, "suspended")
       
    def OnJobStarted(self, job):
        self.SendJobStatus(job, "rendering")

    def SendJobStatus(self, job, status):
        if job.JobUserName == USER:
            logging.debug(job.JobUserName)
            logging.debug(status)
            logging.debug(job.JobId)
            jobId = job.JobId
            data = {
                "jobId": jobId,
                "status": status
            }
            response = send_put_request(API_ENDPOINT, data)
            logging.debug("Sent job status for JobId {}: {}".format(jobId, status))


def GetDeadlineEventListener():
    """This is the function that Deadline calls to get an instance of the
    main DeadlineEventListener class.
    """
    return MyEvent()

def CleanupDeadlineEventListener(deadlinePlugin):
    """This is the function that Deadline calls when the event plugin is
    no longer in use so that it can get cleaned up.
    """
    deadlinePlugin.Cleanup()
