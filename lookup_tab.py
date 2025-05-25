# lookup_tab.py - 동아리원 조회 탭 (결석자 제외 참여 내역 표시)

import tkinter as tk
from tkinter import ttk

# 회원 및 활동 서비스 주입

def create_lookup_tab(notebook, activity_service, member_service):
    # 탭 프레임 설정
    lookup_frame = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(lookup_frame, text="동아리원 조회")

    # 동아리원 목록
    tk.Label(lookup_frame, text="동아리원 목록").grid(row=0, column=0, padx=10, pady=5)
    member_listbox = tk.Listbox(lookup_frame, height=10, width=30)
    member_listbox.grid(row=1, column=0, padx=10, pady=5)

    # 참여(결석자 제외) 활동 출력
    tk.Label(lookup_frame, text="참여한 활동").grid(row=0, column=1, padx=10, pady=5)
    activity_text = tk.Text(lookup_frame, height=12, width=60)
    activity_text.grid(row=1, column=1, padx=10, pady=5)

    # 동아리원 목록 로드 및 정렬
    def load_members():
        member_listbox.delete(0, tk.END)
        members_sorted = sorted(member_service.get_all_members(), key=lambda m: m.student_id)
        for m in members_sorted:
            member_listbox.insert(tk.END, f"{m.name} ({m.student_id})")

    # 선택 학생의 참여 활동(결석 제외) 표시
    def show_member_activities(event):
        sel = member_listbox.curselection()
        if not sel:
            return
        selected = member_listbox.get(sel[0])
        student_id = selected.split("(")[-1].strip(")")

        # 활동 중 결석자 명단을 보고 제외된 활동만 표시
        activity_text.delete("1.0", tk.END)
        attended = []
        for act in activity_service.activities:
            key = f"{act['title']} ({act['date']})"
            absentees = set(act.get('participants', []))  # participants 필드가 결석자 학번 저장용
            if student_id not in absentees:
                attended.append(key)

        if attended:
            activity_text.insert(tk.END, "\n".join(attended))
        else:
            activity_text.insert(tk.END, "참여한 활동이 없습니다.")

    # 이벤트 바인딩 및 초기 실행
    member_listbox.bind("<<ListboxSelect>>", show_member_activities)
    load_members()
