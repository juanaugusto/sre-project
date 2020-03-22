
import logging
import uuid
from datetime import datetime

class ContextFilter(logging.Filter):

    def filter(self, record):
        record.datetime = datetime.now()
        record.kind = 'NotProducedByFlask'
        return True