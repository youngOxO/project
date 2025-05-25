# member_service.py (CSV 저장/불러오기 버전)

import csv
import os
from member import Member

class MemberService:
    def __init__(self, filename="members.csv"):
        self.filename = filename
        self.members = []
        self.member_dict = {}
        self.load_members()

    def load_members(self):
        if os.path.exists(self.filename):
            with open(self.filename, newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    member = Member(
                        name=row["name"],
                        student_id=row["student_id"],
                        phone=row["phone"],
                        role=row["role"]
                    )
                    self.members.append(member)
                    self.member_dict[member.student_id] = member

    def save_members(self):
        with open(self.filename, mode='w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ["name", "student_id", "phone", "role"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for member in self.members:
                writer.writerow({
                    "name": member.name,
                    "student_id": member.student_id,
                    "phone": member.phone,
                    "role": member.role
                })

    def add_member(self, name, student_id, phone, role):
        if student_id in self.member_dict:
            return False, "이미 등록된 학번입니다."
        member = Member(name, student_id, phone, role)
        self.members.append(member)
        self.member_dict[student_id] = member
        self.save_members()
        return True, f"{name} 학생이 등록되었습니다."

    def delete_member(self, student_id):
        if student_id in self.member_dict:
            member = self.member_dict[student_id]
            self.members = [m for m in self.members if m.student_id != student_id]
            del self.member_dict[student_id]
            self.save_members()
            return True, f"{member.name} 학생이 삭제되었습니다."
        return False, "해당 학번의 동아리원을 찾을 수 없습니다."

    def get_members_text(self):
        if not self.members:
            return "등록된 동아리원이 없습니다."
        return "\n".join(str(m) for m in self.members)

    def get_all_members(self):
        return self.members
