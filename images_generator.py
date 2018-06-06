import os
import cv2
import glob
import numpy as np
import posixpath as path
import argparse
import sys

# Examplo (mesma linha hehe):
# python images_generator.py 
# --path "Caminho\\dos\\dados" 
# --format png 
# --quantity 100 
# --angle 45 
# --blur 20 20 
# --width 10 11 
# --height 10 12

parser = argparse.ArgumentParser(
    description='Scripts that generates more images')
parser.add_argument('--path', metavar='p', nargs='?', required=True,
                    type=str, help='Caminho das imagens [ uma pasta augmented sera criada ]')
parser.add_argument('--format', metavar='f', nargs='?', required=True,
                    type=str, help='Formato [ png, jpg ]')
parser.add_argument('--quantity', metavar='q', nargs='?',
                    type=int, help='Quantidade de novas imagens por imagem encontrada em path')
parser.add_argument('--angle', metavar='a', nargs='?',
                    type=int, help='Angulo minimo e maximo de rotacao')
parser.add_argument('--blur', metavar='b', nargs='+',
                    type=int, help='Valor minimo e maximo de blur')
parser.add_argument('--width', metavar='s', nargs='+',
                    type=int, help='Largura minima e maxima do resize')
parser.add_argument('--height', metavar='h', nargs='+',
                    type=int, help='Altura minima e maxima do resize')

def rotate_image(img, angle):
    (rows, cols, ch) = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(img, M, (cols, rows))

def resize_image(img, size):
    return cv2.resize(img, size)

def apply_blur(img, blur):
    return cv2.blur(img, blur)

def numeric_image_path(pathstring, n):
    return pathstring + "_" + str(n) + ".png"

def get_image_name(pathstring):
    imgname = pathstring.split('\\')[-1]
    imgname = imgname.split('.')[0]
    return imgname

if __name__ == '__main__':
    args = parser.parse_args()
    if not args.angle and not args.blur and not args.width and not args.height:
        raise Exception(
            'Use ao menos uma das transformacoes [rotacao, blur, tamanho]')

    basepath = args.path
    images = glob.glob(basepath + '\\*.%s' % args.format, recursive=True)
    blur = tuple(args.blur) if args.blur else None
    quantity = args.quantity if args.quantity else 100
    for imgpath, i in zip(images, range(len(images))):
        print(imgpath)
        imgname = get_image_name(imgpath)

        augmented_path = basepath + "/augmentation/" + imgname
        if not path.exists(augmented_path):
            os.mkdir(augmented_path)
        final_path = augmented_path + "/" + imgname

        cv2.imwrite(numeric_image_path(final_path, 0),  cv2.imread(imgpath))

        for x in range(1, quantity):
            image=cv2.imread(imgpath)

            angle=np.random.randint(
                0-(args.angle), args.angle) if args.angle else None
            modified_image=rotate_image(image, angle = angle)

            if blur:
                modified_image=apply_blur(modified_image, blur = blur)

            if args.width and args.height:
                width=np.random.randint(args.width[0], args.width[1])
                height=np.random.randint(args.height[0], args.height[1])
                modified_image=resize_image(
                    modified_image, size = (width, height))
            cv2.imwrite(numeric_image_path(final_path, x), modified_image)


