import logging

import tenacity
from app.database.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5  # 5 minutes
WAIT_SECONDS = 1


@tenacity.retry(
    stop=tenacity.stop_after_attempt(MAX_TRIES),
    wait=tenacity.wait_fixed(WAIT_SECONDS),
    before=tenacity.before_log(logger, logging.INFO),
    after=tenacity.after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Try to create session to check if DB is awake
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
