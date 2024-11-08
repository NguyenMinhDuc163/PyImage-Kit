
import cv2
import sys
import os




def combine_photos(image_paths):
    
    images = [cv2.imread(path) for path in image_paths]

    
    if any(img is None for img in images):
        print("One or more images could not be loaded. Please check the file paths.")
        return None

    
    if len(images) != 4:
        print("Số lượng ảnh không đủ để kết hợp.")
        return None

    
    height, width = images[0].shape[:2]
    resized_images = [cv2.resize(img, (width, height)) for img in images]

    
    img5 = cv2.vconcat([resized_images[0], resized_images[1]])
    img6 = cv2.vconcat([resized_images[2], resized_images[3]])
    combined_img = cv2.hconcat([img5, img6])

    
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'combined_output.jpg')
    cv2.imwrite(output_path, combined_img)
    print(f"Combined image saved to {output_path}")

    return combined_img





if __name__ == '__main__':
    
    param = sys.argv
    if len(param) != 5:
        print("Usage: $ python " + param[0] + " image1.jpg image2.jpg image3.jpg image4.jpg")
        quit()

    
    img1 = cv2.imread(param[1])
    img2 = cv2.imread(param[2])
    img3 = cv2.imread(param[3])
    img4 = cv2.imread(param[4])

    
    if img1 is None or img2 is None or img3 is None or img4 is None:
        print("One or more images could not be loaded. Please check the file paths.")
        quit()

    
    img5 = cv2.vconcat([img1, img2])
    img6 = cv2.vconcat([img3, img4])
    img7 = cv2.hconcat([img5, img6])

    
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, 'combined_output.jpg')
    cv2.imwrite(output_path, img7)
    print(f"Combined image saved to {output_path}")
