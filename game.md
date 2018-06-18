0. Introduction
	- Sudo Coding for Game Programming Project
	- It will be Implement with Python or Unreal Engine

1. Basic Concept
	- MMORPG로 제작. 하루에 일정 시간동안만 서비스하고(24시간 서비스할 경우 로그아웃하는 사이 뒤통수를 맞을 수 있음), 자유로운 PK를 장려.
	- 세력이 클 경우 한타 싸움에서는 강력하나, 식량 수급과 보급품 조달에 어려움이 생김.
	- 소수의 캐릭터를 강하게 키울 경우, 한타 싸움에서는 상대적으로 비효율적이지만, 적의 보급선 및 심장부를 타격하는 데 용이.
	- 따라서 유리한 상황을 계속 유지하고 굴리는 것이 쉽지만은 않음(자유로운 PK가 가능한 게임에서의 밸런스 조정)
	- 10명의 유저가 각각 통제하는 1의 세력의 연합이, 1명의 유저가 통제하는 10의 세력보다 강했으면 좋겠음(이를 어떻게 구현할지는 미지수)
	- 게임 기획 --> Sudo Coding --> 구현 순으로 제작 (앞 단계일수록 실수의 허용폭이 넓음)

2. Structure(구조물)
	- Command Center: 본진 건물, Farmer 및 Caravan 생산, 식량 저장 및 충전(유닛에게 식량 제공) 가능
	- Storage: 창고, 식량 저장 및 충전(유닛에게 식량 제공) 가능
	- Barrack: 병영, Warrior, Archor, Knight 생산 가능
	
3. Unit Overview
	- 기본 구성: level, exp, hp, food, damage, defense, position, rotation, speed
		- level: 유닛의 레벨. 레벨이 증가하면 hp, damage, defense, speed가 소폭 증가.
		- exp: 유닛의 경험치. maxexp 이상이 되면 level up
		- hp: 유닛의 체력. 0이 되면 캐릭터 사망. 사망한 캐릭터는 부활 불가.
		- food: 유닛의 식량. 0이 되면 캐릭터 능력치 대폭 하락,
		- damage: 유닛의 공격력. 추후에 공격 시스템을 다양화할 수도 있음
		- defense: 유닛의 방어력. 정면에만 적용되며, 적의 공격력을 감소.
		- position: 유닛의 위치.
		- rotation: 유닛의 방향. 2차원의 경우 스칼라로 표현, 3차원의 경우 요소가 3개인 벡터로 표현.
		- speed: 유닛의 속도
	- 유닛 종류
		- Farmer: 농부. 약한 전투능력, 건설 및 채집 가능.
		- Carrivan: 보급용 수레. 식량 적재 및 보급 가능
		- Warrior: 전사.
		- Author: 궁수. 원거리 공격 가능
		- Knight: 기사. 빠른 이동속도 및 강한 전투력. 많은 보급품 소모. 레벨업을 하기 위한 많은 경험치 필요.

4. 스킬
	- 일괄적으로 설정 -> 유닛 종류마다 설정 -> 유닛마다 바인딩
	- 기본 구성: move, stop, attack, patrol, hold
	- 추가 스킬. build, gather, magic(추후 마법 유닛 추가시)


5. 게임 흐름
	- (1) Initial Setting
		- 임의의 장소에 Farmer 4기, Caravan 1기(식량 20000), Warrior 4기, Archor 2기, Knight 1기 배정
	- (2) Main Game Loop
		- Drawmap: Map, MiniMap, Troops, Interface 그리기. 월드의 상태 정보를 반영
		- ReceiveInput: 사용자의 마우스, 키보드 입력을 받음
		- ProcessInput: 사용자에게서 받은 입력을 처리
			- MouseClick(MouseX, MouseY)
			- KeyBoard(Move, Stop, Attack, Patrol, Hold) + Optional(Build, Gather, etc)
			- KeyBoard(Command Center, Storage, Barrack)
			- KeyBoard(Farmer, Caravan)
			- KeyBoard(Footman, Archer, Knight)
		- UpdateCharacterCommand: 필요한 경우, 캐릭터가 수행하는 명령을 업데이트
		- ProcessCharacter: 캐릭터 이동, 공격 등의 행동 수행
