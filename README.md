# 오목 게임 (Omok Game)

파이썬으로 만든 2인용 로컬 오목 게임입니다. GUI 환경에서 즐길 수 있는 클래식한 오목 게임으로, 파이썬 초급자도 이해할 수 있도록 설계되었습니다.

## 🎮 게임 특징

- **2인용 로컬 플레이어**: 같은 컴퓨터에서 번갈아가며 플레이
- **직관적인 GUI**: 마우스 클릭으로 쉽게 돌을 놓을 수 있음
- **실시간 승리 판정**: 5목이 완성되면 즉시 게임 종료
- **쌍삼 방지 기능**: 쌍삼(두 개의 열린 삼)이 되는 위치에는 돌을 놓을 수 없으며, 빨간색 반투명 표시로 경고
- **게임 상태 표시**: 현재 플레이어와 게임 진행 상황을 실시간으로 표시
- **플레이어 닉네임**: 게임 시작 전 플레이어 닉네임을 입력할 수 있음
- **재시작 기능**: 언제든지 새로운 게임을 시작할 수 있으며, 닉네임도 변경 가능

## 🛠️ 기술 스택

- **Python 3.9+**
- **tkinter**: GUI 프레임워크 (파이썬 기본 라이브러리)
- **Pillow**: 이미지 처리 (돌 이미지용)

## 📦 설치 방법

1. 저장소를 클론합니다:
```bash
git clone https://github.com/dongkoony/omok.git
cd omok
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

3. 게임을 실행합니다:
```bash
python main_2d.py
```

## 🎯 게임 규칙

1. **게임판**: 15x15 크기의 바둑판
2. **돌**: 흑돌(검은색)과 백돌(흰색)을 번갈아가며 배치
3. **승리 조건**: 가로, 세로, 대각선 중 하나의 방향으로 5개의 돌을 연속으로 놓으면 승리
4. **쌍삼 금지**: 쌍삼(두 개의 열린 삼을 동시에 만드는 수)이 되는 위치에는 돌을 놓을 수 없음
5. **순서**: 흑돌이 먼저 시작

## 🏗️ 프로젝트 아키텍처

### 전체 시스템 아키텍처

```mermaid
graph TD
    A[main_2d.py] --> B[game.py]
    A --> C[tkinter_gui.py]
    B --> D[board.py]
    B --> E[player.py]
    C --> B
    
    subgraph "게임 로직"
        B[Game 클래스 game.py]
        D[Board 클래스 board.py]
        E[Player 클래스 player.py]
    end
    
    subgraph "사용자 인터페이스 | GUI 클래스"
        C[tkinter_gui]
    end
    
    subgraph "실행"
        A[main_2d.py]
    end
```

### 이벤트 처리 아키텍처

```mermaid
sequenceDiagram
    participant User as 사용자
    participant GUI as TkinterGUI
    participant Game as Game
    participant Board as Board
    participant OS as 운영체제

    User->>GUI: 마우스 클릭
    GUI->>OS: 이벤트 등록
    
    Note over OS: 윈도우: 즉시 처리<br/>맥: 지연 처리
    
    OS->>GUI: 클릭 이벤트 전달
    GUI->>Game: make_move() 호출
    Game->>Board: place_stone() 호출
    Board->>Board: check_win() 호출
    
    alt 승리 조건 만족
        Board->>Game: 승리 반환
        Game->>GUI: handle_win() 콜백
        GUI->>GUI: 승리 메시지 표시
        GUI->>GUI: 새 게임 시작
    else 승리 조건 불만족
        Board->>Game: 계속 진행
        Game->>GUI: 상태 업데이트
        GUI->>GUI: 돌 그리기 (지연 처리)
    end
```

### 크로스 플랫폼 이벤트 처리 비교

```mermaid
graph LR
    subgraph "윈도우 이벤트 처리"
        W1[마우스 클릭] --> W2[즉시 이벤트 처리]
        W2 --> W3[돌 배치]
        W3 --> W4[승리 조건 체크]
        W4 --> W5[돌 그리기]
    end
    
    subgraph "맥 이벤트 처리 수정 전"
        M1[마우스 클릭] --> M2[지연 이벤트 처리]
        M2 --> M3[돌 배치]
        M3 --> M4[승리 조건 체크]
        M4 --> M5[승리 메시지 4개 돌]
        M5 --> M6[돌 그리기 안됨]
    end
    
    subgraph "맥 이벤트 처리 수정 후"
        M1_FIX[마우스 클릭] --> M2_FIX[지연 이벤트 처리]
        M2_FIX --> M3_FIX[돌 배치]
        M3_FIX --> M4_FIX[승리 조건 체크]
        M4_FIX --> M5_FIX[승리 메시지 5개 돌]
        M5_FIX --> M6_FIX[돌 그리기 after 10ms]
    end
```

## 📁 파일 구조

```
omok/
├── main_2d.py           # 게임 실행 파일
├── game.py              # 게임 로직 관리
├── board.py             # 오목판 클래스
├── player.py            # 플레이어 클래스
├── tkinter_gui.py       # GUI 인터페이스
├── nickname_dialog.py   # 닉네임 입력 다이얼로그
├── assets/              # 이미지 파일들
│   ├── black_stone.png
│   ├── white_stone.png
│   └── board.png
├── requirements.txt     # 의존성 파일
└── README.md            # 프로젝트 설명서
```

## 🎮 사용법

1. 게임을 실행하면 플레이어 닉네임 입력 창이 나타납니다
2. 각 플레이어의 닉네임을 입력하거나 빈칸으로 두어 기본 닉네임을 사용합니다
3. 15x15 오목판이 나타나면 흑돌 플레이어부터 시작하여 번갈아가며 돌을 놓습니다
4. 마우스로 원하는 위치를 클릭하여 돌을 배치합니다
5. 쌍삼이 되는 위치에는 빨간색 반투명 표시가 나타나며 돌을 놓을 수 없습니다
6. 5목이 완성되면 승리 메시지가 표시됩니다
7. "새 게임" 버튼을 클릭하여 새로운 게임을 시작할 수 있으며, 닉네임도 변경할 수 있습니다

## 🔧 주요 클래스 설명

### Game 클래스
- 게임의 전체적인 상태를 관리
- 플레이어 턴 관리, 승리 판정, 게임 재시작 기능

### Board 클래스
- 15x15 오목판의 상태를 관리
- 돌 배치, 승리 조건 확인, 보드 초기화 기능

### Player 클래스
- 플레이어 정보 관리 (이름, 돌 색상)
- 플레이어 턴 관리

### TkinterGUI 클래스
- tkinter를 사용한 사용자 인터페이스
- 마우스 이벤트 처리, 게임 상태 표시
- 무르기 기능, 쌍삼 방지 기능

### NicknameDialog 클래스
- 플레이어 닉네임 입력을 위한 다이얼로그
- 모달 창으로 닉네임 입력 처리

## 🔧 크로스 플랫폼 호환성

### 문제 상황
이 프로젝트는 윈도우와 맥에서 서로 다른 동작을 보였습니다:

- **윈도우**: 5개의 돌을 놓고 승리 조건이 만족되면 정상적으로 승리 메시지 표시
- **맥**: 4개의 돌을 놓은 상태에서 5번째 돌을 놓을 때 승리 메시지가 표시되어 5번째 돌이 화면에 그려지지 않음

### 원인 분석
이 문제는 운영체제별 tkinter 이벤트 처리 방식의 차이 때문입니다:

1. **윈도우**: 이벤트를 즉시 처리하여 동기적으로 실행
2. **맥**: 이벤트를 지연 처리하여 비동기적으로 실행

### 해결 방법
`tkinter_gui.py`의 `on_canvas_click` 메서드에서 돌을 그리는 타이밍을 조정했습니다:

```python
# 수정 전 (윈도우에서만 정상 동작)
if self.game.get_game_state() == GameState.PLAYING:
    self.draw_stone(row, col, current_stone_color)

# 수정 후 (맥/윈도우 모두 정상 동작)
if self.game.get_game_state() == GameState.PLAYING:
    # 맥/윈도우 차이를 해결하기 위해 약간의 지연 후 돌을 그림
    self.root.after(10, lambda: self.draw_stone(row, col, current_stone_color))
```

### 수정된 코드 구조

```python
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
                # 맥/윈도우 차이를 해결하기 위해 약간의 지연 후 돌을 그림
                self.root.after(10, lambda: self.draw_stone(row, col, current_stone_color))
            # 승리한 경우에는 handle_win에서 돌을 그리므로 여기서는 그리지 않음
        else:
            # 잘못된 이동 표시
            self.show_invalid_move_indicator(row, col)
```

### 기술적 세부사항

1. **`root.after(10, callback)`**: 10밀리초 후에 콜백 함수를 실행
2. **람다 함수**: 클로저를 사용하여 현재 상태를 보존
3. **이벤트 큐**: tkinter의 이벤트 큐에 지연된 작업을 등록하여 동기화

이 수정으로 윈도우와 맥 모두에서 일관된 동작을 보장할 수 있습니다.

## 🚀 학습 포인트

이 프로젝트를 통해 학습할 수 있는 내용:

1. **클래스 설계**: 객체지향 프로그래밍의 기본 개념
2. **GUI 프로그래밍**: tkinter를 사용한 사용자 인터페이스 구현
3. **이벤트 처리**: 마우스 클릭 이벤트 처리
4. **게임 로직**: 승리 조건 판정 알고리즘
5. **모듈화**: 코드를 여러 파일로 나누어 관리
6. **상태 관리**: 게임 상태의 변화를 추적하고 관리
7. **콜백 시스템**: 이벤트 기반 프로그래밍
8. **무르기 기능**: 게임 상태 되돌리기 구현
9. **쌍삼 방지**: 오목 규칙 구현
10. **사용자 경험**: 직관적인 UI/UX 설계
11. **크로스 플랫폼 호환성**: 운영체제별 이벤트 처리 차이 해결
12. **비동기 프로그래밍**: 지연된 작업 처리

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든지 환영합니다!

## 📋 변경 이력

### v1.0.0 (2025-07-28) - 초기 릴리즈
**주요 기능**
- 기본 오목 게임 기능 구현
- GUI 인터페이스 구현 (tkinter)
- 쌍삼 방지 기능
- 무르기 기능
- 플레이어 닉네임 입력 시스템

### v1.1.0 (2025-07-30) - 크로스 플랫폼 호환성 개선
**버그 수정**
- 윈도우와 맥 간의 이벤트 처리 순서 차이 해결
- 5번째 돌을 놓을 때 승리 메시지가 정확히 표시되도록 수정

**기술적 개선**
- `root.after()` 메서드를 사용한 지연된 돌 그리기 구현
- 이벤트 처리 최적화로 모든 플랫폼에서 일관된 동작 보장

**사용자 경험**
- 모든 플랫폼에서 일관된 게임 플레이 경험 제공
- 승리 조건 만족 시 시각적 피드백 개선

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 