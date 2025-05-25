# teacher_report_review.py - 선생님 보고서 열람 및 피드백

import tkinter as tk
from tkinter import messagebox
import csv
import os

REPORTS_FILE = "activity_reports.csv"
FEEDBACK_FILE = "activity_feedback.csv"

# 보고서 및 피드백 열람 인터페이스

def create_teacher_report_tab(notebook):
    tab = tk.Frame(notebook)
    notebook.add(tab, text="보고서 피드백")

    tk.Label(tab, text="제출된 보고서 목록").pack()
    report_listbox = tk.Listbox(tab, width=80, height=10)
    report_listbox.pack(pady=5)

    detail_text = tk.Text(tab, width=85, height=10)
    detail_text.pack(pady=5)

    tk.Label(tab, text="피드백 입력").pack()
    feedback_entry = tk.Text(tab, width=85, height=4)
    feedback_entry.pack(pady=5)

    reports = []  # (student_id, activity, report) 저장용

    def load_reports():
        activity_absentees = {}
        from activity_service import ActivityService
        service = ActivityService()
        for act in service.activities:
            key = f"{act['title']} ({act['date']})"
            activity_absentees[key] = set(act.get("absentees", []))

        if os.path.exists(REPORTS_FILE):
            with open(REPORTS_FILE, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    student_id = row['student_id']
                    activity = row['activity']
                    if student_id in activity_absentees.get(activity, set()):
                        continue  # 결석자는 제외
                    reports.append((student_id, activity, row['report']))
                    report_listbox.insert(tk.END, f"{student_id} - {activity}")

    def show_selected_report(event):
        selection = report_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        student_id, activity, report = reports[idx]
        detail_text.delete("1.0", tk.END)
        detail_text.insert(tk.END, report)
        feedback_entry.delete("1.0", tk.END)
        # 피드백 로딩
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['student_id'] == student_id and row['activity'] == activity:
                        feedback_entry.insert(tk.END, row['feedback'])
                        break

    def save_feedback():
        selection = report_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        student_id, activity, _ = reports[idx]
        feedback = feedback_entry.get("1.0", tk.END).strip()

        # 기존 피드백 덮어쓰기
        feedback_data = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, newline='', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                feedback_data = list(reader)

        updated = False
        for row in feedback_data:
            if row['student_id'] == student_id and row['activity'] == activity:
                row['feedback'] = feedback
                updated = True
                break

        if not updated:
            feedback_data.append({"student_id": student_id, "activity": activity, "feedback": feedback})

        with open(FEEDBACK_FILE, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["student_id", "activity", "feedback"])
            writer.writeheader()
            writer.writerows(feedback_data)

        messagebox.showinfo("완료", "피드백이 저장되었습니다.")

    report_listbox.bind("<<ListboxSelect>>", show_selected_report)
    tk.Button(tab, text="피드백 저장", command=save_feedback).pack(pady=10)

    load_reports()
