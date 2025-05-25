# student_report_view.py - 내가 쓴 보고서 보기 탭 (피드백 표시 기능 수정)

import tkinter as tk
import csv
import os

REPORTS_FILE = "activity_reports.csv"
FEEDBACK_FILE = "activity_feedback.csv"

# 보고서 보기 탭 생성 함수
def create_report_view_tab(notebook, student_id):
    view_frame = tk.Frame(notebook)
    notebook.add(view_frame, text="내 보고서 보기")

    # 내가 작성한 보고서 목록
    tk.Label(view_frame, text="내가 작성한 보고서").pack(pady=(5,0))
    report_listbox = tk.Listbox(view_frame, width=60, height=10)
    report_listbox.pack(pady=5)

    # 보고서 상세 내용 표시
    tk.Label(view_frame, text="보고서 내용").pack(pady=(5,0))
    detail_text = tk.Text(view_frame, width=70, height=8)
    detail_text.pack(pady=5)

    # 피드백 표시 영역 (초기에는 숨김)
    feedback_label = tk.Label(view_frame, text="피드백")
    feedback_text = tk.Text(view_frame, width=70, height=5)

    # 보고서 목록 로드 함수
    def load_reports():
        report_listbox.delete(0, tk.END)
        if os.path.exists(REPORTS_FILE):
            with open(REPORTS_FILE, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['student_id'] == student_id:
                        report_listbox.insert(tk.END, row['activity'])

    # 선택된 보고서 상세 및 피드백 표시 함수
    def show_detail(event):
        selection = report_listbox.curselection()
        if not selection:
            return
        activity_key = report_listbox.get(selection[0])

        # 보고서 내용 표시
        detail_text.delete("1.0", tk.END)
        with open(REPORTS_FILE, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['student_id'] == student_id and row['activity'] == activity_key:
                    detail_text.insert(tk.END, row['report'])
                    break

        # 피드백 표시 여부 초기화
        feedback_label.pack_forget()
        feedback_text.pack_forget()

        # 피드백 존재 여부 확인 및 표시
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['student_id'] == student_id and row['activity'] == activity_key:
                        feedback_label.pack(pady=(10,0))
                        feedback_text.pack(pady=5)
                        feedback_text.delete("1.0", tk.END)
                        feedback_text.insert(tk.END, row['feedback'])
                        break

    # 이벤트 바인딩 및 초기 실행
    report_listbox.bind("<<ListboxSelect>>", show_detail)
    load_reports()
