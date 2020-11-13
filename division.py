import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import os

with open("model_labels.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    #for line in lines:
    #   print(line.strip())

path, dirs, files = next(os.walk("crop_image"))

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

for file in files:
    image = Image.open(f'crop_image/{file}')
    original_image = Image.open(f'crop_image/{file}')

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #image.show()
    #original_image.show()

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(f"{file}",lines[prediction.argmax()].strip(), prediction.max())
    if prediction.max() >= 0.97:
        if os.path.isdir(f"Classified_image/{lines[prediction.argmax()].strip().split()[1]}"):
            original_image.save(f"Classified_image/{lines[prediction.argmax()].strip().split()[1]}/{file}")
        else:
            os.mkdir(f"Classified_image/{lines[prediction.argmax()].strip().split()[1]}")
            original_image.save(f"Classified_image/{lines[prediction.argmax()].strip().split()[1]}/{file}")
