import tkinter as tk
from tkinter import messagebox, ttk
from activity_service import ActivityService
from student_report_write import create_report_write_tab
from student_report_view import create_report_view_tab

# GUI 실행 함수 (student_id 전달)
def launch_student_gui(student_id):
    activity_service = ActivityService()

    root = tk.Tk()
    root.title(f"{student_id} - 활동 보고서 작성 및 조회")
    root.geometry("650x500")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # 탭 등록
    create_report_write_tab(notebook, student_id, activity_service)
    create_report_view_tab(notebook, student_id)

    root.mainloop()