"""
플레이어 클래스
오목 게임의 플레이어 정보를 관리합니다.
"""

from enum import Enum


class StoneColor(Enum):
    """돌 색상을 정의하는 열거형"""
    BLACK = "black"
    WHITE = "white"


class Player:
    """오목 게임의 플레이어를 나타내는 클래스"""
    
    def __init__(self, name: str, stone_color: StoneColor):
        """
        플레이어 초기화
        
        Args:
            name (str): 플레이어 이름
            stone_color (StoneColor): 플레이어의 돌 색상
        """
        self.name = name
        self.stone_color = stone_color
        self.score = 0
    
    def get_stone_color(self) -> StoneColor:
        """플레이어의 돌 색상을 반환합니다."""
        return self.stone_color
    
    def get_name(self) -> str:
        """플레이어 이름을 반환합니다."""
        return self.name
    
    def add_score(self, points: int = 1):
        """플레이어 점수를 증가시킵니다."""
        self.score += points
    
    def get_score(self) -> int:
        """플레이어 점수를 반환합니다."""
        return self.score
    
    def __str__(self) -> str:
        """플레이어 정보를 문자열로 반환합니다."""
        return f"{self.name} ({self.stone_color.value}) - 점수: {self.score}"
    
    def __repr__(self) -> str:
        """플레이어 객체의 표현을 반환합니다."""
        return f"Player(name='{self.name}', stone_color={self.stone_color})" 