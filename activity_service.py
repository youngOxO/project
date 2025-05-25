# activity_service.py - 활동 데이터 관리 모듈 (CSV 기반 저장)

import os
import csv

class ActivityService:
    def __init__(self):
        # 활동 데이터를 저장할 CSV 파일 이름
        self.filename = "activities.csv"
        self.activities = []  # 활동 정보 리스트
        self.activity_dict = {}  # 활동 제목+날짜를 키로 한 딕셔너리
        self.load_activities()  # 실행 시 기존 CSV 파일에서 불러오기

    def add_activity(self, title, date, description, participants):
        # 활동 고유 키 생성
        key = f"{title} ({date})"
        # 활동 정보 딕셔너리 구성
        activity = {
            "title": title,
            "date": date,
            "description": description,
            "participants": participants
        }
        # 리스트와 딕셔너리에 저장
        self.activities.append(activity)
        self.activity_dict[key] = activity
        self.save_activities()  # 저장 후 파일 갱신
        return f"활동 '{title}' 이(가) 등록되었습니다."

    def delete_activity_by_key(self, key):
        # 활동 키가 존재하면 삭제
        if key in self.activity_dict:
            self.activities = [a for a in self.activities if f"{a['title']} ({a['date']})" != key]
            del self.activity_dict[key]
            self.save_activities()
            return f"활동 '{key}' 삭제 완료."
        return "해당 활동을 찾을 수 없습니다."

    def get_activity_titles(self):
        # 활동 제목과 날짜 리스트 반환
        return [f"{a['title']} ({a['date']})" for a in self.activities]

    def get_activity_detail(self, key):
        # 키에 해당하는 활동 정보 상세 보기
        a = self.activity_dict.get(key)
        if not a:
            return "해당 활동을 찾을 수 없습니다."
        return f"제목: {a['title']}\n날짜: {a['date']}\n내용: {a['description']}\n참여자: {', '.join(a['participants']) if a['participants'] else '없음'}"

    def get_activity_titles_by_student(self, student_id):
        # 특정 학생이 참여한 활동 제목+날짜 목록
        return [f"{a['title']} ({a['date']})" for a in self.activities if student_id in a['participants']]

    def get_activities_by_student(self, student_id):
        # 특정 학생이 참여한 활동 전체 정보 리스트
        return [a for a in self.activities if student_id in a['participants']]

    def save_activities(self):
        # 활동 정보를 CSV 파일로 저장
        with open(self.filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "date", "description", "participants"])
            for a in self.activities:
                writer.writerow([
                    a['title'],
                    a['date'],
                    a['description'],
                    ",".join(a['participants'])
                ])

    def load_activities(self):
        # CSV 파일이 존재하면 불러오기
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    participants = row['participants'].split(',') if row['participants'] else []
                    activity = {
                        "title": row['title'],
                        "date": row['date'],
                        "description": row['description'],
                        "participants": participants
                    }
                    self.activities.append(activity)
                    key = f"{row['title']} ({row['date']})"
                    self.activity_dict[key] = activity
