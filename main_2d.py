"""
tkinter 2D 오목 게임 메인 실행 파일
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    from tkinter_gui import TkinterGUI
    
    def run_2d_game():
        """2D 오목 게임을 실행합니다."""
        print("tkinter 2D 오목 게임을 시작합니다...")
        
        # tkinter 루트 윈도우 생성
        root = tk.Tk()
        
        # GUI 앱 생성 및 실행
        app = TkinterGUI(root)
        app.run()
        
    if __name__ == "__main__":
        run_2d_game()
        
except ImportError as e:
    print(f"tkinter 모듈을 찾을 수 없습니다: {e}")
    print("Python에 tkinter가 설치되어 있는지 확인해주세요.")
    sys.exit(1)
except Exception as e:
    print(f"2D 게임 실행 중 오류가 발생했습니다: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 