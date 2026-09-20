# Structural Dynamics & Aeroelasticity

첫 화면 1개와 본문 20개로 구성된 블로그 HTML이다.

## 적용

ZIP의 structural-dynamics 폴더로 블로그의 기존 동명 폴더를 교체한다. 첫 화면은 structural-dynamics/index.html이다. 기존 글의 폴더 주소는 유지했다.

각 HTML에 스타일과 목차 스크립트가 포함되어 있으므로 별도 빌드가 필요하지 않다. 수식은 참고 HTML과 같은 MathJax 3 CDN을 사용하므로 표시할 때 인터넷 연결이 필요하다.

## 형식

참고로 제공한 「2.2 Conservation of Momentum」 HTML의 CSS와 MathJax 설정, 우측 목차 동작을 그대로 사용했다.

- 본문 17px, 줄간격 2, 본문 열 860px
- 동일한 글꼴 목록, 제목 크기, 여백, 화면 너비별 배치
- MathJax CHTML 배율 1.02
- 영어 제목과 소제목, 한국어 본문, 식 번호와 본문 참조
- 글마다 개념과 현상, 가정, 중간 유도, 물리적 의미를 설명

본문은 학부에서 석사 입문 수준으로 구성했다. 플러터 부분은 정적 공탄성, 대표 단면의 굽힘·비틀림, 복소 고유값에 의한 안정성 해석까지 다룬다.

## 구성

1. Fundamentals — 1.1–1.2
2. Free Vibration — 2.1–2.2
3. Forced Vibration — 3.1–3.3
4. Multi-Degree-of-Freedom Systems — 4.1–4.3
5. Continuous Systems and Beam Vibration — 5.1–5.4
6. Structural Analysis Methods — 6.1–6.3
7. Aeroelasticity and Flutter — 7.1–7.3

폴더 안의 HTML만으로 첫 화면과 모든 본문 사이를 이동할 수 있다.
