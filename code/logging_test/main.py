import logging
from logging.handlers import RotatingFileHandler
from database import db_function
from auth import authenticate_user
from utils import helper_function

class ExcludeAuthFilter(logging.Filter):
    def filter(self, record):
        # 'WDM'이라는 이름을 가진 로거에서 발생한 로그는 제외
        return not record.name.startswith("auth")

# 기본 로그 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 파일 핸들러 (로그 파일이 1MB를 넘으면 새로운 파일로 교체, 최대 3개의 파일을 보관)
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 루트 로거 설정
logging.basicConfig(
    level=logging.INFO,  # 프로덕션 환경에서 기본 레벨 설정 (개발 환경에서는 DEBUG로 변경 가능)
    handlers=[file_handler, console_handler]
)

# 루트 로거에 필터 추가
# root_logger = logging.getLogger()
# root_logger.addFilter(ExcludeAuthFilter())

# auth 로거에 필터 직접 추가
auth_logger = logging.getLogger('auth')
auth_logger.addFilter(ExcludeAuthFilter())

logger = logging.getLogger(__name__)

def run():
    logger.info("Starting the application")
    db_function()
    authenticate_user("test_user")
    helper_function()
    logger.info("Application finished")

if __name__ == '__main__':
    run()