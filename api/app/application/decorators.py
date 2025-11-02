from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError

# Retries ante errores transitorios de DB (u otros operacionales)
def retry_on_db_errors(fn):
    return retry(
        reraise=True,
        retry=retry_if_exception_type((OperationalError, )),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=2)
    )(fn)
