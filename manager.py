# 서버를 구동시키는 역할
# 디버그 / 테스트 / 라이브 모드 설정. => flask_script 라이브러리 활용

from server import created_app

app = created_app()

# 디버그 모드 => 파이썬 파일을 저장하면 => 서버도 자동 재시작

app.run(host='0.0.0.0')