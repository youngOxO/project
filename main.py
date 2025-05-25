# main.py - GUI 실행 진입점

import tkinter as tk
from tkinter import ttk
from member_tab import create_member_tab
from activity_tab import create_activity_tab
from activity_service import ActivityService
from member_service import MemberService
from lookup_tab import create_lookup_tab
from teacher_report_review import create_teacher_report_tab

#print("📁 activities.csv 저장 위치:", os.path.abspath(self.filename))


def launch_gui():
    root = tk.Tk()
    root.title("동아리 관리 프로그램")

    activity_service = ActivityService()
    member_service = MemberService()

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, fill="both", expand=True)

    # 탭 분리: 외부 모듈에서 탭 생성
    create_member_tab(notebook, member_service)
    create_activity_tab(notebook, activity_service, member_service)
    create_lookup_tab(notebook, activity_service, member_service)
    create_teacher_report_tab(notebook)  # 보고서 피드백 탭 추가

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
