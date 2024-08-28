> Python 의 logging 라이브러리를 사용하여 log를 출력하고 남기기 가능

# 예제: 웹 애플리케이션 로그 관리
### 애플리케이션 구조
- main.py: 애플리케이션의 진입점
- database.py: 데이터베이스 관련 작업을 처리하는 모듈
- auth.py: 사용자 인증 관련 모듈
- utils.py: 유틸리티 함수 모듈
### 요구사항
1. 로그를 파일과 콘솔에 모두 기록하되, 파일은 일정 크기 이상이 되면 새 파일로 교체한다.
2. 각 모듈별로 다른 로거를 사용하여, 필요한 경우 모듈별로 로그를 관리할 수 있다.
3. 프로덕션 환경에서는 **INFO 레벨** 이상의 로그만 기록하고, 개발 환경에서는 **DEBUG 레벨**의 상세 로그를 기록한다.
4. 특정 **모듈에서만 ERROR 이상의 로그**를 별도로 관리한다.

### 예제 코드

**main.py**
```python
import logging
from logging.handlers import RotatingFileHandler
from database import db_function
from auth import authenticate_user
from utils import helper_function

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

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the application")
    db_function()
    authenticate_user("test_user")
    helper_function()
    logger.info("Application finished")

if __name__ == '__main__':
    main()
```

**database.py**
```python
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
```

**auth.py**
```python
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
```

**utils.py**
```python
import logging

# 유틸리티 전용 로거
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)  # 디버그 정보를 포함한 모든 로그 기록

def helper_function():
    logger.debug("Starting helper function")
    # 유틸리티 작업 수행
    logger.debug("Helper function is performing a task")
    logger.info("Helper function finished")
```

1. **로그 파일 관리**: 로그는 app.log 파일에 기록되며, 이 파일이 1MB를 넘으면 새로운 파일로 교체됩니다. 최대 3개의 백업 파일이 유지됩니다.
2. **모듈별 로거**: 각 모듈(database, auth, utils)은 자체 로거를 가지고 있으며, 필요에 따라 로그 레벨을 다르게 설정할 수 있습니다. 예를 들어, auth 모듈에서는 WARNING 이상의 로그만 기록합니다.
3. **로그 레벨 조정**: main.py에서 애플리케이션의 전체 로그 레벨을 설정할 수 있습니다. 이 레벨은 개발 환경에서는 DEBUG로, 프로덕션 환경에서는 INFO로 조정할 수 있습니다.
4. **상세한 로그 관리**: database 모듈에서 예외가 발생하면 ERROR 로그가 기록되며, 해당 오류의 스택 트레이스도 함께 기록됩니다 (exc_info=True).

> console_handler option
> StreamHandler를 사용하여 로그 메시지를 콘솔에 출력하고, 로그 메시지의 형식을 지정해주는 핸들러
> 즉, handler 옵션을 사용하면 콘솔에서 메세지를 출력시킬 수 있음

### Log Level
1. **DEBUG** (10)
	- 가장 낮은 로그 레벨입니다.
	- 디버깅 목적으로 상세한 정보를 기록합니다.
	- 개발 중 문제를 추적하기 위해 사용됩니다.
2. **INFO** (20)
	- 일반적인 정보 메시지를 기록합니다.
	- 애플리케이션의 정상적인 동작을 나타내는 정보입니다.
3. **WARNING** (30)
	- 주의가 필요한 상황을 기록합니다.
	- 비정상적인 동작이지만, 애플리케이션이 계속해서 동작할 수 있는 경우입니다.
4. **ERROR** (40)
	- 오류가 발생한 상황을 기록합니다.
	- 애플리케이션에서 중요한 기능이 실패했음을 나타냅니다.
5. **CRITICAL** (50)
	- 가장 높은 로그 레벨입니다.
	- 치명적인 오류를 기록하며, 애플리케이션이 더 이상 실행될 수 없거나 중대한 문제가 발생했을 때 사용됩니다.

> 로그 레벨이 INFO로 설정된 경우, INFO, WARNING, ERROR, CRITICAL 레벨의 메시지는 기록되지만, DEBUG 레벨의 메시지는 무시

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.debug("This is a debug message")  # 기록되지 않음
logger.info("This is an info message")   # 기록됨
logger.warning("This is a warning message")  # 기록됨
logger.error("This is an error message")  # 기록됨
logger.critical("This is a critical message")  # 기록됨
```

# 추가: 특정 모듈 로그 필터링 (제외)
1. **필터 사용**: 필터를 적용하여 특정 로거의 로그를 제외시킵니다.
2. **레벨 조정**: 모듈 로거의 레벨을 WARNING으로 설정하여, INFO 로그가 출력되지 않도록 합니다.

### 1. 필터 사용
**main.py**
```python
import logging
from logging.handlers import RotatingFileHandler
from database import db_function
from auth import authenticate_user
from utils import helper_function

class ExcludeAuthFilter(logging.Filter):
	def filter(self, record):
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
	level=logging.INFO, # 프로덕션 환경에서 기본 레벨 설정 (개발 환경에서는 DEBUG로 변경 가능)
	handlers=[file_handler, console_handler]
)

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
```
### 2. 레벨 조정
**auth.py**
```python
import logging

# 인증 전용 로거
logger = logging.getLogger('auth')
logger.setLevel(logging.ERROR)  # ERROR 이상의 로그만 기록

def authenticate_user(username):
    logger.info(f"Authenticating user: {username}")
    if username != "valid_user":
        logger.warning(f"Authentication failed for user: {username}")
        return False
    logger.info(f"User {username} authenticated successfully")
    return True
```