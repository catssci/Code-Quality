import logging

# 데이터베이스 전용 로거
logger = logging.getLogger('database')
logger.setLevel(logging.INFO)  # 기본적으로 INFO 레벨 이상의 로그만 기록

def db_function():
    logger.info("Starting database function")
    # 데이터베이스 작업 수행
    try:
        # 예제: 데이터베이스 연결 시도
        logger.debug("Attempting to connect to the database")
        # 예제: 데이터베이스 연결 성공
        logger.info("Connected to the database")
    except Exception as e:
        logger.error("Database connection failed", exc_info=True)
    logger.info("Database function finished")