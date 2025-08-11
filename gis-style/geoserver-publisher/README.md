# GeoServer Publisher

SLD(Styled Layer Descriptor) 파일을 GeoServer에 자동으로 업로드하는 도구입니다.

## 📋 기능

- 로컬 SLD 파일을 GeoServer에 일괄 업로드
- 기존 스타일 자동 업데이트
- 워크스페이스별 스타일 관리
- 업로드 상태 실시간 모니터링
- 환경 변수 기반 안전한 인증

## 🔧 요구사항

### 시스템 요구사항
- Python 3.7+
- GeoServer 2.x 이상
- 네트워크 연결

### Python 패키지
```bash
pip install requests python-dotenv
```

## ⚙️ 설정

1. `.env.example` 파일을 `.env`로 복사:
```bash
cp .env.example .env
```

2. `.env` 파일 편집:
```env
GEOSERVER_URL=http://localhost:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=your_password_here
GEOSERVER_WORKSPACE=your_workspace
SLD_FOLDER=./sld_files
```

### 환경 변수 설명

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `GEOSERVER_URL` | GeoServer 기본 URL | http://localhost:8080/geoserver |
| `GEOSERVER_USER` | GeoServer 관리자 사용자명 | 필수 |
| `GEOSERVER_PASSWORD` | GeoServer 관리자 비밀번호 | 필수 |
| `GEOSERVER_WORKSPACE` | 대상 워크스페이스 | default |
| `SLD_FOLDER` | SLD 파일이 있는 로컬 폴더 | ./sld_files |

## 📂 디렉토리 구조

```
geoserver-publisher/
├── publish_style.py     # 메인 스크립트
├── .env                # 환경 설정 (생성 필요)
├── .env.example        # 환경 설정 예제
└── sld_files/          # SLD 파일 폴더
    ├── style1.sld
    ├── style2.sld
    └── ...
```

## 🚀 사용법

### 기본 실행
```bash
python publish_style.py
```

### 실행 예제
```bash
# 환경 변수 직접 설정
export GEOSERVER_URL="http://192.168.1.100:8080/geoserver"
export GEOSERVER_USER="admin"
export GEOSERVER_PASSWORD="geoserver"
export GEOSERVER_WORKSPACE="climate_data"
export SLD_FOLDER="../sld-generator/output_sld"

# 스크립트 실행
python publish_style.py
```

## 🔄 업로드 프로세스

1. **환경 설정 검증**: 필수 환경 변수 확인
2. **SLD 파일 스캔**: 지정된 폴더에서 `.sld` 파일 검색
3. **스타일 존재 확인**: GeoServer에 동일 이름 스타일 확인
4. **업로드/업데이트**:
   - 신규: POST 요청으로 생성
   - 기존: PUT 요청으로 업데이트
5. **결과 보고**: 성공/실패 통계 출력

## 📊 출력 예시

```
✅ 설정 검증 완료!
🚀 SLD 파일 업로드 시작...

📤 처리 중: prcp_2020_2030_2020.sld
   ✅ 새로운 스타일 업로드 성공: prcp_2020_2030_2020

📤 처리 중: temp_2020_2030_2020.sld
   🔄 기존 스타일 덮어쓰기 성공: temp_2020_2030_2020

✨ 업로드 완료! 성공: 2/2
```

## 📚 GeoServer REST API

이 도구는 다음 GeoServer REST 엔드포인트를 사용합니다:

- `GET /rest/workspaces/{workspace}/styles/{style}.sld` - 스타일 존재 확인
- `POST /rest/workspaces/{workspace}/styles` - 새 스타일 생성
- `PUT /rest/workspaces/{workspace}/styles/{style}` - 기존 스타일 업데이트
