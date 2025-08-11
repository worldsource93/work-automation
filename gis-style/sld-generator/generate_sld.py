import os
import numpy as np
import rasterio
import re
import sys
from qgis.core import (
    QgsRasterLayer, QgsColorRampShader, QgsRasterShader,
    QgsSingleBandPseudoColorRenderer, QgsStyle
)
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# === 사용자 지정 경로 ===
tif_dir = Path(os.getenv("TIF_DIR", "./input_tif"))
output_dir = Path(os.getenv("OUTPUT_DIR", "./output_sld"))
output_dir.mkdir(parents=True, exist_ok=True)

# === 설정 ===
color_map = {
    "prcp": "YlGnBu",  # 강수량 컬러 램프 이름 (QGIS 내장)
    "temp": "YlOrRd"   # 평균기온 컬러 램프 이름
}

# 밴드 이름에 사용할 기준 연도
BASE_YEAR = int(os.getenv("BASE_YEAR", "2020"))


# 대한민국 평균기온 범위 (경고용)
KOREA_TEMP_MIN = -10
KOREA_TEMP_MAX = 40

# QGIS 기본 컬러 램프 가져오기
def get_color_ramp(name):
    ramp = QgsStyle().defaultStyle().colorRamp(name)
    if not ramp:
        raise Exception(f"Color ramp '{name}' not found in QGIS.")
    return ramp

# 중복 급간, 0길이 급간 제거
def clean_breaks(breaks):
    clean = [breaks[0]]
    for val in breaks[1:]:
        if val > clean[-1]:
            clean.append(val)
    return clean

# rasterio로 실제 값 읽기 함수
def get_raster_values_rasterio(tif_path, band_index=1):
    try:
        with rasterio.open(tif_path) as src:
            if band_index > src.count:
                raise ValueError(f"밴드 인덱스 {band_index}가 범위를 벗어났습니다. (최대: {src.count})")
            data = src.read(band_index)
            values = data.flatten()
            values = values[~np.isnan(values)]
            if len(values) == 0:
                raise ValueError(f"유효한 래스터 값이 없습니다: {tif_path}")
            return values
    except Exception as e:
        print(f"❌ 래스터 파일 읽기 실패: {tif_path} - {e}")
        raise

# 스타일 생성 함수
def generate_sld(tif_path, variable_type):
    tif_name = os.path.splitext(os.path.basename(tif_path))[0]
    layer = QgsRasterLayer(tif_path, tif_name)

    if not layer.isValid():
        print(f"Invalid raster: {tif_path}")
        return

    provider = layer.dataProvider()
    band_count = provider.bandCount()

    for band in range(1, band_count + 1):
        stats = provider.bandStatistics(band)
        min_val, max_val = stats.minimumValue, stats.maximumValue

        # 급간 생성
        if variable_type == "prcp":
            # rasterio로 실제 데이터 읽기 후 Quantile 계산
            values = get_raster_values_rasterio(tif_path, band)
            quantiles = np.quantile(values, np.linspace(0, 1, 10))
            breaks = clean_breaks(np.round(quantiles, 2).tolist())
            ramp_name = color_map["prcp"]
        elif variable_type == "temp":
            # Equal interval 방식
            if min_val < KOREA_TEMP_MIN or max_val > KOREA_TEMP_MAX:
                print(f"[경고] 평균기온 범위 이상치 발견: {tif_name} 밴드 {band} ({min_val:.1f} ~ {max_val:.1f})")
            breaks = np.linspace(min_val, max_val, 10).tolist()
            ramp_name = color_map["temp"]
        else:
            print(f"Unknown variable type for {tif_path}")
            continue

        # 스타일 구성
        ramp = get_color_ramp(ramp_name)
        entries = []
        for i in range(len(breaks) - 1):
            val_min, val_max = breaks[i], breaks[i + 1]
            if val_min == val_max:
                # 무의미한 구간은 건너뜀
                continue

            # quantity 값은 소수점 둘째 자리에서 반올림(float)
            quantity_val = round(val_min, 2)

            # 라벨은 소수점 첫째 자리까지만 표시 (기온, 강수량 모두 동일)
            label = f"{quantity_val:.1f} – {round(val_max, 2):.1f}"

            color = ramp.color(float(i) / (len(breaks) - 2))
            entries.append(QgsColorRampShader.ColorRampItem(quantity_val, color, label))

        shader = QgsColorRampShader()
        shader.setColorRampType(QgsColorRampShader.Interpolated)
        shader.setColorRampItemList(entries)

        raster_shader = QgsRasterShader()
        raster_shader.setRasterShaderFunction(shader)

        renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band, raster_shader)
        layer.setRenderer(renderer)

        # SLD 스타일 저장
        sld_name = f"{tif_name}_{band+BASE_YEAR}.sld"
        sld_path = os.path.join(output_dir, sld_name)
        layer.saveSldStyle(sld_path)
        print(f"Saved: {sld_path}")

def detect_variable_type(filename):
    """파일명에서 변수 타입 감지"""
    patterns = {
        "prcp": re.compile(r".*prcp.*\.tif$", re.IGNORECASE),
        "temp": re.compile(r".*temp.*\.tif$", re.IGNORECASE)
    }
    
    for var_type, pattern in patterns.items():
        if pattern.match(filename):
            return var_type
    return None

def main():
    """메인 실행 함수"""
    if not tif_dir.exists():
        print(f"❌ TIF 디렉토리를 찾을 수 없습니다: {tif_dir}")
        sys.exit(1)
    
    tif_files = list(tif_dir.glob("*.tif"))
    
    if not tif_files:
        print(f"⚠️ {tif_dir}에 TIF 파일이 없습니다.")
        return
    
    print(f"📁 {len(tif_files)}개의 TIF 파일을 처리합니다...")
    success_count = 0
    
    for tif_path in tif_files:
        var_type = detect_variable_type(tif_path.name)
        
        if var_type:
            try:
                generate_sld(str(tif_path), var_type)
                success_count += 1
            except Exception as e:
                print(f"❌ 처리 실패: {tif_path.name} - {e}")
        else:
            print(f"⚠️ 변수 타입을 알 수 없음: {tif_path.name}")
    
    print(f"\n✅ 완료: {success_count}/{len(tif_files)} 파일 처리 성공")

if __name__ == "__main__":
    main()