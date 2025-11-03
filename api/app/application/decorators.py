import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from sqlalchemy.exc import OperationalError

logger = logging.getLogger("retry")

def retry_on_db_errors(fn):
    return retry(
        reraise=True,
        retry=retry_if_exception_type((OperationalError, )),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2),
        before_sleep=before_sleep_log(logger, logging.WARNING)  
    )(fn)
