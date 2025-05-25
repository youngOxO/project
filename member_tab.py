# member_tab.py
import tkinter as tk
from tkinter import messagebox

def create_member_tab(notebook, member_service):
    member_frame = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(member_frame, text="동아리원 관리")

    tk.Label(member_frame, text="이름").grid(row=0, column=0, sticky="e")
    name_entry = tk.Entry(member_frame)
    name_entry.grid(row=0, column=1)

    tk.Label(member_frame, text="학번").grid(row=1, column=0, sticky="e")
    id_entry = tk.Entry(member_frame)
    id_entry.grid(row=1, column=1)

    tk.Label(member_frame, text="연락처").grid(row=2, column=0, sticky="e")
    phone_entry = tk.Entry(member_frame)
    phone_entry.grid(row=2, column=1)

    tk.Label(member_frame, text="역할").grid(row=3, column=0, sticky="e")
    role_entry = tk.Entry(member_frame)
    role_entry.grid(row=3, column=1)
    role_entry.insert(0, "일반")

    member_output = tk.Text(member_frame, height=10, width=50)
    member_output.grid(row=5, column=0, columnspan=2, pady=10)

    def register():
        name = name_entry.get()
        student_id = id_entry.get()
        phone = phone_entry.get()
        role = role_entry.get()
        success, msg = member_service.add_member(name, student_id, phone, role)
        messagebox.showinfo("등록 결과", msg)
        if success:
            name_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            role_entry.delete(0, tk.END)
            role_entry.insert(0, "일반")
            load_members()

    def delete_member():
        student_id = id_entry.get()
        success, msg = member_service.delete_member(student_id)
        messagebox.showinfo("삭제 결과", msg)
        if success:
            load_members()

    def show_members():
        member_output.delete("1.0", tk.END)
        member_output.insert(tk.END, member_service.get_members_text())

    def load_members():
        show_members()

    tk.Button(member_frame, text="등록", command=register).grid(row=4, column=0)
    tk.Button(member_frame, text="삭제", command=delete_member).grid(row=4, column=1)
    tk.Button(member_frame, text="목록 보기", command=show_members).grid(row=6, column=0, columnspan=2)

    load_members()
