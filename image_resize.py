import argparse
import logging
import os

from PIL import Image


def resize_image(image, input_data):
    if input_data['scale'] is not None and input_data['width'] is None and input_data['height'] is None:
        new_size = get_new_size_by_scale(image, input_data['scale'])
    elif input_data['scale'] is None and input_data['width'] is not None and input_data['height'] is None:
        new_size = get_new_size_by_width(image, input_data['width'])
    elif input_data['scale'] is None and input_data['width'] is None and input_data['height'] is not None:
        new_size = get_new_size_by_height(image, input_data['height'])
    elif input_data['scale'] is None and input_data['width'] is not None and input_data['height'] is not None:
        new_size = get_new_size_by_width_and_height(image, input_data['width'], input_data['height'])
    else:
        new_size = None
        logging.error(
            '''
            Incorrect input parameters. Use -h or --help to get help message.
            Possible combinations of parameters: --scale; --width; --height; --width and --height in common
            '''
        )

    if new_size is not None:
        return image.resize(new_size)


def get_new_size_by_scale(image, scale):
    current_width, current_height = image.size
    return round(current_width * scale), round(current_height * scale)


def get_new_size_by_width(image, new_width):
    current_width, current_height = image.size
    new_height = round(new_width * current_height / current_width)
    return new_width, new_height


def get_new_size_by_height(image, new_height):
    current_width, current_height = image.size
    new_width = round(new_height * current_width / current_height)
    return new_width, new_height


def get_new_size_by_width_and_height(image, new_width, new_height):
    current_width, current_height = image.size
    current_ratio = current_width / current_height
    new_ratio = new_width / new_height
    if new_ratio != current_ratio:
        logging.warning("Proportions of new and initial images don't coincide")
    return new_width, new_height


def get_image(image_path):
    try:
        image = Image.open(image_path)
        current_width, current_height = image.size
        logging.info(
            'Image "%s" with size %dx%d is loaded',
            input_data['image_name'],
            current_width,
            current_height
        )
        return image
    except IOError:
        logging.exception('Open image file "%s" error', image_path)


def save_image(image, file_name):
    try:
        image.save(file_name)
        logging.info('File "%s" saved', file_name)
    except IOError:
        logging.exception('Image file "%s" save error', file_name)


def get_new_image_file_name(new_width, new_height, input_data):
    file_name, ext = os.path.splitext(os.path.basename(input_data['image_name']))
    new_file_name = '{0}_{1}X{2}{3}'.format(file_name, new_width, new_height, ext)
    return os.path.join(input_data['output_dir'], new_file_name)


def get_input_data():
    parser = argparse.ArgumentParser(description='Script for image resizing')
    parser.add_argument('image_path', help='Input image path')
    parser.add_argument('--width', type=int, help='Image width')
    parser.add_argument('--height', type=int, help='Image height')
    parser.add_argument('--scale', type=float, help='Image scale')
    parser.add_argument('--output', help='Result image path')
    args = parser.parse_args()
    return {
        'image_name': args.image_path,
        'output_dir': args.output,
        'width': args.width,
        'height': args.height,
        'scale': args.scale
    }


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s# %(levelname)-8s [%(asctime)s] %(message)s',
        datefmt=u'%m/%d/%Y %I:%M:%S %p'
    )

    input_data = get_input_data()

    if input_data['output_dir'] is None:
        input_data['output_dir'] = os.path.dirname(input_data['image_name'])

    image = get_image(input_data['image_name'])

    if image is not None:
        new_image = resize_image(image, input_data)
        if new_image is not None:
            save_image(new_image, get_new_image_file_name(*new_image.size, input_data))
