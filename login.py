# login.py - 로그인 창 (학생/선생님 로그인 분리)

import tkinter as tk
from tkinter import messagebox
from main import launch_gui  # 선생님용 메인 앱 실행
from student_report_gui import launch_student_gui  # 학생 보고서 창 실행
from member_service import MemberService

# 로그인 정보
TEACHERS = {"teacher": "1234"}  # 선생님 계정 딕셔너리 구조

member_service = MemberService()

# 로그인 실행
root = tk.Tk()
root.title("로그인")
root.geometry("300x200")

role_var = tk.StringVar(value="student")

def try_login():
    user_id = id_entry.get().strip()
    pw = pw_entry.get().strip()
    role = role_var.get()

    if role == "teacher":
        if user_id in TEACHERS and pw == TEACHERS[user_id]:
            messagebox.showinfo("성공", "선생님 로그인 성공")
            root.destroy()
            launch_gui()  # 학생은 보고서 작성 GUI 실행  # 선생님은 메인 GUI 실행
        else:
            messagebox.showerror("실패", "아이디 또는 비밀번호가 틀렸습니다")

    elif role == "student":
        # 학번 기반 인증 (비밀번호는 생략 또는 학번 동일 처리 가능)
        student_ids = set(m.student_id for m in member_service.get_all_members())  # set으로 검색 성능 향상
        if user_id in student_ids and pw == user_id:
            messagebox.showinfo("성공", f"{user_id} 학생 로그인 성공")
            root.destroy()
            launch_student_gui(user_id)
        else:
            messagebox.showerror("실패", "학번이 등록되지 않았거나 비밀번호가 학번과 일치하지 않습니다")

# 역할 선택
tk.Label(root, text="역할 선택").pack(pady=5)
tk.Radiobutton(root, text="학생", variable=role_var, value="student").pack()
tk.Radiobutton(root, text="선생님", variable=role_var, value="teacher").pack()

# 아이디 입력
tk.Label(root, text="아이디").pack()
id_entry = tk.Entry(root)
id_entry.pack()

# 비밀번호 입력
tk.Label(root, text="비밀번호").pack()
pw_entry = tk.Entry(root, show="*")
pw_entry.pack()

# 로그인 버튼
tk.Button(root, text="로그인", command=try_login).pack(pady=10)

root.mainloop()
