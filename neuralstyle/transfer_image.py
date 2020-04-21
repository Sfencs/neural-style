import os

import argparse
import numpy as np
from PIL import Image

import tensorflow as tf

import net
import vgg_preprocessing

# Content layer where will pull our feature maps
CONTENT_LAYERS = ['block4_conv2']

# Style layer we are interested in
STYLE_LAYERS = ['block1_conv1',
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']

STYLE_IMAGE_SIZE = 512
TEST_IMAGE_SIZE = 1024

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("mode",
                    help="Mode to run the script",
                    choices=["infer",])
parser.add_argument("--style_image_path",
                    help="Directory to save mode",
                    type=str,
                    default="")
parser.add_argument("--test_images_path",
                    help="A comma seperated string for paths of testing images",
                    type=str,
                    default="")



args = parser.parse_args()

STYLE_NAME = os.path.basename(args.style_image_path).split('.')[0]

input_shape = (None, None, 3)
img_input = tf.keras.layers.Input(shape=input_shape)

output = net.style_net(img_input)
model_output = tf.keras.models.Model(img_input, output)

test_img = {}
for path in args.test_images_path.split(','):
  name = os.path.basename(path).split('.')[0]
  print(path)
  img = tf.io.read_file(path)
  img = tf.image.decode_image(img)
  img = tf.cast(img, tf.float32)
  img = vgg_preprocessing._mean_image_subtraction(img)
  img = vgg_preprocessing._aspect_preserving_resize(img, TEST_IMAGE_SIZE)
  img = tf.expand_dims(img, 0)
  test_img[name] = img

model_output.load_weights('model/' + STYLE_NAME + '_model.h5')
for key in test_img:
    x = test_img[key]
    img = model_output.predict(x)[0]
    img = np.ndarray.astype(img, np.uint8)
    img = Image.fromarray(img, 'RGB')

    try:
        os.stat("output")
    except:
        os.makedirs("output")
    img.save("output/" + key + ".jpg", "JPEG")