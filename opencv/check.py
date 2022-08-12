import os
import cv2
import imghdr


def check_images(s_dir):  # 检查图片的格式
    bad_images = []
    bad_ext = []
    s_list = os.listdir(s_dir)
    ext_list = ['jpg', 'png', 'jpeg', 'gif', 'bmp']  # list of acceptable extensions
    for klass in s_list:
        klass_path = os.path.join(s_dir, klass)
        print('processing class directory ', klass)
        if os.path.isdir(klass_path):
            file_list = os.listdir(klass_path)
            for f in file_list:
                f_path = os.path.join(klass_path, f)
                tip = imghdr.what(f_path)
                if ext_list.count(tip) == 0:
                    bad_images.append(f_path)
                if os.path.isfile(f_path):
                    try:
                        img = cv2.imread(f_path)
                        shape = img.shape
                    except:
                        print('file ', f_path, ' is not a valid image file')
                        bad_images.append(f_path)
                else:
                    print('*** fatal error, you a sub directory ', f, ' in class directory ', klass)
        else:
            print('*** WARNING*** you have files in ', s_dir, ' it should only contain sub directories')
    if len(bad_images) != 0:
        print('improper image files are listed below')
        for i in range(len(bad_images)):
            print(bad_images[i])
    else:
        print(' no improper image files were found')


source_dir = 'C:\\Users\\kjhjk\\Desktop\\test\\testdata'

check_images(source_dir)
