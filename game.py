"""
게임 클래스
오목 게임의 전체적인 상태를 관리하고 게임 로직을 처리합니다.
"""

from typing import Optional, Callable, Tuple
from player import Player, StoneColor
from board import Board


class GameState:
    """게임 상태를 정의하는 열거형"""
    PLAYING = "playing"
    WIN = "win"
    DRAW = "draw"


class Game:
    """오목 게임의 메인 클래스"""
    
    def __init__(self, player1_name: str = "플레이어 1", player2_name: str = "플레이어 2"):
        """
        게임 초기화
        
        Args:
            player1_name (str): 첫 번째 플레이어 이름 (흑돌)
            player2_name (str): 두 번째 플레이어 이름 (백돌)
        """
        self.board = Board()
        self.player1 = Player(player1_name, StoneColor.BLACK)
        self.player2 = Player(player2_name, StoneColor.WHITE)
        self.current_player = self.player1
        self.game_state = GameState.PLAYING
        self.winner = None
        self.move_count = 0
        
        # 콜백 함수들
        self.on_state_change: Optional[Callable] = None
        self.on_win: Optional[Callable] = None
        self.on_draw: Optional[Callable] = None
    
    def get_current_player(self) -> Player:
        """현재 플레이어를 반환합니다."""
        return self.current_player
    
    def get_other_player(self) -> Player:
        """다른 플레이어를 반환합니다."""
        return self.player2 if self.current_player == self.player1 else self.player1
    
    def get_game_state(self) -> str:
        """현재 게임 상태를 반환합니다."""
        return self.game_state
    
    def get_winner(self) -> Optional[Player]:
        """승자를 반환합니다."""
        return self.winner
    
    def get_move_count(self) -> int:
        """총 이동 횟수를 반환합니다."""
        return self.move_count
    
    def make_move(self, row: int, col: int) -> bool:
        """
        돌을 놓습니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            
        Returns:
            bool: 이동 성공 여부
        """
        # 게임이 이미 종료되었거나 유효하지 않은 위치인 경우
        if self.game_state != GameState.PLAYING or not self.board.is_valid_position(row, col):
            return False
        
        # 돌을 놓을 수 없는 위치인 경우
        if not self.board.is_empty(row, col):
            return False
        
        # 쌍삼 방지 확인
        stone_color = self.current_player.get_stone_color()
        if self.board.check_double_three(row, col, stone_color):
            return False  # 쌍삼이므로 돌을 놓을 수 없음
        
        # 돌을 놓습니다
        if not self.board.place_stone(row, col, stone_color):
            return False
        
        self.move_count += 1
        
        # 승리 조건 확인 (5번째 돌을 두고 오목이 완성되었는지)
        if self.board.check_win(row, col, stone_color):
            # 승리 처리 (GUI에서 팝업 표시)
            self._handle_win()
            return True
        
        # 무승부 확인
        if self.board.is_full():
            # 무승부 처리 (GUI에서 팝업 표시)
            self._handle_draw()
            return True
        
        # 다음 플레이어로 턴 변경
        self._switch_player()
        
        # 상태 변경 콜백 호출
        if self.on_state_change:
            self.on_state_change()
        
        return True
    
    def _handle_win(self):
        """승리 처리"""
        self.game_state = GameState.WIN
        self.winner = self.current_player
        self.winner.add_score()
        
        if self.on_win:
            self.on_win(self.winner)
    
    def _handle_draw(self):
        """무승부 처리"""
        self.game_state = GameState.DRAW
        
        if self.on_draw:
            self.on_draw()
    
    def _switch_player(self):
        """플레이어 턴을 변경합니다."""
        self.current_player = self.get_other_player()
    
    def reset_game(self):
        """게임을 초기화합니다."""
        self.board.reset()
        self.current_player = self.player1
        self.game_state = GameState.PLAYING
        self.winner = None
        self.move_count = 0
        
        if self.on_state_change:
            self.on_state_change()
    
    def undo_move(self) -> bool:
        """
        마지막 이동을 되돌립니다.
        
        Returns:
            bool: 무르기 성공 여부
        """
        if self.game_state != GameState.PLAYING:
            return False
        
        # 마지막 이동 되돌리기
        last_move = self.board.undo_last_move()
        if last_move is None:
            return False
        
        # 플레이어 턴 되돌리기
        self._switch_player()
        
        # 상태 변경 알림
        if self.on_state_change:
            self.on_state_change()
        
        return True
    
    def get_board(self) -> Board:
        """게임 보드를 반환합니다."""
        return self.board
    
    def get_last_move(self) -> Optional[Tuple[int, int]]:
        """마지막 이동을 반환합니다."""
        return self.board.get_last_move()
    
    def get_player1(self) -> Player:
        """첫 번째 플레이어를 반환합니다."""
        return self.player1
    
    def get_player2(self) -> Player:
        """두 번째 플레이어를 반환합니다."""
        return self.player2
    
    def is_game_over(self) -> bool:
        """게임이 종료되었는지 확인합니다."""
        return self.game_state in [GameState.WIN, GameState.DRAW]
    
    def get_game_info(self) -> dict:
        """게임 정보를 딕셔너리로 반환합니다."""
        return {
            "current_player": self.current_player.get_name(),
            "current_stone": self.current_player.get_stone_color().value,
            "game_state": self.game_state,
            "move_count": self.move_count,
            "player1_score": self.player1.get_score(),
            "player2_score": self.player2.get_score(),
            "winner": self.winner.get_name() if self.winner else None
        }
    
    def set_callbacks(self, on_state_change: Callable = None, 
                        on_win: Callable = None, on_draw: Callable = None):
        """
        콜백 함수들을 설정합니다.
        
        Args:
            on_state_change: 게임 상태가 변경될 때 호출되는 함수
            on_win: 승리했을 때 호출되는 함수
            on_draw: 무승부일 때 호출되는 함수
        """
        self.on_state_change = on_state_change
        self.on_win = on_win
        self.on_draw = on_draw
    
    def __str__(self) -> str:
        """게임 상태를 문자열로 반환합니다."""
        info = self.get_game_info()
        return (f"게임 상태: {info['game_state']}\n"
                f"현재 플레이어: {info['current_player']} ({info['current_stone']})\n"
                f"이동 횟수: {info['move_count']}\n"
                f"점수 - {self.player1.get_name()}: {info['player1_score']}, "
                f"{self.player2.get_name()}: {info['player2_score']}") 