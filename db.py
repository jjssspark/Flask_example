
import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='mariadb',  # cloudtype 사용 시
                port=3306,   # cloudtype 사용 시
                database='test',  # test 데이터베이스 사용
                user='root',
                password='park!6443',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor   # 쿼리 결과를 딕셔너리로 변환
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def save_bmi_record(self, weight, height, bmi, category):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO bmi_records (height, weight, bmi, category)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (height, weight, bmi, category))
                self.connection.commit()   # ← 이게 제일 중요!
                return True
        except Exception as e:
            print("저장 오류:", e)
            return False
    def get_bmi_records(self, limit=10):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT height, weight, bmi, category, created_at 
                FROM bmi_records 
                ORDER BY created_at DESC 
                LIMIT %s
                """
                cursor.execute(sql, (limit,))
                return cursor.fetchall()

        except Exception as e:
            print("History 조회 오류:", e)
            return []
    def close(self):
    
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")