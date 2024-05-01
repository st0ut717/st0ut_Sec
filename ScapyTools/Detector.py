import cv2
import os

root = '/home/st0ut/Pictures'
faces = '/home/st0ut/Pictures/Faces'
training = '/home/st0ut/Pictures/Training'

def detect(srcdir=root, tgtdir=faces, train_dir=training):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('JPG'):
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.joint(tgtdir, fname)
        img = cv2.imread(fullname)
        if img is None:
            continue
        grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        train = os.path.join(traing_dir, 'haarcascade_frountalface_alt.xml')
        cascade = cv2.CascadeClassifier(train)
        rects = cascade.detectMultiScale(grey, 1.3, 5)
        try:
            if rects.any():
                print('Got a face!!!')
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}')
            continue
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
            cv2.imwrite(newname, img)

if name == '__main__':
    detect()
