"""
닉네임 입력 다이얼로그
게임 시작 전 플레이어들의 닉네임을 입력받는 창입니다.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Tuple, Optional


class NicknameDialog:
    """닉네임 입력 다이얼로그 클래스"""
    
    def __init__(self, parent: tk.Tk):
        """
        닉네임 다이얼로그 초기화
        
        Args:
            parent (tk.Tk): 부모 윈도우
        """
        self.parent = parent
        self.result: Optional[Tuple[str, str]] = None
        
        # 다이얼로그 윈도우 생성
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("플레이어 닉네임 입력")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # 모달 설정 (부모 윈도우 비활성화)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 다이얼로그를 최상위로 설정
        self.dialog.attributes('-topmost', True)
        self.dialog.focus_force()
        
        self._create_widgets()
        self._center_window()
    
    def _create_widgets(self):
        """위젯들을 생성합니다."""
        # 메인 프레임
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # 제목
        title_label = tk.Label(main_frame, text="플레이어 닉네임을 입력하세요", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 플레이어 1 프레임
        player1_frame = tk.Frame(main_frame)
        player1_frame.pack(fill="x", pady=(0, 15))
        
        player1_label = tk.Label(player1_frame, text="플레이어 1 (흑돌):", 
                                font=("Arial", 12), width=15, anchor="w")
        player1_label.pack(side="left")
        
        self.player1_entry = tk.Entry(player1_frame, font=("Arial", 12), width=20)
        self.player1_entry.pack(side="left", padx=(10, 0))
        self.player1_entry.insert(0, "플레이어 1")
        self.player1_entry.select_range(0, tk.END)
        self.player1_entry.focus()
        
        # 플레이어 2 프레임
        player2_frame = tk.Frame(main_frame)
        player2_frame.pack(fill="x", pady=(0, 20))
        
        player2_label = tk.Label(player2_frame, text="플레이어 2 (백돌):", 
                                font=("Arial", 12), width=15, anchor="w")
        player2_label.pack(side="left")
        
        self.player2_entry = tk.Entry(player2_frame, font=("Arial", 12), width=20)
        self.player2_entry.pack(side="left", padx=(10, 0))
        self.player2_entry.insert(0, "플레이어 2")
        
        # 설명 텍스트
        info_text = "빈칸으로 두면 기본 닉네임이 사용됩니다."
        info_label = tk.Label(main_frame, text=info_text, 
                             font=("Arial", 10), fg="gray")
        info_label.pack(pady=(0, 20))
        
        # 버튼 프레임
        button_frame = tk.Frame(main_frame)
        button_frame.pack()
        
        # 시작 버튼
        start_button = tk.Button(button_frame, text="게임 시작", 
                                command=self._on_start,
                                font=("Arial", 12, "bold"),
                                bg="#4CAF50", fg="white",
                                padx=20, pady=5)
        start_button.pack(side="left", padx=(0, 10))
        
        # 취소 버튼
        cancel_button = tk.Button(button_frame, text="취소", 
                                 command=self._on_cancel,
                                 font=("Arial", 12),
                                 bg="#f44336", fg="white",
                                 padx=20, pady=5)
        cancel_button.pack(side="left")
        
        # Enter 키 바인딩
        self.dialog.bind("<Return>", lambda e: self._on_start())
        self.dialog.bind("<Escape>", lambda e: self._on_cancel())
    
    def _center_window(self):
        """윈도우를 화면 중앙에 위치시킵니다."""
        self.dialog.update_idletasks()
        
        # 화면 크기 가져오기
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        # 윈도우 크기 설정 (고정 크기)
        window_width = 400
        window_height = 300
        
        # 중앙 위치 계산
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # 윈도우 위치 설정
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _on_start(self):
        """게임 시작 버튼 클릭 처리"""
        player1_name = self.player1_entry.get().strip()
        player2_name = self.player2_entry.get().strip()
        
        # 빈칸이면 기본값 사용
        if not player1_name:
            player1_name = "플레이어 1"
        if not player2_name:
            player2_name = "플레이어 2"
        
        # 같은 닉네임인지 확인
        if player1_name == player2_name:
            messagebox.showwarning("경고", "플레이어들의 닉네임이 같습니다.\n다른 닉네임을 입력해주세요.")
            return
        
        self.result = (player1_name, player2_name)
        self.dialog.destroy()
    
    def _on_cancel(self):
        """취소 버튼 클릭 처리"""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[Tuple[str, str]]:
        """
        다이얼로그를 표시하고 결과를 반환합니다.
        
        Returns:
            Optional[Tuple[str, str]]: (플레이어1 닉네임, 플레이어2 닉네임) 또는 None
        """
        try:
            print("다이얼로그 표시 시작...")
            self.dialog.wait_window()
            print("다이얼로그 닫힘, 결과 반환")
            return self.result
        except Exception as e:
            print(f"다이얼로그 표시 오류: {e}")
            return None


def get_nicknames(parent: tk.Tk) -> Optional[Tuple[str, str]]:
    """
    닉네임 입력 다이얼로그를 표시하고 결과를 반환합니다.
    
    Args:
        parent (tk.Tk): 부모 윈도우
        
    Returns:
        Optional[Tuple[str, str]]: (플레이어1 닉네임, 플레이어2 닉네임) 또는 None
    """
    dialog = NicknameDialog(parent)
    return dialog.show() 