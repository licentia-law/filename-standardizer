import pytest
from file_processor import get_new_filename

def test_get_new_filename_basic():
    """기본 파일명 변환 규칙 테스트 (FR-02)"""
    # 0R2A 제거 + 숫자 4자리 추출 + 확장자 소문자
    assert get_new_filename("0R2A0813.JPG") == "IMG_0813.jpg"

def test_get_new_filename_correction():
    """보정 파일명 변환 규칙 테스트"""
    # _보정 문구를 숫자 1로 변환
    assert get_new_filename("0R2A0813_보정.png") == "IMG_08131.png"

def test_get_new_filename_no_match():
    """규칙에 맞지 않는 파일은 변경하지 않음"""
    assert get_new_filename("random_file.txt") == "random_file.txt"

def test_get_new_filename_correction_with_number():
    """보정 파일명 변환 규칙 테스트 (숫자 포함)"""
    # _보정 뒤의 숫자를 그대로 사용
    assert get_new_filename("0R2A0494_보정1.JPG") == "IMG_04942.jpg"
    assert get_new_filename("0R2A0494_보정2.png") == "IMG_04943.png"

def test_get_new_filename_imgp_prefix():
    """IMGP로 시작하는 파일명 변환 규칙 테스트"""
    # IMGP 제거 + 숫자 4자리 추출 + 확장자 소문자
    assert get_new_filename("IMGP1234.JPG") == "IMG_1234.jpg"

def test_get_new_filename_law_prefix():
    """Law_로 시작하는 파일명 변환 규칙 테스트"""
    assert get_new_filename("Law_231009_5019.JPG") == "IMG_5019.jpg"
    assert get_new_filename("Law_231009_5019_보정.png") == "IMG_50191.png"
    assert get_new_filename("Law_231009_5019_보정1.jpeg") == "IMG_50192.jpeg"

def test_get_new_filename_mey_prefix():
    """Mey_로 시작하는 파일명 변환 규칙 테스트"""
    assert get_new_filename("Mey_123456_7890.JPG") == "IMG_7890.jpg"
    assert get_new_filename("Mey_123456_7890_보정.png") == "IMG_78901.png"
    assert get_new_filename("Mey_123456_7890_보정1.jpeg") == "IMG_78902.jpeg"