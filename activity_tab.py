# activity_tab.py - 활동 관리 탭 (결석자 기반 수정)

import tkinter as tk
from tkinter import messagebox

# create_activity_tab 함수 정의
def create_activity_tab(notebook, activity_service, member_service):
    # 탭 프레임 생성
    activity_frame = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(activity_frame, text="활동 관리")

    # 입력 영역 프레임
    input_frame = tk.LabelFrame(activity_frame, text="활동 입력", padx=10, pady=10)
    input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

    # 제목 입력
    tk.Label(input_frame, text="제목").grid(row=0, column=0, sticky="e")
    title_entry = tk.Entry(input_frame, width=30)
    title_entry.grid(row=0, column=1, pady=2)

    # 날짜 입력
    tk.Label(input_frame, text="날짜").grid(row=1, column=0, sticky="e")
    date_entry = tk.Entry(input_frame, width=30)
    date_entry.grid(row=1, column=1, pady=2)

    # 내용 입력
    tk.Label(input_frame, text="내용").grid(row=2, column=0, sticky="ne")
    desc_text = tk.Text(input_frame, height=4, width=30)
    desc_text.grid(row=2, column=1, pady=2)

    # 결석자 학번 입력 (쉼표 구분)
    tk.Label(input_frame, text="결석자 학번(쉼표)").grid(row=3, column=0, sticky="e")
    absentees_entry = tk.Entry(input_frame, width=30)
    absentees_entry.grid(row=3, column=1, pady=2)

    # 버튼 영역 프레임
    button_frame = tk.Frame(activity_frame)
    button_frame.grid(row=1, column=0, columnspan=2, pady=5)

    # 활동 등록 함수
    def add_activity():
        title = title_entry.get().strip()
        date = date_entry.get().strip()
        desc = desc_text.get("1.0", tk.END).strip()
        absentees = [p.strip() for p in absentees_entry.get().split(',') if p.strip()]
        if not title or not date:
            messagebox.showwarning("입력 오류", "제목과 날짜는 필수 입력 항목입니다.")
            return
        msg = activity_service.add_activity(title, date, desc, absentees)
        messagebox.showinfo("등록 결과", msg)
        # 입력 필드 초기화
        title_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        desc_text.delete("1.0", tk.END)
        absentees_entry.delete(0, tk.END)
        refresh_activity_list()

    # 활동 삭제 함수
    def delete_activity():
        selected = activity_listbox.curselection()
        if not selected:
            messagebox.showwarning("선택 없음", "삭제할 활동을 선택하세요.")
            return
        key = activity_listbox.get(selected[0])
        msg = activity_service.delete_activity_by_key(key)
        messagebox.showinfo("삭제 결과", msg)
        detail_text.delete("1.0", tk.END)
        refresh_activity_list()

    # 등록/삭제 버튼 배치
    tk.Button(button_frame, text="활동 등록", command=add_activity, width=20).pack(side="left", padx=5)
    tk.Button(button_frame, text="선택한 활동 삭제", command=delete_activity, width=20).pack(side="left", padx=5)

    # 활동 목록 표시
    tk.Label(activity_frame, text="활동 목록").grid(row=2, column=0, sticky="w")
    activity_listbox = tk.Listbox(activity_frame, height=8, width=40)
    activity_listbox.grid(row=3, column=0, padx=5, pady=5)

    # 상세 정보 영역 (결석자 표시)
    tk.Label(activity_frame, text="상세 정보").grid(row=2, column=1, sticky="w")
    detail_text = tk.Text(activity_frame, height=8, width=50)
    detail_text.grid(row=3, column=1, padx=5, pady=5)

    # 활동 목록 갱신 함수
    def refresh_activity_list():
        activity_listbox.delete(0, tk.END)
        for key in activity_service.get_activity_titles():
            activity_listbox.insert(tk.END, key)

    # 상세 정보 표시 함수 (결석자 기준)
    def show_detail(event):
        selection = activity_listbox.curselection()
        if not selection:
            return
        key = activity_listbox.get(selection[0])
        a = activity_service.activity_dict.get(key)
        detail_text.delete("1.0", tk.END)
        if a:
            detail_text.insert(
                tk.END,
                f"제목: {a['title']}\n날짜: {a['date']}\n내용: {a['description']}\n결석자: {', '.join(a['participants']) if a['participants'] else '없음'}"
            )

    # 이벤트 바인딩 및 초기 로드
    activity_listbox.bind("<<ListboxSelect>>", show_detail)
    refresh_activity_list()
