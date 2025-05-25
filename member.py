class Member:
    def __init__(self, name, student_id, phone, role="일반"):
        self.name = name
        self.student_id = student_id
        self.phone = phone
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.role}, 연락처: {self.phone}"

    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "phone": self.phone,
            "role": self.role
        }

    @staticmethod
    def from_dict(data):
        return Member(data["name"], data["student_id"], data["phone"], data["role"])