# 🍳 레시피 & 스핀오프 공유 플랫폼

## 📌 프로젝트 소개
나만의 레시피를 등록하고, 다른 사람의 레시피에서 영감을 받아 새로운 **스핀오프 레시피**를 생성할 수 있는 웹 애플리케이션입니다.  
**좋아요 기능**, **마이페이지**, **카테고리 분류**, **재료 JSON 처리** 등의 기능을 통해 사용자 중심의 경험을 제공합니다.

## 🛠️ 기술 스택

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Backend:** Python, Django 5.2.2
- **Database:** SQLite3 (기본)
- **기타:** Django ORM, REST Framework 예외 처리, Form 기반 입력 처리

## ⚙️ 주요 기능

### 1. 사용자 인증
- 로그인, 로그아웃 기능 (Django `login_required` 적용)
- 본인이 작성한 콘텐츠에만 수정/삭제 가능

### 2. 레시피 기능
- 레시피 등록, 수정, 삭제
- 카테고리 (음식/음료/디저트) 필터링
- 재료 입력: JSON 문자열 형태로 저장 (`form.contents` → JavaScript 처리)

### 3. 스핀오프 기능
- 특정 레시피에서 파생된 아이디어를 **스핀오프 레시피**로 등록
- 기존 레시피의 내용을 재활용하면서 창의적인 레시피 공유 가능

### 4. 좋아요 기능
- 레시피, 스핀오프에 좋아요 / 취소 (toggle 방식)
- 좋아요 상태는 ❤️ / 🤍 아이콘으로 시각화

### 5. 마이페이지
- 내가 등록한 레시피 / 스핀오프 확인
- 내가 좋아요한 콘텐츠 확인

## 🖥️ 시연 영상 안내

- 영상 경로: `video/` 디렉토리에 3분 이내 시연 영상 포함
- 오디오 포함 여부: **Yes**
- 시연 순서:  
  1. 로그인  
  2. 레시피 등록  
  3. 스핀오프 생성  
  4. 좋아요 누르기  
  5. 마이페이지 확인  

## 📁 프로젝트 구조 (일부)
```
recipe_app/
├── models.py            # Recipe, Spinoff, Like 모델 정의
├── views.py             # 뷰 함수 (서비스 분리 구조 반영)
├── services/
│   └── recipe_services.py   # 비즈니스 로직 분리
├── templates/
│   └── recipe_app/
│       ├── recipe_form.html
│       ├── spinoff_form.html
│       ├── my_page.html
│       └── ...
```

## ✅ 실행 방법

1. 가상환경 설정 및 라이브러리 설치
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. 마이그레이션 및 서버 실행
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

3. 접속 URL
```
http://127.0.0.1:8000/
```

---

## 💡 개발 포인트
- 비즈니스 로직을 `Service Layer`로 분리하여 유지보수성과 테스트 용이성 확보
- 모델에 `classmethod`, `custom manager` 등을 적극 활용
- HTML Form → JavaScript → JSON 변환 로직을 통해 사용자 입력의 유연한 처리

---

## 🙋 팀 또는 개발자 소개
> 개발자: 고다연  
> 과제명: AD_Project  
> 제출일: 2025.06.16
