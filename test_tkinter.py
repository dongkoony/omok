"""
tkinter 테스트 파일
"""

import tkinter as tk
from tkinter import messagebox

def test_tkinter():
    """tkinter 기본 기능 테스트"""
    try:
        # 루트 윈도우 생성
        root = tk.Tk()
        root.title("tkinter 테스트")
        root.geometry("300x200")
        
        # 라벨 추가
        label = tk.Label(root, text="tkinter가 정상적으로 작동합니다!", font=("Arial", 14))
        label.pack(pady=50)
        
        # 버튼 추가
        def show_message():
            messagebox.showinfo("테스트", "메시지 박스도 정상 작동합니다!")
        
        button = tk.Button(root, text="테스트 버튼", command=show_message)
        button.pack(pady=20)
        
        print("tkinter 테스트 시작...")
        root.mainloop()
        print("tkinter 테스트 완료!")
        
    except Exception as e:
        print(f"tkinter 테스트 실패: {e}")

if __name__ == "__main__":
    test_tkinter() 