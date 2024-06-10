import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Пути до файлов
big_image_path = "/Users/artemprokudin/Downloads/YandexLMS/pythonProject/img/img_full.png"
small_images_dir = "/Users/artemprokudin/Downloads/YandexLMS/pythonProject/img/"
output_image_path = "/Users/artemprokudin/Downloads/YandexLMS/pythonProject/img/all_full_img.png"

# Размеры маленьких и большого изображений
big_image_width = 3024
big_image_height = 3024
small_image_width = 756
small_image_height = 756

# Количество строк и столбцов маленьких изображений
num_rows = 4
num_cols = 4

# Загружаем большое изображение как массив numpy
big_image = cv2.imread(big_image_path)
big_image_gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)

# Создаем пустое изображение для вставки маленьких изображений
output_image = Image.new('RGB', (big_image_width, big_image_height))

# Функция для поиска позиции маленького изображения на большом с использованием OpenCV
def find_position_opencv(big_image, small_image):
    result = cv2.matchTemplate(big_image, small_image, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    return max_loc

# Загружаем и вставляем каждое маленькое изображение в нужную клетку сетки
for index in range(1, num_rows * num_cols + 1):
    small_image_filename = os.path.join(small_images_dir, f"crop {index:02d}.png")
    if os.path.exists(small_image_filename):
        print(f"Обрабатывается изображение: {small_image_filename}")
        small_image = cv2.imread(small_image_filename, cv2.IMREAD_GRAYSCALE)
        small_image_pil = Image.open(small_image_filename)

        # Находим позицию маленького изображения на большом
        top_left = find_position_opencv(big_image_gray, small_image)

        # Вставляем маленькое изображение на большое
        output_image.paste(small_image_pil, top_left)

        # Добавляем название файла в центр маленького изображения
        draw = ImageDraw.Draw(output_image)
        font = ImageFont.load_default()  # Используем шрифт по умолчанию
        draw.text((top_left[0] + 10, top_left[1] + 10), f"crop {index:02d}.png", font=font, fill="white")
    else:
        print(f"Файл не найден: {small_image_filename}")

# Сохраняем полученное большое изображение
output_image.save(output_image_path)

print(f"Сохраненное изображение: {output_image_path}")
