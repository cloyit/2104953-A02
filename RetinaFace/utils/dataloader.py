import cv2
import numpy as np
import torch.utils.data as data
from PIL import Image
from utils.utils import preprocess_input


class DataGenerator(data.Dataset):
    def __init__(self, txt_path, img_size):
        self.img_size = img_size
        self.txt_path = txt_path

        self.imgs_path, self.words = self.process_labels()

    def __len__(self):
        return len(self.imgs_path)

    def get_len(self):
        return len(self.imgs_path)

    def __getitem__(self, index):

        img         = Image.open(self.imgs_path[index])
        labels      = self.words[index]
        annotations = np.zeros((0, 217))
        if len(labels) == 0:
            return img, annotations

        for idx, label in enumerate(labels):
            annotation = np.zeros((1, 217))

            annotation[0, 0] = label[0]  # x1
            annotation[0, 1] = label[1]  # y1
            annotation[0, 2] = label[2]  # x2
            annotation[0, 3] = label[3]  # y2

            for i in range(4,216):
                annotation[0,i] = label[i]

            annotation[0,216] = 1

            annotations = np.append(annotations, annotation, axis=0)
        target = np.array(annotations)

        img, target = self.get_random_data(img, target, [self.img_size,self.img_size])

        img = np.array(np.transpose(preprocess_input(img), (2, 0, 1)), dtype=np.float32)
        return img, target

    def rand(self, a=0, b=1):
        return np.random.rand()*(b-a) + a

    def get_random_data(self, image, targes, input_shape, jitter=.3, hue=.1, sat=1.5, val=1.5):
        #inputshape是训练时照片的尺寸
        #image是读取的输入照片的尺寸
        iw, ih  = image.size
        h, w    = input_shape
        box     = targes

        new_ar = w/h * self.rand(1-jitter,1+jitter)/self.rand(1-jitter,1+jitter)
        scale = self.rand(0.25, 3.25)
        if new_ar < 1:
            nh = int(scale*h)
            nw = int(nh*new_ar)
        else:
            nw = int(scale*w)
            nh = int(nw/new_ar)
        image = image.resize((nw,nh), Image.BICUBIC)

        dx = int(self.rand(0, w-nw))
        dy = int(self.rand(0, h-nh))
        new_image = Image.new('RGB', (w,h), (128,128,128))
        new_image.paste(image, (dx, dy))
        image = new_image

        hue = self.rand(-hue, hue)
        sat = self.rand(1, sat) if self.rand()<.5 else 1/self.rand(1, sat)
        val = self.rand(1, val) if self.rand()<.5 else 1/self.rand(1, val)
        x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
        x[..., 0] += hue*360
        x[..., 0][x[..., 0]>1] -= 1
        x[..., 0][x[..., 0]<0] += 1
        x[..., 1] *= sat
        x[..., 2] *= val
        x[x[:,:, 0]>360, 0] = 360
        x[:, :, 1:][x[:, :, 1:]>1] = 1
        x[x<0] = 0
        image_data = cv2.cvtColor(x, cv2.COLOR_HSV2RGB)*255

        if len(box)>0:
            np.random.shuffle(box)
            box[:, [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
                    38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
                    74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,
                    110,112,114,116,118,120,122,124,126,128,130,132,134,136,
                    138,140,142,144,146,148,150,152,154,156,158,160,162,164,
                    166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,
                    198,200,202,204,206,208,210,212,214]] = box[:,
                    [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
                    38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
                    74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,
                    110,112,114,116,118,120,122,124,126,128,130,132,134,136,
                    138,140,142,144,146,148,150,152,154,156,158,160,162,164,
                    166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,
                    198,200,202,204,206,208,210,212,214]]*nw/iw + dx
            box[:, [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,
                    47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,
                    91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,
                    127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,
                    163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,
                    199,201,203,205,207,209,211,213,215]] = \
                box[:, [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,
                    47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,
                    91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,
                    127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,
                    163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,
                    199,201,203,205,207,209,211,213,215]]*nh/ih + dy
            
            center_x = (box[:, 0] + box[:, 2])/2
            center_y = (box[:, 1] + box[:, 3])/2
        
            box = box[np.logical_and(np.logical_and(center_x>0, center_y>0), np.logical_and(center_x<w, center_y<h))]

            box[:, 0:216][box[:, 0:216]<0] = 0
            box[:, [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
                    38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
                    74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,
                    110,112,114,116,118,120,122,124,126,128,130,132,134,136,
                    138,140,142,144,146,148,150,152,154,156,158,160,162,164,
                    166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,
                    198,200,202,204,206,208,210,212,214]][box[:, [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
                    38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
                    74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,
                    110,112,114,116,118,120,122,124,126,128,130,132,134,136,
                    138,140,142,144,146,148,150,152,154,156,158,160,162,164,
                    166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,
                    198,200,202,204,206,208,210,212,214]]>w] = w
            box[:, [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,
                    47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,
                    91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,
                    127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,
                    163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,
                    199,201,203,205,207,209,211,213,215]][box[:, [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,
                    47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,
                    91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,
                    127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,
                    163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,
                    199,201,203,205,207,209,211,213,215]]>h] = h
            
            box_w = box[:, 2] - box[:, 0]
            box_h = box[:, 3] - box[:, 1]
            box = box[np.logical_and(box_w>1, box_h>1)] # discard invalid box

        box[:,4:-1][box[:,-1]==-1]=0
        box[:, [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
                    38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,
                    74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,
                    110,112,114,116,118,120,122,124,126,128,130,132,134,136,
                    138,140,142,144,146,148,150,152,154,156,158,160,162,164,
                    166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,
                    198,200,202,204,206,208,210,212,214]] /= w
        box[:, [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,
                    47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,
                    91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,
                    127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,
                    163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,
                    199,201,203,205,207,209,211,213,215]] /= h
        box_data = box
        return image_data, box_data
        
    def process_labels(self):
        imgs_path = []
        words = []
        txt_path = 'F:/Training_data/boundary.txt'

        f = open(txt_path, 'r')
        lines = f.readlines()
        isFirst = True
        labels = []
        for line in lines:
            line = line.rstrip()
            if isFirst is True:
                isFirst = False
            else:
                labels_copy = labels.copy()
                words.append([labels_copy])

                labels.clear()
            line = line.split(' ')
            path = line[0]
            landmark_path = path.replace('picture','landmark')
            #path = txt_path.replace('boundary.txt', 'images/') + path
            imgs_path.append(path)
            # label = [float(x) for x in line]
            label = line[1:]

            for l in label:
                labels.append(float(l))

            landmark_path = landmark_path + '.txt'
            fl = open(landmark_path, 'r')
            landmarks = fl.readlines()
            landmarks = landmarks[1:]
            for landmark in landmarks:
                landmark = landmark.rstrip()
                landmark = landmark.split(' ')
                lm_label = [float(x) for x in landmark]
                for lm in lm_label:
                    labels.append(lm)

        words.append([labels])
        return imgs_path, words

def detection_collate(batch):
    images  = []
    targets = []
    for img, box in batch:
        if len(box)==0:
            continue
        images.append(img)
        targets.append(box)
    images = np.array(images)
    return images, targets
