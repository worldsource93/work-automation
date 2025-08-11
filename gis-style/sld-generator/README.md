# SLD Generator

GeoTIFF 래스터 파일에서 자동으로 SLD(Styled Layer Descriptor) 스타일 파일을 생성하는 도구입니다.

## 📋 기능

- 멀티밴드 GeoTIFF 파일 지원
- 강수량 및 온도 데이터 자동 감지
- QGIS 색상 램프를 활용한 시각화
- 분위수 및 등간격 분류 방법 지원
- 밴드별 개별 SLD 파일 생성

## 🔧 요구사항

### 시스템 요구사항
- Python 3.7+
- QGIS Python 바인딩

### Python 패키지
```bash
pip install rasterio numpy python-dotenv
```

### QGIS 설치 (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install qgis python3-qgis
```

## ⚙️ 설정

1. `.env.example` 파일을 `.env`로 복사:
```bash
cp .env.example .env
```

2. `.env` 파일 편집:
```env
TIF_DIR=./input_tif      # 입력 GeoTIFF 파일 디렉토리
OUTPUT_DIR=./output_sld   # 출력 SLD 파일 디렉토리
BASE_YEAR=2020           # 밴드 이름에 사용할 기준 연도
```

## 📂 디렉토리 구조

```
sld-generator/
├── generate_sld.py       # 메인 스크립트
├── .env                 # 환경 설정 (생성 필요)
├── .env.example         # 환경 설정 예제
├── input_tif/           # 입력 GeoTIFF 파일 위치
│   ├── prcp_2020_2030.tif
│   └── temp_2020_2030.tif
└── output_sld/          # 생성된 SLD 파일 위치
    ├── prcp_2020_2030_2020.sld
    ├── prcp_2020_2030_2021.sld
    └── ...
```

## 🚀 사용법

### 기본 실행
```bash
python generate_sld.py
```

### 실행 예제
```bash
# 환경 변수 설정
export TIF_DIR="./my_tiff_files"
export OUTPUT_DIR="./my_sld_output"
export BASE_YEAR=2020

# 스크립트 실행
python generate_sld.py
```

## 📊 데이터 유형별 처리

### 강수량 데이터 (prcp)
- **파일명 패턴**: `prcp`, `precipitation`, `rainfall` 포함
- **색상 램프**: YlGnBu (노랑-초록-파랑)
- **분류 방법**: 5분위수 (Quantile)
- **분류 개수**: 5개 구간

### 온도 데이터 (temp)
- **파일명 패턴**: `temp`, `temperature` 포함
- **색상 램프**: YlOrRd (노랑-주황-빨강)
- **분류 방법**: 등간격 (Equal Interval)
- **분류 개수**: 5개 구간
- **경고**: 한국 기준 온도 범위(-10°C ~ 40°C) 벗어날 시 경고 메시지