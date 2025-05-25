# student_report_write.py - 보고서 작성 탭 정의

import tkinter as tk
from tkinter import messagebox
import csv
import os

REPORTS_FILE = "activity_reports.csv"

def save_report(student_id, activity_key, report_text):
    file_exists = os.path.exists(REPORTS_FILE)
    with open(REPORTS_FILE, "a", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["student_id", "activity", "report"])
        writer.writerow([student_id, activity_key, report_text.strip()])

def create_report_write_tab(notebook, student_id, activity_service):
    write_frame = tk.Frame(notebook)
    notebook.add(write_frame, text="보고서 작성")

    tk.Label(write_frame, text="활동 선택").pack()
    activity_listbox = tk.Listbox(write_frame, width=50, height=5)
    activity_listbox.pack(pady=5)

    for title in activity_service.get_activity_titles():
        activity_listbox.insert(tk.END, title)

    tk.Label(write_frame, text="보고서 내용").pack()
    report_text = tk.Text(write_frame, width=70, height=10)
    report_text.pack(pady=5)

    def submit():
        selection = activity_listbox.curselection()
        if not selection:
            messagebox.showwarning("선택 없음", "활동을 선택하세요")
            return
        activity_key = activity_listbox.get(selection[0])
        text = report_text.get("1.0", tk.END)
        if not text.strip():
            messagebox.showwarning("내용 없음", "보고서 내용을 입력하세요")
            return
        save_report(student_id, activity_key, text)
        messagebox.showinfo("제출 완료", "보고서가 제출되었습니다")
        report_text.delete("1.0", tk.END)

    tk.Button(write_frame, text="보고서 제출", command=submit).pack(pady=10)
