# GIS Style 자동화 시스템

GeoTIFF 파일에서 SLD(Styled Layer Descriptor) 스타일을 자동으로 생성하고 GeoServer에 배포하는 자동화 시스템입니다.

## 📋 개요

이 프로젝트는 두 가지 주요 컴포넌트로 구성되어 있습니다:

1. **SLD Generator** - GeoTIFF 래스터 파일에서 자동으로 SLD 스타일 파일 생성
2. **GeoServer Publisher** - 생성된 SLD 파일을 GeoServer에 자동 배포

## 🏗 프로젝트 구조

```
gis-style/
├── sld-generator/         # SLD 파일 생성 모듈
│   ├── generate_sld.py    # 메인 생성 스크립트
│   ├── .env.example       # 환경 변수 예제
│   └── README.md          # 모듈 문서
├── geoserver-publisher/   # GeoServer 배포 모듈
│   ├── publish_style.py   # 메인 배포 스크립트
│   ├── .env.example       # 환경 변수 예제
│   └── README.md          # 모듈 문서
└── README.md             # 이 문서
```

## 🚀 빠른 시작

### 1. SLD 파일 생성
```bash
cd sld-generator
cp .env.example .env
# .env 파일 편집 후
python generate_sld.py
```

### 2. GeoServer에 배포
```bash
cd ../geoserver-publisher
cp .env.example .env
# .env 파일 편집 후
python publish_style.py
```

## 📊 지원하는 데이터 유형

- **강수량 데이터 (prcp)**: YlGnBu 색상 램프 사용, 분위수 기반 분류
- **온도 데이터 (temp)**: YlOrRd 색상 램프 사용, 등간격 분류

## 🔄 워크플로우

1. GeoTIFF 파일을 `sld-generator/input_tif/` 폴더에 배치
2. `generate_sld.py` 실행하여 SLD 파일 생성
3. 생성된 SLD 파일을 검토
4. `publish_style.py` 실행하여 GeoServer에 배포

## 📝 라이선스

이 프로젝트는 내부 사용을 위해 개발되었습니다.