import logging

# 유틸리티 전용 로거
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)  # 디버그 정보를 포함한 모든 로그 기록

def helper_function():
    logger.debug("Starting helper function")
    # 유틸리티 작업 수행
    logger.debug("Helper function is performing a task")
    logger.info("Helper function finished")