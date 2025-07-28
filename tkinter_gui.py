"""
tkinter 2D 오목 게임 GUI
기존 게임 로직을 활용하여 2D 환경에서 오목을 구현합니다.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple, List
import math

from game import Game, GameState
from player import StoneColor
from nickname_dialog import get_nicknames


class TkinterGUI:
    """tkinter 2D 오목 게임 GUI 클래스"""
    
    def __init__(self, root: tk.Tk):
        """tkinter GUI 초기화"""
        self.root = root
        self.root.title("오목 게임 (2D)")
        
        # 게임 인스턴스
        self.game: Optional[Game] = None
        
        # 캔버스 설정
        self.canvas_width = 800
        self.canvas_height = 800
        self.board_size = 15
        self.cell_size = self.canvas_width // (self.board_size + 1)
        self.stone_radius = self.cell_size // 2 - 2
        
        # UI 요소들
        self.canvas: Optional[tk.Canvas] = None
        self.status_label: Optional[tk.Label] = None
        self.score_label: Optional[tk.Label] = None
        self.new_game_button: Optional[tk.Button] = None
        
        # 쌍삼 표시
        self.double_three_indicator: Optional[int] = None
        
        # 닉네임 입력
        self.get_player_nicknames()
        
        # GUI 초기화
        if self.game:
            self.create_widgets()
            self.draw_board()
            self.update_display()
            self.center_main_window()
    
    def get_player_nicknames(self):
        """플레이어 닉네임을 입력받습니다."""
        try:
            nicknames = get_nicknames(self.root)
            if nicknames is None:
                # 취소된 경우 프로그램 종료
                self.root.quit()
                return
            
            player1_name, player2_name = nicknames
            self.game = Game(player1_name, player2_name)
            
            # 게임 콜백 설정
            self.game.set_callbacks(
                on_state_change=self.update_display,
                on_win=self.handle_win,
                on_draw=self.handle_draw
            )
            
        except Exception as e:
            print(f"닉네임 입력 오류: {e}")
            # 기본 닉네임 사용
            self.game = Game("플레이어 1", "플레이어 2")
    
    def create_widgets(self):
        """위젯들을 생성합니다."""
        # 메인 프레임
        main_frame = tk.Frame(self.root, bg="#f5e6d3", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # 제목
        title_label = tk.Label(
            main_frame,
            text="오목 게임",
            font=("Segoe UI", 24, "bold"),
            fg="#8b4513",
            bg="#f5e6d3"
        )
        title_label.pack(pady=(0, 20))
        
        # 상태 표시 프레임
        status_frame = tk.Frame(main_frame, bg="#f5e6d3")
        status_frame.pack(fill="x", pady=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 14),
            fg="#8b4513",
            bg="#f5e6d3"
        )
        self.status_label.pack()
        
        self.score_label = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 12),
            fg="#a0522d",
            bg="#f5e6d3"
        )
        self.score_label.pack()
        
        # 캔버스 프레임
        canvas_frame = tk.Frame(main_frame, bg="#34495e", relief="raised", bd=3)
        canvas_frame.pack(pady=20)
        
        # 캔버스
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#e8c39e",  # 밝은 나무색 배경
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # 마우스 이벤트 바인딩
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        
        # 버튼 프레임
        button_frame = tk.Frame(main_frame, bg="#f5e6d3")
        button_frame.pack(pady=20)
        
        # 새 게임 버튼
        self.new_game_button = tk.Button(
            button_frame,
            text="새 게임",
            font=("Segoe UI", 12, "bold"),
            bg="#d2691e",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            command=self.new_game
        )
        self.new_game_button.pack(side="left", padx=10)
        
        # 무르기 버튼
        undo_button = tk.Button(
            button_frame,
            text="무르기",
            font=("Segoe UI", 12, "bold"),
            bg="#cd853f",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            command=self.undo_move
        )
        undo_button.pack(side="left", padx=10)
        
        # 종료 버튼
        exit_button = tk.Button(
            button_frame,
            text="종료",
            font=("Segoe UI", 12, "bold"),
            bg="#b8860b",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            command=self.root.quit
        )
        exit_button.pack(side="left", padx=10)
        
        # 무르기 버튼 참조 저장
        self.undo_button = undo_button
        
        # 버튼 호버 효과 설정
        self.setup_button_hover_effects()
    
    def setup_button_hover_effects(self):
        """버튼 호버 효과를 설정합니다."""
        def on_enter(event):
            if "새 게임" in event.widget.cget("text"):
                event.widget.config(bg="#ff8c00")
            elif "무르기" in event.widget.cget("text"):
                event.widget.config(bg="#daa520")
            else:
                event.widget.config(bg="#ffd700")
        
        def on_leave(event):
            if "새 게임" in event.widget.cget("text"):
                event.widget.config(bg="#d2691e")
            elif "무르기" in event.widget.cget("text"):
                event.widget.config(bg="#cd853f")
            else:
                event.widget.config(bg="#b8860b")
        
        for button in [self.new_game_button, self.undo_button, self.root.winfo_children()[0].winfo_children()[-1].winfo_children()[-1]]:
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
    
    def center_main_window(self):
        """메인 윈도우를 화면 중앙에 위치시킵니다."""
        self.root.update_idletasks()
        
        # 윈도우 크기 설정
        window_width = 900
        window_height = 1000
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(window_width, window_height)
        
        # 화면 중앙 계산
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def draw_board(self):
        """오목판을 그립니다."""
        if not self.canvas:
            return
        
        # 격자선 그리기
        for i in range(self.board_size + 1):
            x = (i + 1) * self.cell_size
            
            # 세로선
            self.canvas.create_line(
                x, self.cell_size, x, self.canvas_height - self.cell_size,
                fill="#000000", width=2
            )
            
            # 가로선
            self.canvas.create_line(
                self.cell_size, x, self.canvas_width - self.cell_size, x,
                fill="#000000", width=2
            )
        
        # 화점 그리기
        star_points = [3, 7, 11]
        for i in star_points:
            for j in star_points:
                x = (i + 1) * self.cell_size
                y = (j + 1) * self.cell_size
                
                # 화점 (별 모양)
                self.canvas.create_oval(
                    x - 4, y - 4, x + 4, y + 4,
                    fill="#000000", outline="#000000"
                )
        
        # 3D 효과 추가
        self.create_3d_board_effects()
    
    def create_3d_board_effects(self):
        """오목판에 3D 효과를 추가합니다."""
        # 오목판 가장자리 그림자
        shadow_color = "#654321"
        self.canvas.create_rectangle(
            5, 5, self.canvas_width - 5, self.canvas_height - 5,
            outline=shadow_color, width=3
        )
        
        # 격자선에 미묘한 그림자 효과
        for i in range(self.board_size + 1):
            x = (i + 1) * self.cell_size
            
            # 세로선 그림자
            self.canvas.create_line(
                x + 1, self.cell_size, x + 1, self.canvas_height - self.cell_size,
                fill="#8b4513", width=1
            )
            
            # 가로선 그림자
            self.canvas.create_line(
                self.cell_size, x + 1, self.canvas_width - self.cell_size, x + 1,
                fill="#8b4513", width=1
            )
    
    def draw_stone(self, row: int, col: int, stone_color: StoneColor):
        """돌을 그립니다."""
        if not self.canvas:
            return
        
        # 보드 좌표를 캔버스 좌표로 변환
        x = (col + 1) * self.cell_size
        y = (row + 1) * self.cell_size
        
        # 돌 색상 설정
        if stone_color == StoneColor.BLACK:
            fill_color = "#000000"
            outline_color = "#1a1a1a"
            shadow_color = "#1a1a1a"
            highlight_color = "#333333"
        else:
            fill_color = "#ffffff"
            outline_color = "#f0f0f0"
            shadow_color = "#f0f0f0"
            highlight_color = "#ffffff"
        
        # 그림자 효과 (3D 느낌)
        self.canvas.create_oval(
            x - self.stone_radius + 2, y - self.stone_radius + 2,
            x + self.stone_radius + 2, y + self.stone_radius + 2,
            fill=shadow_color, outline=shadow_color
        )
        
        # 메인 돌
        self.canvas.create_oval(
            x - self.stone_radius, y - self.stone_radius,
            x + self.stone_radius, y + self.stone_radius,
            fill=fill_color, outline=outline_color, width=2
        )
        
        # 하이라이트 효과 (3D 느낌)
        highlight_radius = self.stone_radius // 3
        self.canvas.create_oval(
            x - highlight_radius, y - highlight_radius,
            x + highlight_radius, y + highlight_radius,
            fill=highlight_color, outline="", stipple="gray50"
        )
    
    def on_canvas_click(self, event):
        """캔버스 클릭 이벤트를 처리합니다."""
        if not self.game or self.game.is_game_over():
            return
        
        # 클릭 위치를 보드 좌표로 변환
        col = round((event.x - self.cell_size) / self.cell_size)
        row = round((event.y - self.cell_size) / self.cell_size)
        
        # 유효한 위치인지 확인
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            # 현재 플레이어의 돌 색상 저장
            current_stone_color = self.game.get_current_player().get_stone_color()
            
            if self.game.make_move(row, col):
                # 돌을 그리기 (승리하지 않은 경우에만)
                if self.game.get_game_state() == GameState.PLAYING:
                    self.draw_stone(row, col, current_stone_color)
                # 승리한 경우에는 handle_win에서 돌을 그리므로 여기서는 그리지 않음
            else:
                # 잘못된 이동 표시
                self.show_invalid_move_indicator(row, col)
    
    def on_canvas_motion(self, event):
        """캔버스 마우스 움직임 이벤트를 처리합니다."""
        if not self.game or self.game.is_game_over():
            return
        
        # 마우스 위치를 보드 좌표로 변환
        col = round((event.x - self.cell_size) / self.cell_size)
        row = round((event.y - self.cell_size) / self.cell_size)
        
        # 유효한 위치인지 확인
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.game.get_board().is_empty(row, col):
                stone_color = self.game.get_current_player().get_stone_color()
                if self.game.get_board().check_double_three(row, col, stone_color):
                    self.show_double_three_indicator(row, col)
                else:
                    self.clear_double_three_indicator()
    
    def show_double_three_indicator(self, row: int, col: int):
        """쌍삼 표시기를 보여줍니다."""
        self.clear_double_three_indicator()
        
        if not self.canvas:
            return
        
        # 보드 좌표를 캔버스 좌표로 변환
        x = (col + 1) * self.cell_size
        y = (row + 1) * self.cell_size
        
        # 반투명 빨간색 원
        self.double_three_indicator = self.canvas.create_oval(
            x - self.stone_radius, y - self.stone_radius,
            x + self.stone_radius, y + self.stone_radius,
            fill="#ff0000", outline="#cc0000", width=2,
            stipple="gray25"  # 반투명 효과
        )
        
        # X 표시
        x_size = self.stone_radius // 2
        self.canvas.create_line(
            x - x_size, y - x_size, x + x_size, y + x_size,
            fill="#ffffff", width=3
        )
        self.canvas.create_line(
            x - x_size, y + x_size, x + x_size, y - x_size,
            fill="#ffffff", width=3
        )
    
    def clear_double_three_indicator(self):
        """쌍삼 표시기를 제거합니다."""
        if self.double_three_indicator and self.canvas:
            self.canvas.delete(self.double_three_indicator)
            self.double_three_indicator = None
    
    def show_invalid_move_indicator(self, row: int, col: int):
        """잘못된 이동 표시기를 보여줍니다."""
        if not self.canvas:
            return
        
        # 보드 좌표를 캔버스 좌표로 변환
        x = (col + 1) * self.cell_size
        y = (row + 1) * self.cell_size
        
        # 빨간색 원 (1초 후 제거)
        indicator = self.canvas.create_oval(
            x - self.stone_radius, y - self.stone_radius,
            x + self.stone_radius, y + self.stone_radius,
            fill="#ff0000", outline="#cc0000", width=2,
            stipple="gray25"
        )
        
        # 1초 후 제거
        self.root.after(1000, lambda: self.canvas.delete(indicator))
    
    def highlight_winning_stones(self):
        """승리한 돌들을 강조 표시합니다."""
        if not self.game or not self.game.get_last_move():
            return
        
        last_move = self.game.get_last_move()
        if not last_move:
            return
        
        row, col = last_move
        stone_color = self.game.get_board().get_stone(row, col)
        if not stone_color:
            return
        
        # 승리한 5개의 돌 위치 찾기
        winning_positions = self.find_winning_positions(row, col, stone_color)
        
        # 승리한 돌들을 빨간색 테두리로 강조
        for win_row, win_col in winning_positions:
            x = (win_col + 1) * self.cell_size
            y = (win_row + 1) * self.cell_size
            
            # 빨간색 테두리 원 생성
            highlight = self.canvas.create_oval(
                x - self.stone_radius - 3, y - self.stone_radius - 3,
                x + self.stone_radius + 3, y + self.stone_radius + 3,
                outline="#ff0000", width=3, fill=""
            )
            
            # 승리 표시기 저장 (새 게임 시작 시 제거)
            if not hasattr(self, 'winning_highlights'):
                self.winning_highlights = []
            self.winning_highlights.append(highlight)
    
    def find_winning_positions(self, row: int, col: int, stone_color: StoneColor) -> List[Tuple[int, int]]:
        """승리한 5개의 돌 위치를 찾습니다."""
        directions = [
            (0, 1),   # 가로
            (1, 0),   # 세로
            (1, 1),   # 대각선 (우하향)
            (1, -1)   # 대각선 (좌하향)
        ]
        
        for dr, dc in directions:
            positions = self._get_stone_positions_in_direction(row, col, dr, dc, stone_color)
            if len(positions) >= 5:
                return positions[:5]  # 처음 5개만 반환
        
        return []
    
    def _get_stone_positions_in_direction(self, row: int, col: int, dr: int, dc: int, stone_color: StoneColor) -> List[Tuple[int, int]]:
        """특정 방향의 연속된 돌들의 위치를 반환합니다."""
        positions = [(row, col)]
        
        # 정방향 확인
        r, c = row + dr, col + dc
        while (0 <= r < self.board_size and 0 <= c < self.board_size and 
               self.game.get_board().get_stone(r, c) == stone_color):
            positions.append((r, c))
            r += dr
            c += dc
        
        # 역방향 확인
        r, c = row - dr, col - dc
        while (0 <= r < self.board_size and 0 <= c < self.board_size and 
               self.game.get_board().get_stone(r, c) == stone_color):
            positions.insert(0, (r, c))
            r -= dr
            c -= dc
        
        return positions
    
    def update_display(self):
        """화면 표시를 업데이트합니다."""
        if not self.game:
            return
        
        info = self.game.get_game_info()
        
        # 상태 표시 업데이트
        if info['game_state'] == GameState.PLAYING:
            status_text = f"현재 턴: {info['current_player']} ({info['current_stone']})"
        elif info['game_state'] == GameState.WIN:
            status_text = f"승리: {info['winner']}!"
        else:
            status_text = "무승부!"
        
        if self.status_label:
            self.status_label.config(text=status_text)
        
        # 점수 표시 업데이트
        score_text = f"점수 - {self.game.get_player1().get_name()}: {info['player1_score']} | {self.game.get_player2().get_name()}: {info['player2_score']}"
        if self.score_label:
            self.score_label.config(text=score_text)
    
    def handle_win(self, winner):
        """승리 처리"""
        winner_name = winner.get_name()
        
        # 마지막으로 놓은 돌을 그리기
        last_move = self.game.get_last_move()
        if last_move:
            row, col = last_move
            stone_color = self.game.get_board().get_stone(row, col)
            if stone_color:
                self.draw_stone(row, col, stone_color)
        
        # 승리한 돌들을 강조 표시
        self.highlight_winning_stones()
        
        # 승리 메시지 표시 (1초 후 자동으로 새 게임 시작)
        messagebox.showinfo("게임 종료", f"{winner_name}님이 승리했습니다!")
        
        # 1초 후 자동으로 새 게임 시작
        self.root.after(1000, self.new_game)
    
    def handle_draw(self):
        """무승부 처리"""
        # 무승부 메시지 표시 (1초 후 자동으로 새 게임 시작)
        messagebox.showinfo("게임 종료", "무승부입니다!")
        
        # 1초 후 자동으로 새 게임 시작
        self.root.after(1000, self.new_game)
    
    def new_game(self):
        """새 게임을 시작합니다."""
        # 기존 돌들 제거
        if self.canvas:
            # 격자선과 화점을 제외한 모든 요소 제거
            for item in self.canvas.find_all():
                if item != self.double_three_indicator:
                    self.canvas.delete(item)
            
            # 보드 다시 그리기
            self.draw_board()
        
        # 쌍삼 표시기 제거
        self.clear_double_three_indicator()
        
        # 승리 표시기 제거
        if hasattr(self, 'winning_highlights'):
            for highlight in self.winning_highlights:
                if highlight in self.canvas.find_all():
                    self.canvas.delete(highlight)
            self.winning_highlights = []
        
        # 게임 재시작
        self.game.reset_game()
        
        # 화면 업데이트
        self.update_display()
    
    def undo_move(self):
        """마지막 이동을 되돌립니다."""
        if not self.game or self.game.is_game_over():
            return
        
        # 무르기 실행
        if self.game.undo_move():
            # 화면에서 마지막 돌 제거
            if self.canvas:
                # 모든 돌 제거 후 다시 그리기
                for item in self.canvas.find_all():
                    if item != self.double_three_indicator:
                        self.canvas.delete(item)
                
                # 보드 다시 그리기
                self.draw_board()
                
                # 기존 돌들 다시 그리기
                board_state = self.game.get_board().get_board_state()
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        stone_color = board_state[row][col]
                        if stone_color:
                            self.draw_stone(row, col, stone_color)
            
            # 화면 업데이트
            self.update_display()
        else:
            # 무르기 실패 시 메시지
            messagebox.showinfo("무르기", "무를 수 있는 이동이 없습니다.")
    
    def run(self):
        """GUI를 실행합니다."""
        self.root.mainloop()


def main():
    """GUI 테스트용 메인 함수"""
    root = tk.Tk()
    app = TkinterGUI(root)
    app.run()


if __name__ == "__main__":
    main() 