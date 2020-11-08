import os
from PIL import Image, ImageOps
import numpy as np

inpput_directory = "Classified_image"
output_directory = "Formalization_image"
path, dirs, files = next(os.walk(f"{inpput_directory}"))

if not os.path.isdir(f"{output_directory}"):
    os.mkdir(f"{output_directory}")

for dir in dirs:
    path, dirs2, files = next(os.walk(f"{inpput_directory}/{dir}"))

    for file in files:
        image = Image.open(f"{inpput_directory}/{dir}/{file}")
        x, y = image.size

        if x > y :
            new_size = x
            x_offset = 0
            y_offset = int((x-y)/2)
        elif y > x:
            new_size = y
            x_offset = int((y-x) / 2)
            y_offset = 0

        background_color = "white"
        new_image = Image.new("RGBA", (new_size, new_size), background_color)
        new_image.paste(image, (x_offset, y_offset))

        new_image = ImageOps.fit(new_image, (214,214), Image.ANTIALIAS)

        base_image = Image.new("RGBA", (224, 224), background_color)
        base_image.paste(new_image, (10, 10))

        new_image = base_image

        if not os.path.isdir(f"{output_directory}/{dir}"):
            os.mkdir(f"{output_directory}/{dir}")

        new_image.save(f"{output_directory}/{dir}/{file}")

