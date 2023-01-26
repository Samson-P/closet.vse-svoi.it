# Работа с изображениями
from PIL import Image
# Транслитерация
from transliterate import translit
import datetime
import os


# Подгружаем новую фотографию расходника в папку
def uploaded_image(POST_FILES) -> str:
    date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    file_extension = str(POST_FILES).split(".")[-1]
    path = f'web_interface/static/img/prepare/expenses/{date}.{file_extension}'
    with open(path, 'wb') as file:
        for chunk in POST_FILES.chunks():
            file.write(chunk)
    return path


# Готовим из POST запроса с файлом изображение и отдаем
def preparation(POST_FILES):
    path = uploaded_image(POST_FILES)
    return Image.open(path), path


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция для обрезки изображения по центру.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def resize(pil_img, size):
    return pil_img.resize((size, size))


def image_formatting(POST_FILES, pre_name):
    """

    :param POST_FILES: Файл, который вернет страница http://closet-it.ru/crm/expenses-6 в POST
    :param pre_name: Короткое имя расходника в БД
    :return: Путь к миниатюре изображения
    """
    # Дата и время форматирования используется для именования
    date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    # Короткое название, транслитерация и убираем точки
    pre_name = translit(pre_name, language_code='ru', reversed=True).replace(" ", "_").replace(".", "")

    # Подготовка и открытие файла
    image, OLD_PATH = preparation(POST_FILES)
    # Вырезаем максимальный квадрат и сохраняем для
    image = crop_max_square(image)
    # Меняем на стандартный размер 300*300
    image = resize(image, 300)
    # И сохраняем в JPEG
    pre = 'web_interface/static/img/jpeg/expenses/'
    image.save(f'{pre}{pre_name}{date}.jpeg')
    # Уменьшаем до 64*64
    image = resize(image, 64)
    # Сохраняем в папку PNG
    pre_min = 'web_interface/static/img/png/expenses/'
    image.save(f'{pre_min}{pre_name}{date}.png', quality=95)

    # Удаляем уже не нужный temp файл
    os.remove(OLD_PATH)

    return f'{pre_min}{pre_name}{date}.png'
