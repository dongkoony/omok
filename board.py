"""
오목판 클래스
오목 게임의 보드 상태를 관리하고 승리 조건을 확인합니다.
"""

from typing import Optional, Tuple, List
from player import StoneColor


class Board:
    """오목 게임의 보드를 나타내는 클래스"""
    
    def __init__(self, size: int = 15):
        """
        보드 초기화
        
        Args:
            size (int): 보드 크기 (기본값: 15x15)
        """
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.last_move = None
        self.move_history = []  # 무르기를 위한 이동 기록
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """
        위치가 유효한지 확인합니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            
        Returns:
            bool: 유효한 위치인지 여부
        """
        return 0 <= row < self.size and 0 <= col < self.size
    
    def is_empty(self, row: int, col: int) -> bool:
        """
        해당 위치가 비어있는지 확인합니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            
        Returns:
            bool: 비어있는지 여부
        """
        if not self.is_valid_position(row, col):
            return False
        return self.board[row][col] is None
    
    def place_stone(self, row: int, col: int, stone_color: StoneColor) -> bool:
        """
        돌을 배치합니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            stone_color (StoneColor): 돌 색상
            
        Returns:
            bool: 배치 성공 여부
        """
        if not self.is_empty(row, col):
            return False
        
        self.board[row][col] = stone_color
        self.last_move = (row, col)
        self.move_history.append((row, col, stone_color))  # 이동 기록 추가
        return True
    
    def get_stone(self, row: int, col: int) -> Optional[StoneColor]:
        """
        해당 위치의 돌을 반환합니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            
        Returns:
            Optional[StoneColor]: 돌 색상 또는 None
        """
        if not self.is_valid_position(row, col):
            return None
        return self.board[row][col]
    
    def get_last_move(self) -> Optional[Tuple[int, int]]:
        """마지막으로 놓은 돌의 위치를 반환합니다."""
        return self.last_move
    
    def check_win(self, row: int, col: int, stone_color: StoneColor) -> bool:
        """
        승리 조건을 확인합니다.
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            stone_color (StoneColor): 확인할 돌 색상
            
        Returns:
            bool: 승리 여부
        """
        directions = [
            (0, 1),   # 가로
            (1, 0),   # 세로
            (1, 1),   # 대각선 (우하향)
            (1, -1)   # 대각선 (좌하향)
        ]
        
        for dr, dc in directions:
            if self._check_direction(row, col, dr, dc, stone_color):
                return True
        return False
    
    def _check_direction(self, row: int, col: int, dr: int, dc: int, stone_color: StoneColor) -> bool:
        """
        특정 방향으로 5목이 완성되었는지 확인합니다.
        
        Args:
            row (int): 시작 행 인덱스
            col (int): 시작 열 인덱스
            dr (int): 행 방향
            dc (int): 열 방향
            stone_color (StoneColor): 확인할 돌 색상
            
        Returns:
            bool: 5목 완성 여부
        """
        count = 1  # 현재 위치 포함
        
        # 정방향 확인
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.board[r][c] == stone_color:
            count += 1
            r += dr
            c += dc
        
        # 역방향 확인
        r, c = row - dr, col - dc
        while self.is_valid_position(r, c) and self.board[r][c] == stone_color:
            count += 1
            r -= dr
            c -= dc
        
        return count >= 5
    
    def is_full(self) -> bool:
        """
        보드가 가득 찼는지 확인합니다.
        
        Returns:
            bool: 보드가 가득 찬 여부
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is None:
                    return False
        return True
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """
        가능한 모든 이동을 반환합니다.
        
        Returns:
            List[Tuple[int, int]]: 가능한 이동 목록
        """
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_empty(row, col):
                    moves.append((row, col))
        return moves
    
    def check_double_three(self, row: int, col: int, stone_color: StoneColor) -> bool:
        """
        해당 위치에 돌을 놓으면 쌍삼이 되는지 확인합니다.
        쌍삼: 두 개의 열린 삼을 동시에 만드는 수
        
        Args:
            row (int): 행 인덱스
            col (int): 열 인덱스
            stone_color (StoneColor): 확인할 돌 색상
            
        Returns:
            bool: 쌍삼 여부
        """
        # 임시로 돌을 놓아서 확인
        if not self.is_empty(row, col):
            return False
        
        self.board[row][col] = stone_color
        
        # 열린 삼 개수 확인
        three_count = 0
        directions = [
            (0, 1),   # 가로
            (1, 0),   # 세로
            (1, 1),   # 대각선 (우하향)
            (1, -1)   # 대각선 (좌하향)
        ]
        
        for dr, dc in directions:
            if self._check_three(row, col, dr, dc, stone_color):
                three_count += 1
                if three_count >= 2:  # 쌍삼 이상
                    # 돌 제거
                    self.board[row][col] = None
                    return True
        
        # 돌 제거
        self.board[row][col] = None
        return False
    
    def _check_three(self, row: int, col: int, dr: int, dc: int, stone_color: StoneColor) -> bool:
        """
        특정 방향으로 열린 삼이 되는지 확인합니다.
        열린 삼: 양쪽 끝이 모두 열려있는 3개의 연속된 돌
        
        Args:
            row (int): 시작 행 인덱스
            col (int): 시작 열 인덱스
            dr (int): 행 방향
            dc (int): 열 방향
            stone_color (StoneColor): 확인할 돌 색상
            
        Returns:
            bool: 열린 삼 여부
        """
        # 현재 위치를 제외한 양쪽의 돌 개수 확인
        count_forward = 0
        count_backward = 0
        
        # 정방향 확인
        r, c = row + dr, col + dc
        while self.is_valid_position(r, c) and self.board[r][c] == stone_color:
            count_forward += 1
            r += dr
            c += dc
        
        # 역방향 확인
        r, c = row - dr, col - dc
        while self.is_valid_position(r, c) and self.board[r][c] == stone_color:
            count_backward += 1
            r -= dr
            c -= dc
        
        # 열린 삼 조건: 양쪽에 각각 1개씩 돌이 있고, 양쪽 끝이 모두 열려있어야 함
        total_count = count_forward + count_backward
        if total_count == 2:  # 양쪽에 1개씩 (총 3개)
            # 양쪽 끝에 빈 공간이 있는지 확인 (열린 삼)
            forward_empty = self.is_valid_position(row + (count_forward + 1) * dr, 
                                                 col + (count_forward + 1) * dc) and \
                           self.is_empty(row + (count_forward + 1) * dr, 
                                       col + (count_forward + 1) * dc)
            backward_empty = self.is_valid_position(row - (count_backward + 1) * dr, 
                                                  col - (count_backward + 1) * dc) and \
                            self.is_empty(row - (count_backward + 1) * dr, 
                                        col - (count_backward + 1) * dc)
            
            return forward_empty and backward_empty
        
        return False
    
    def reset(self):
        """보드를 초기화합니다."""
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None
        self.move_history = []
    
    def undo_last_move(self) -> Optional[Tuple[int, int, StoneColor]]:
        """
        마지막 이동을 되돌립니다.
        
        Returns:
            Optional[Tuple[int, int, StoneColor]]: 되돌린 이동 정보 (행, 열, 돌색상) 또는 None
        """
        if not self.move_history:
            return None
        
        last_move_info = self.move_history.pop()
        row, col, stone_color = last_move_info
        self.board[row][col] = None
        
        # last_move 업데이트
        if self.move_history:
            self.last_move = (self.move_history[-1][0], self.move_history[-1][1])
        else:
            self.last_move = None
        
        return last_move_info
        self.move_history = []  # 무르기를 위한 이동 기록
    
    def get_board_state(self) -> List[List[Optional[StoneColor]]]:
        """현재 보드 상태를 반환합니다."""
        return [row[:] for row in self.board]
    
    def __str__(self) -> str:
        """보드 상태를 문자열로 반환합니다."""
        result = []
        for row in self.board:
            row_str = []
            for cell in row:
                if cell is None:
                    row_str.append(".")
                elif cell == StoneColor.BLACK:
                    row_str.append("●")
                else:
                    row_str.append("○")
            result.append(" ".join(row_str))
        return "\n".join(result) 