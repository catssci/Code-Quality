import logging

# 인증 전용 로거
logger = logging.getLogger('auth')
logger.setLevel(logging.WARNING)  # WARNING 이상의 로그만 기록

def authenticate_user(username):
    logger.info(f"Authenticating user: {username}")
    if username != "valid_user":
        logger.warning(f"Authentication failed for user: {username}")
        return False
    logger.info(f"User {username} authenticated successfully")
    return True