import os
import requests
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 🛠 GeoServer 접속 정보
GEOSERVER_URL = os.getenv("GEOSERVER_URL", "http://localhost:8080/geoserver")
GEOSERVER_USER = os.getenv("GEOSERVER_USER")
GEOSERVER_PASSWORD = os.getenv("GEOSERVER_PASSWORD")
WORKSPACE = os.getenv("GEOSERVER_WORKSPACE", "default")

# 📁 SLD 파일이 저장된 로컬 폴더 경로
SLD_FOLDER = os.getenv("SLD_FOLDER", "./sld_files")

# 🔧 헤더 설정
headers = {
    "Content-Type": "application/vnd.ogc.sld+xml"
}

def upload_sld_to_geoserver(style_name, sld_file_path):
    with open(sld_file_path, "rb") as file:
        sld_data = file.read()

    # 업로드 URL 구성
    style_check_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/styles/{style_name}.sld"
    upload_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/styles"
    params = {"name": style_name}

    # 스타일 존재 여부 확인
    try:
      check_response = requests.get(
        style_check_url, 
        auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
        timeout=60
      )
    except request.RequestException as e:
        print(f"❌ GeoServer 연결 실패: {e}")
        return False

    if check_response.status_code == 200:
        print(f"🔁 {style_name} 스타일이 이미 존재함. 덮어쓰기 중...")
        # PUT: 기존 스타일 덮어쓰기
        put_url = f"{upload_url}/{style_name}"
        response = requests.put
            put_url, headers=headers, data=sld_data,
            auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
            timeout=60
        )
    else:
        print(f"➕ {style_name} 스타일 새로 업로드 중...")
        # POST: 새로운 스타일 생성
        response = requests.post(
            upload_url, headers=headers, params=params, data=sld_data,
            auth=(GEOSERVER_USER, GEOSERVER_PASSWORD),
            timeout=60
        )

    # 결과 확인
    if response.status_code in [200, 201]:
        print(f"✅ 스타일 업로드 성공: {style_name}")
        return True
    else:
        error_msg = response.text[:200] if response.text else "No error message"
        print(f"❌ 업로드 실패: {style_name} (코드 {response.status_code}) - {error_msg}")
        return False

def validate_config():
    """필수 설정 검증"""
    if not all([GEOSERVER_URL, GEOSERVER_USER, GEOSERVER_PASSWORD, WORKSPACE]):
        print("❌ GeoServer 접속 정보가 설정되지 않았습니다.")
        print("환경 변수를 확인하세요: GEOSERVER_URL, GEOSERVER_USER, GEOSERVER_PASSWORD, GEOSERVER_WORKSPACE")
        return False
    
    if not os.path.exists(SLD_FOLDER):
        print(f"❌ SLD 폴더를 찾을 수 없습니다: {SLD_FOLDER}")
        return False
    
    return True

def main():
    """메인 실행 함수"""
    if not validate_config():
        return
    
    sld_files = [f for f in os.listdir(SLD_FOLDER) if f.endswith(".sld")]
    
    if not sld_files:
        print(f"⚠️ {SLD_FOLDER}에 SLD 파일이 없습니다.")
        return
    
    print(f"📁 {len(sld_files)}개의 SLD 파일을 처리합니다...")
    success_count = 0
    
    for filename in sld_files:
        style_name = os.path.splitext(filename)[0]
        file_path = os.path.join(SLD_FOLDER, filename)
        if upload_sld_to_geoserver(style_name, file_path):
            success_count += 1
    
    print(f"\n✅ 완료: {success_count}/{len(sld_files)} 파일 업로드 성공")

if __name__ == "__main__":
    main()