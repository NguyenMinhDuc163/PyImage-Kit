import pytest
from extract_color import extract_color
import numpy as np

import cv2



def create_dummy_image(width, height, color):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image



def test_extract_color_low_high():
    
    src = create_dummy_image(100, 100, (255, 0, 0))
    h_th_low = 50
    h_th_up = 100
    s_th = 50
    v_th = 50

    
    result = extract_color(src, h_th_low, h_th_up, s_th, v_th)

    
    expected = np.zeros((100, 100), dtype=np.uint8)
    

    
    assert np.array_equal(result, expected), "The extract_color function did not perform as expected with low < high."


def test_extract_color_high_low():
    
    src = create_dummy_image(100, 100, (0, 255, 0))
    h_th_low = 70
    h_th_up = 50
    s_th = 50
    v_th = 50

    
    result = extract_color(src, h_th_low, h_th_up, s_th, v_th)

    
    expected = np.zeros((100, 100), dtype=np.uint8)

    
    assert np.array_equal(result, expected), "The extract_color function did not perform as expected with high > low."



def test_extract_color_sv_threshold():
    
    src = create_dummy_image(100, 100, (128, 128, 128))
    h_th_low = 20
    h_th_up = 30
    s_th = 100  
    v_th = 100  

    
    result = extract_color(src, h_th_low, h_th_up, s_th, v_th)

    
    expected = np.zeros((100, 100), dtype=np.uint8)  

    
    assert np.array_equal(result, expected), "The s_th and v_th thresholds did not filter out the pixels correctly."



def test_extract_color_with_none_image():
    with pytest.raises(cv2.error):
        extract_color(None, 50, 100, 50, 100)
