import os
import glob
import argparse

import numpy as np
import pandas as pd
import cv2
import yaml


def converter(output_dir, csv_path, images_dir=None, f=10, k1=0, k2=0):
    """Convert pose file into bundler file.

    Args:
        output_dir (str): output directory.
        csv_path (str): camera pose file path.
        images_dir (str, optional): image files directory. Defaults to None.
        f (float, optional): focal length. Defaults to 100.
        k1 (float, optional): distortion coefficients k1. Defaults to 0.
        k2 (float, optional): distortion coefficients k2. Defaults to 0.
    """

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df = df.sort_values('image_id')
    matrices = df[['r11', 'r12', 'r13', 'r21', 'r22', 'r23', 'r31', 'r32', 'r33']].to_numpy()
    vectors = df[['t1', 't2', 't3']].to_numpy()

    num_cameras = len(matrices)

    lines = []
    params = f'{f} {k1} {k2}\n'
    for matrix, vector in zip(matrices, vectors):
        matrix = matrix.reshape([3, 3])

        # For bundler format, invert transformation.
        matrix = matrix.T

        # For good visualize, multiply -1 for some reason.
        matrix[2] = - matrix[2]

        # alse invert vector.
        vector = - matrix @ vector

        lines.append(params)
        for row in matrix:
            lines.append(f'{row[0]} {row[1]} {row[2]}\n')
        
        lines.append(f'{vector[0]} {vector[1]} {vector[2]}\n')
    
    bundler_path = os.path.join(output_dir, 'bundler.out')
    with open(bundler_path, 'w', encoding='utf-8') as file:
        file.write('# Bundle file v0.3\n')
        file.write(f'{len(matrices)} 0\n')
        file.writelines(lines)


    if images_dir is not None:
        images_path_list = glob.glob(os.path.join(images_dir, '*.jpg'))
        images_path_list.sort()
    else:
        dummy_image_path = os.path.join(output_dir, 'dummy.jpg')
        dummy_image = np.zeros([int(f), int(f)]).astype(np.uint8)
        cv2.putText(dummy_image, 'IMAGE', (0, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
        images_path_list = []
        cv2.imwrite(dummy_image_path, dummy_image)
        for i in range(num_cameras):
            images_path_list.append('./dummy.jpg')

    image_list_path =os.path.join(output_dir, 'list.txt') 
    with open(image_list_path, 'w', encoding='utf-8') as file:

        for image_path in images_path_list:
            file.write(image_path  + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='./config.yaml')
    
    args = parser.parse_args()

    config_path = args.config

    with open(config_path, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    params = config['params']
    pose_file_path = config['pose_file_path']
    images_dir = config['images_dir']
    output_dir = config['output_dir']
    if images_dir == '':
        images_dir = None

    converter(output_dir, pose_file_path, images_dir, **params)


if __name__ == '__main__':
    main()
