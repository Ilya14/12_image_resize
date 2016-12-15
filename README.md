# 12_image_resize

## Описание

Скрипт производит изменение размера изображений

## Использование

Обязательные параметры:

* image_path - путь до исходного изображения

Опциональные параметры:

* -h, --help - помощь
* --width - новая ширина изображения
* --height - новая высота изображения
* --scale - масштабный множитель
* --output - каталог для файла-результата

Скрипт работает следующим образом:

* Если указана только ширина – высота считается так, чтобы сохранить
пропорции изображения, и наоборот.
 
* Если указана и ширина и высота – создается именно такое изображение.
При этом в консоль выводится предупреждение, если пропорции не
совпадают с исходным изображением.
 
* Если указан масштаб, то ширина и высота указаны быть не могут. 
В противном случае выводится сообщение об ошибке.

* Если не указан путь до финального файла, то результат сохраняется
рядом с исходным файлом.

## Пример

Отображение справки:

```sh
$ python3.5 ./image_resize.py -h
usage: image_resize.py [-h] [--width WIDTH] [--height HEIGHT] [--scale SCALE]
                       [--output OUTPUT]
                       image_path

Script for image resizing

positional arguments:
  image_path       Input image path

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Image width
  --height HEIGHT  Image height
  --scale SCALE    Image scale
  --output OUTPUT  Result image path
```

Пример использования:

```sh
$ python3.5 ./image_resize.py --scale 0.5 ./pic.png
image_resize.py# INFO     [12/15/2016 03:45:33 PM] Image "./pic.png" with size 1920x1080 is loaded
image_resize.py# INFO     [12/15/2016 03:45:33 PM] File "./pic_960X540.png" saved
```