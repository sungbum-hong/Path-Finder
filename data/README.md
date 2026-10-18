# 데이터 받는 방법

원자료는 용량이 커서 Git에 올리지 않습니다. 아래 표대로 내려받아 `data/raw/`에 저장하세요.
받은 날짜와 데이터 기준 시점을 오른쪽 칸에 꼭 적어주세요. 재현과 기획서 출처 표기에 필요합니다.

| 번호 | 데이터 | 받는 곳 | 저장 폴더 | 기준 시점 / 받은 날 |
| --- | --- | --- | --- | --- |
| 1 | 가해운전자 연령층별 교통사고 (수도권 시군구, 최근 3년) | [TAAS](https://taas.koroad.or.kr) | `data/raw/accident/` | |
| 2 | 행정동별 연령별 주민등록 인구 (수도권) | [주민등록 인구통계](https://jumin.mois.go.kr) | `data/raw/population/` | |
| 3 | 수도권 생활이동 (연령별·출발-도착지, 내국인), 한 달 치 | [공공데이터포털](https://www.data.go.kr/data/15145614/fileData.do) | `data/raw/mobility_purpose/` | |
| 4 | 수도권 생활이동 수단 (선택) | [서울 열린데이터광장](https://data.seoul.go.kr/dataList/OA-22655/F/1/datasetView.do) | `data/raw/mobility_mode/` | |
| 5 | 전국 버스정류장 위치정보 | [공공데이터포털](https://www.data.go.kr/data/15067528/fileData.do) | `data/raw/bus_stop/` | |
| 6 | 버스노선정보 (배차간격) | [공공데이터포털 API](https://www.data.go.kr/data/15098529/openapi.do) | 노트북 02에서 API로 수집 | |
| 7 | 면허 반납 지원 조례 | [국가법령정보 공동활용 API](https://open.law.go.kr) | 노트북 04에서 API로 수집 | |
| 8 | 행정동 경계 | [SGIS](https://sgis.kostat.go.kr) | `data/raw/boundary/` | |

## 받을 때 확인할 것

- **3번 생활이동:** 같은 메뉴의 매뉴얼과 행정동 코드 정보를 먼저 읽고, 연령대 구분과 목적 코드를 확인하세요.
- **5번 정류장:** 국가대중교통정보센터(TAGO)와 연계된 지자체만 들어 있어 서울·경기 일부가 빠질 수 있습니다. 빠진 지역은 서울 열린데이터광장, 경기데이터드림의 정류장 데이터로 보완합니다.
- **행정동 코드:** 데이터마다 행정안전부 코드(10자리)와 통계청 코드(8자리)가 섞여 있을 수 있습니다. 팀 공통 코드표에 맞춰 변환하세요.
