import cv2,os

directory = "crop_image"

path, dirs, files = next(os.walk(directory))
print(len(files))

def find_pixel_avg(img):
    height, width = img.shape
    sum = 0
    for i in range(height):
        for j in range(width):
            sum += img.item(i, j)
    avg = sum/(height*width)
    return avg



for file in files:
    img = cv2.imread(f"{directory}/{file}", cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    pixel_avg = find_pixel_avg(img)
    for i in range(height):
        for j in range(width):
            if img.item(i, j) >= pixel_avg-10:
                img.itemset(i, j, 255)
            else:
                img.itemset(i, j, 0)
    print(file)
    cv2.imwrite(f"{directory}/{file}", img)