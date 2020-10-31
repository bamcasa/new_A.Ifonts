import cv2,os

directory = "crop_image"

path, dirs, files = next(os.walk(directory))
print(len(files))

for file in files:
    img = cv2.imread(f"{directory}/{file}", cv2.IMREAD_COLOR)

    height, width, channel = img.shape

    for i in range(height):
        for j in range(width):
            if img.item(i, j, 0) + img.item(i, j, 1) + img.item(i, j, 2) > 500:
                for m in range(3):
                    img.itemset(i, j, m, 255)
            else:
                for m in range(3):
                    img.itemset(i, j, m, 0)
    print(file)
    cv2.imwrite(f"{directory}/{file}", img)