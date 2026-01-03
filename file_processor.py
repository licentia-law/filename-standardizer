import os
import re
from PIL import Image
import pillow_heif
import shutil # 파일 복사를 위해 추가
import logging # 로그 기록을 위해 추가

# pillow_heif 등록
pillow_heif.register_heif_opener()

# FR-05: ERROR만 파일 기록
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def _get_suffix_from_correction_match(correction_group, correction_number_group):
    """
    '_보정' 관련 정규식 매치 그룹에서 suffix를 생성합니다.
    correction_group: '_보정' 또는 '_보정N' 전체 매치 (예: '_보정', '_보정1')
    correction_number_group: '_보정' 뒤의 숫자 부분 (예: '1', '2' 또는 None)
    """
    suffix = ""
    if correction_group: # '_보정' 또는 '_보정N' 부분이 있는 경우
        if correction_number_group: # '_보정' 뒤에 숫자가 있는 경우
            suffix = str(int(correction_number_group) + 1)
        else: # '_보정'만 있는 경우
            suffix = "1"
    return suffix

def get_new_filename(original_filename):
    """
    PRD FR-02 규칙에 따라 새 파일명을 생성합니다.
    - `0R2A0813.jpg` -> `IMG_0813.jpg`
    - `0R2A0813_보정.png` -> `IMG_08131.png`
    """
    base_name, ext = os.path.splitext(original_filename)
    lower_ext = ext.lower()

    # FR-02: '0R2A'로 시작하는 파일명 처리
    # 예: 0R2A0813.JPG -> IMG_0813.jpg
    # 예: 0R2A0813_보정.png -> IMG_08131.png
    # 예: 0R2A0494_보정1.JPG -> IMG_04942.jpg
    match_0r2a = re.match(r'^0R2A(\d{4})(_보정(\d+)?)?$', base_name, re.IGNORECASE)
    if match_0r2a:
        number_part = match_0r2a.group(1)   # 숫자 4자리 (예: 0813)
        suffix = _get_suffix_from_correction_match(match_0r2a.group(2), match_0r2a.group(3))
        return f"IMG_{number_part}{suffix}{lower_ext}"

    # 요구사항: 'Law_'로 시작하는 파일명 처리
    # 예: Law_231009_5019.JPG -> IMG_5019.jpg
    # 예: Law_231009_5019_보정.JPG -> IMG_50191.jpg
    # 예: Law_231009_5019_보정1.JPG -> IMG_50192.jpg
    match_law = re.match(r'^Law_\d{6}_(\d{4})(_보정(\d+)?)?$', base_name, re.IGNORECASE)
    if match_law:
        number_part = match_law.group(1) # 마지막 4자리 숫자
        suffix = _get_suffix_from_correction_match(match_law.group(2), match_law.group(3))
        return f"IMG_{number_part}{suffix}{lower_ext}"

    # 요구사항: 'Mey_'로 시작하는 파일명 처리
    # 예: Mey_123456_7890.JPG -> IMG_7890.jpg
    # 예: Mey_123456_7890_보정.JPG -> IMG_78901.jpg
    # 예: Mey_123456_7890_보정1.JPG -> IMG_78902.jpg
    match_mey = re.match(r'^Mey_\d{6}_(\d{4})(_보정(\d+)?)?$', base_name, re.IGNORECASE)
    if match_mey:
        number_part = match_mey.group(1) # 마지막 4자리 숫자
        suffix = _get_suffix_from_correction_match(match_mey.group(2), match_mey.group(3))
        return f"IMG_{number_part}{suffix}{lower_ext}"

    # 요구사항: 'IMGP'로 시작하는 파일명 처리
    # 예: IMGP1234.JPG -> IMG_1234.jpg
    match_imgp = re.match(r'^IMGP(\d{4})$', base_name, re.IGNORECASE)
    if match_imgp:
        number_part = match_imgp.group(1) # 숫자 4자리 (예: 1234)
        return f"IMG_{number_part}{lower_ext}"

    # 규칙에 맞지 않는 파일은 원본 이름 그대로 반환
    return original_filename

def process_files(source_dir, progress_callback=None, status_callback=None):
    """
    지정된 디렉토리의 파일들을 재귀적으로 처리합니다.
    PRD FR-01, FR-03, FR-05 요구사항을 구현합니다.
    # - 하위 폴더 재귀 탐색
    # - result 폴더 생성 및 원본 구조 유지
    # - HEIC/HIF 변환
    # - 로그 (ERROR만) 기록
    """
    if not os.path.isdir(source_dir):
        logging.error(f"소스 디렉토리가 존재하지 않거나 유효하지 않습니다: {source_dir}")
        if status_callback:
            status_callback(f"오류: 소스 디렉토리가 유효하지 않습니다.")
        return

    result_dir = os.path.join(source_dir, "result")
    os.makedirs(result_dir, exist_ok=True)

    # FR-03: 허용 확장자
    allowed_image_exts = ['.cr3', '.jpg', '.jpeg', '.png', '.gif', '.heic', '.hif', '.dng']
    allowed_video_exts = ['.mp4', '.wma', '.mov']
    all_allowed_exts = allowed_image_exts + allowed_video_exts

    total_files = 0
    processed_files_count = 0
    
    # 1차 순회: 총 파일 수 계산 (진행률 표시용)
    for root, _, files in os.walk(source_dir):
        # 결과 디렉토리 자체는 처리 대상에서 제외
        if os.path.commonpath([result_dir, root]) == result_dir and root != result_dir:
            continue
        if root == result_dir: # result_dir 자체도 건너뛰기
            continue

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in all_allowed_exts:
                total_files += 1

    if status_callback:
        status_callback(f"총 {total_files}개의 파일 처리 예정...")

    # 2차 순회: 실제 파일 처리
    for root, _, files in os.walk(source_dir):
        # 결과 디렉토리 자체는 처리 대상에서 제외
        if os.path.commonpath([result_dir, root]) == result_dir and root != result_dir:
            continue
        if root == result_dir: # result_dir 자체도 건너뛰기
            continue

        relative_path = os.path.relpath(root, source_dir)
        destination_sub_dir = os.path.join(result_dir, relative_path)
        os.makedirs(destination_sub_dir, exist_ok=True)

        for original_filename in files:
            original_filepath = os.path.join(root, original_filename)
            base_name, ext = os.path.splitext(original_filename)
            lower_ext = ext.lower()

            if lower_ext not in all_allowed_exts:
                logging.warning(f"지원하지 않는 파일 형식 (건너감): {original_filepath}")
                if status_callback:
                    status_callback(f"건너감: {original_filename} (지원하지 않는 형식)")
                continue

            try:
                new_filename_base_with_ext = get_new_filename(original_filename)
                new_base_name, new_ext = os.path.splitext(new_filename_base_with_ext)

                if new_filename_base_with_ext == original_filename:
                    log_message = f"규칙에 맞지 않아 원본 파일명 유지: {original_filename}"
                    if status_callback:
                        status_callback(log_message)
                
                final_new_filename = new_filename_base_with_ext
                counter = 1
                # 파일명 충돌 처리 (FR-02: "충돌 시 숫자 증가" - _보정1 외 일반적인 충돌에도 적용)
                while os.path.exists(os.path.join(destination_sub_dir, final_new_filename)):
                    final_new_filename = f"{new_base_name}{counter}{new_ext}"
                    counter += 1

                destination_filepath = os.path.join(destination_sub_dir, final_new_filename)

                if lower_ext in ['.heic', '.hif']:
                    # HEIC/HIF 파일을 JPG로 변환
                    if status_callback:
                        status_callback(f"변환 중: {original_filename} -> {final_new_filename}")
                    
                    # Ensure output is JPG
                    dest_filepath_for_conversion = os.path.splitext(destination_filepath)[0] + ".jpg"
                    
                    image = Image.open(original_filepath)
                    image.save(dest_filepath_for_conversion, format="jpeg")
                    if status_callback:
                        status_callback(f"변환 완료: {original_filename} -> {os.path.basename(dest_filepath_for_conversion)}")
                else:
                    # 그 외 허용된 파일은 파일명만 변경하여 복사
                    if status_callback:
                        status_callback(f"복사 중: {original_filename} -> {final_new_filename}")
                    shutil.copy2(original_filepath, destination_filepath)
                    if status_callback:
                        status_callback(f"복사 완료: {original_filename} -> {final_new_filename}")

                processed_files_count += 1
                if progress_callback:
                    progress_callback(processed_files_count, total_files)

            except Exception as e:
                logging.error(f"파일 처리 중 오류 발생: {original_filepath} - {e}", exc_info=True)
                if status_callback:
                    status_callback(f"오류 발생: {original_filename} - {e}")
                # NFR-01: 단일 파일 오류 시 전체 중단 ❌, 파일 단위 예외 처리 ⭕
                # 다음 파일로 계속 진행

    if status_callback:
        status_callback("모든 파일 처리 완료.")