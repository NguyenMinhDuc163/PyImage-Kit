
import cv2
import sys
import os

 

def resize(src, w_ratio, h_ratio):
    """Resize image

    Args:
        src (numpy.ndarray): Image
        w_ratio (int): Width ratio
        h_ratio (int): Height ratio

    Returns:
        numpy.ndarray: Image
    """
    height = src.shape[0]
    width = src.shape[1]
    dst = cv2.resize(src, (int(width / 100 * w_ratio), int(height / 100 * h_ratio)))
    return dst

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 4:
        print("Usage: $ python " + param[0] + " sample.jpg wide_ratio height_ratio")
        quit()

    
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    w_ratio = int(param[2])
    h_ratio = int(param[3])

    output_img = resize(input_img, w_ratio, h_ratio)

    
    output_dir = 'output/resize'
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, 'resized_' + os.path.basename(param[1]))
    cv2.imwrite(output_path, output_img)
    print(f"Resized image saved to {output_path}")
