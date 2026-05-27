"""
DB에 샘플 데이터 삽입 — 로그인 없이 DB 구조 테스트용
python -m db.seed
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.db import get_conn, init_schema


COURSES = [
    (1001, "ISD3001", "정보시스템설계"),
    (1002, "CSE2012", "데이터베이스"),
    (1003, "CSE3021", "머신러닝"),
    (1004, "ENG1001", "공학영어"),
]

MATERIALS = [
    # (course_lms_id, title, file_type, file_path, checksum)
    (1001, "1주차_시스템설계개론.pdf", "pdf", "data/materials/1001/1주차_시스템설계개론.pdf", "abc123"),
    (1001, "2주차_요구사항분석.pptx", "pptx", "data/materials/1001/2주차_요구사항분석.pptx", "def456"),
    (1002, "week1_DB개론.pdf", "pdf", "data/materials/1002/week1_DB개론.pdf", "aaa111"),
    (1002, "week2_ERD설계.pptx", "pptx", "data/materials/1002/week2_ERD설계.pptx", "bbb222"),
    (1003, "ML_01_선형회귀.pdf", "pdf", "data/materials/1003/ML_01_선형회귀.pdf", "ccc333"),
    (1004, "ENG_Unit1.pdf", "pdf", "data/materials/1004/ENG_Unit1.pdf", "ddd444"),
]

ACTIVITIES = [
    # (course_lms_id, title, status, due_date)
    (1001, "[assignment] 시스템 분석 보고서 제출", "pending", "2025-06-10"),
    (1001, "[quiz] 1주차 퀴즈", "completed", "2025-05-20"),
    (1002, "[assignment] ERD 설계 과제", "pending", "2025-06-15"),
    (1002, "[quiz] SQL 기초 퀴즈", "completed", "2025-05-22"),
    (1003, "[assignment] 선형회귀 구현", "pending", "2025-06-20"),
]

CHAT_SESSIONS = [
    # (course_lms_id, messages)
    (1001, [
        ("user", "시스템 분석 보고서 어떻게 써야 해?"),
        ("assistant", "시스템 분석 보고서는 요구사항 정의 → 현황 분석 → 개선 방향 순으로 작성합니다."),
        ("user", "유즈케이스 다이어그램도 포함해야 해?"),
        ("assistant", "네, 유즈케이스 다이어그램은 이해관계자와 시스템 기능의 관계를 시각화하는 데 효과적입니다."),
    ]),
    (1002, [
        ("user", "ERD에서 정규화 3NF 기준이 뭐야?"),
        ("assistant", "3NF는 2NF를 만족하면서, 이행적 종속(Transitive Dependency)이 없는 상태입니다."),
    ]),
]


def seed():
    init_schema()
    conn = get_conn()

    with conn:
        with conn.cursor() as cur:

            # User
            cur.execute("""
                INSERT INTO "User" (lms_id, scraping_interval)
                VALUES ('202501718', 3600)
                ON CONFLICT (lms_id) DO NOTHING
                RETURNING user_id
            """)
            row = cur.fetchone()
            if row:
                user_id = row[0]
            else:
                cur.execute('SELECT user_id FROM "User" WHERE lms_id = %s', ('202501718',))
                user_id = cur.fetchone()[0]
            print(f"user_id = {user_id}")

            # Courses + Enrollment + Materials + Activities
            course_id_map = {}
            for lms_url_id, code, title in COURSES:
                cur.execute("""
                    INSERT INTO Course (lms_url_id, course_code, title)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (lms_url_id) DO UPDATE
                        SET course_code = EXCLUDED.course_code, title = EXCLUDED.title
                    RETURNING course_id
                """, (lms_url_id, code, title))
                course_id = cur.fetchone()[0]
                course_id_map[lms_url_id] = course_id

                cur.execute("""
                    INSERT INTO Enrollment (user_id, course_id, role)
                    VALUES (%s, %s, 'student')
                    ON CONFLICT (user_id, course_id) DO NOTHING
                """, (user_id, course_id))

            print(f"courses: {len(COURSES)}")

            # Materials
            for lms_url_id, title, ftype, fpath, checksum in MATERIALS:
                course_id = course_id_map[lms_url_id]
                cur.execute("""
                    INSERT INTO Material (course_id, title, file_type, file_path, checksum)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (course_id, title, ftype, fpath, checksum))
            print(f"materials: {len(MATERIALS)}")

            # Activities
            for lms_url_id, title, status, due_date in ACTIVITIES:
                course_id = course_id_map[lms_url_id]
                cur.execute("""
                    INSERT INTO Learning_Activity (user_id, course_id, title, status, due_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (user_id, course_id, title, status, due_date))
            print(f"activities: {len(ACTIVITIES)}")

            # Chat Sessions + Logs
            for lms_url_id, messages in CHAT_SESSIONS:
                course_id = course_id_map[lms_url_id]
                cur.execute("""
                    INSERT INTO Chat_Session (user_id, course_id)
                    VALUES (%s, %s) RETURNING session_id
                """, (user_id, course_id))
                session_id = cur.fetchone()[0]
                for role, content in messages:
                    cur.execute("""
                        INSERT INTO Chat_Log (session_id, role, content)
                        VALUES (%s, %s, %s)
                    """, (session_id, role, content))
            print(f"chat sessions: {len(CHAT_SESSIONS)}")

    conn.close()
    print("\nDB 시드 완료.")


if __name__ == "__main__":
    seed()
