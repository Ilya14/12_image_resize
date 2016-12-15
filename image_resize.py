import argparse
import logging
import os

from PIL import Image


def resize_image(input_data):
    if input_data['output_dir'] is None:
        input_data['output_dir'] = os.path.dirname(input_data['image_name'])

    image = get_image(input_data['image_name'])
    if image is not None:
        current_width, current_height = image.size
        logging.info(
            'Image "%s" with size %dx%d is loaded',
            input_data['image_name'],
            current_width,
            current_height
        )

        if input_data['scale'] is not None and input_data['width'] is None and input_data['height'] is None:
            new_size = (round(current_width * input_data['scale']), round(current_height * input_data['scale']))
            new_image = image.resize(new_size)
            save_image(new_image, get_new_image_file_name(*new_image.size, input_data))
        elif input_data['scale'] is None and input_data['width'] is not None and input_data['height'] is None:
            new_height = round(input_data['width'] * current_height / current_width)
            new_size = (input_data['width'], new_height)
            new_image = image.resize(new_size)
            save_image(new_image, get_new_image_file_name(*new_image.size, input_data))
        elif input_data['scale'] is None and input_data['width'] is None and input_data['height'] is not None:
            new_width = round(input_data['height'] * current_width / current_height)
            new_size = (new_width, input_data['height'])
            new_image = image.resize(new_size)
            save_image(new_image, get_new_image_file_name(*new_image.size, input_data))
        elif input_data['scale'] is None and input_data['width'] is not None and input_data['height'] is not None:
            current_ratio = current_width / current_height
            new_ratio = input_data['width'] / input_data['height']
            if new_ratio != current_ratio:
                logging.warning("Proportions of new and initial images don't coincide")
            new_size = (input_data['width'], input_data['height'])
            new_image = image.resize(new_size)
            save_image(new_image, get_new_image_file_name(*new_image.size, input_data))
        else:
            logging.error(
                '''
                Incorrect input parameters. Use -h or --help to get help message.
                Possible combinations of parameters: --scale; --width; --height; --width and --height in common
                '''
            )


def get_image(image_path):
    try:
        return Image.open(image_path)
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
    return '{0}/{1}_{2}X{3}{4}'.format(input_data['output_dir'], file_name, new_width, new_height, ext)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s# %(levelname)-8s [%(asctime)s] %(message)s',
        datefmt=u'%m/%d/%Y %I:%M:%S %p'
    )

    parser = argparse.ArgumentParser(description='Script for image resizing')
    parser.add_argument('image_path', help='Input image path')
    parser.add_argument('--width', type=int, help='Image width')
    parser.add_argument('--height', type=int, help='Image height')
    parser.add_argument('--scale', type=float, help='Image scale')
    parser.add_argument('--output', help='Result image path')
    args = parser.parse_args()

    input_data = {
        'image_name': args.image_path,
        'output_dir': args.output,
        'width': args.width,
        'height': args.height,
        'scale': args.scale
    }

    resize_image(input_data)


