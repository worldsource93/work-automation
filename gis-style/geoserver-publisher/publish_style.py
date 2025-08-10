import os
import requests

# 🛠 GeoServer 접속 정보 - 사용자 설정 필요
GEOSERVER_URL = ""
GEOSERVER_USER = ""
GEOSERVER_PASSWORD = ""
WORKSPACE = ""

# 📁 SLD 파일이 저장된 로컬 폴더 경로 - 사용자 설정 필요
SLD_FOLDER = ""

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
    check_response = requests.get(style_check_url, auth=(GEOSERVER_USER, GEOSERVER_PASSWORD))

    if check_response.status_code == 200:
        print(f"🔁 {style_name} 스타일이 이미 존재함. 덮어쓰기 중...")
        # PUT: 기존 스타일 덮어쓰기
        put_url = f"{upload_url}/{style_name}"
        response = requests.put(put_url, headers=headers, data=sld_data,
                                auth=(GEOSERVER_USER, GEOSERVER_PASSWORD))
    else:
        print(f"➕ {style_name} 스타일 새로 업로드 중...")
        # POST: 새로운 스타일 생성
        response = requests.post(upload_url, headers=headers, params=params, data=sld_data,
                                 auth=(GEOSERVER_USER, GEOSERVER_PASSWORD))

    # 결과 확인
    if response.status_code in [200, 201]:
        print(f"✅ 스타일 업로드 성공: {style_name}")
    else:
        print(f"❌ 업로드 실패: {style_name} (코드 {response.status_code}) - {response.text}")

# ▶ 실행: 폴더 내 모든 SLD 파일 업로드
for filename in os.listdir(SLD_FOLDER):
    if filename.endswith(".sld"):
        style_name = os.path.splitext(filename)[0]  # 확장자 제거한 파일명
        file_path = os.path.join(SLD_FOLDER, filename)
        upload_sld_to_geoserver(style_name, file_path)
