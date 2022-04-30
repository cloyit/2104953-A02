import torch
import torch.nn as nn

from nets.retinaface import RetinaFace
from utils.anchors import Anchors
from utils.config import cfg_mnet, cfg_re50
from utils.utils import letterbox_image, preprocess_input
from utils.utils_bbox import (decode, decode_landm, non_max_suppression,
                              retinaface_correct_boxes)

import cv2
import time
import os
from scipy.spatial import distance as dist
import numpy as np

from utils2.utils import cvtColor, get_classes, resize_image, preprocess_input



# 储存截图的目录
path_screenshots = "data/screenshots/"

cap = cv2.VideoCapture(0)
cap.set(3, 480)

screenshot_cnt = 0
f = 0
count = 0
f2 = 0
count2 = 0

def clear_screenshots():
    ss = os.listdir("data/screenshots/")
    for image in ss:
        print("Remove: ", "data/screenshots/"+image)
        os.remove("data/screenshots/"+image)

def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

class Retinaface(object):
    _defaults = {
        #model_path指向logs文件夹下的权值文件
        #"model_path"        : 'model_data/Retinaface_mobilenet0.25.pth',
        "model_path": 'logs/Epoch40-Total_Loss20.3585.pth',
        #"model_path": 'model_data/Retinaface_resnet50.pth',
        "backbone"          : 'mobilenet',

        "confidence"        : 0.9,

        "nms_iou"           : 0.45,

        "input_shape"       : [1280, 1280, 3],

        "letterbox_image"   : True,

        "cuda"              : True,

    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)

        if self.backbone == "mobilenet":
            self.cfg = cfg_mnet
        else:
            self.cfg = cfg_re50

        if self.letterbox_image:
            self.anchors = Anchors(self.cfg, image_size=[self.input_shape[0], self.input_shape[1]]).get_anchors()
        self.generate()
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0

    def generate(self):

        self.net    = RetinaFace(cfg=self.cfg, mode='eval').eval()

        device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net    = self.net.eval()
        print('{} model, and classes loaded.'.format(self.model_path))

        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()

    def detect_image(self, image):

        old_image = image.copy()
        dilb_image = image.copy()
        frame = image.copy()

        image = np.array(image,np.float32)

        im_height, im_width, _ = np.shape(image)

        scale = [
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0]
        ]
        scale_for_landmarks = [
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0],np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0], np.shape(image)[1], np.shape(image)[0],
            np.shape(image)[1], np.shape(image)[0] ]

        if self.letterbox_image:
            image = letterbox_image(image, [self.input_shape[1], self.input_shape[0]])
        else:
            self.anchors = Anchors(self.cfg, image_size=(im_height, im_width)).get_anchors()
            
        with torch.no_grad():

            # unsqueeze增加维度  squeeze删去某一维度  该维度只能是1

            image = torch.from_numpy(preprocess_input(image).transpose(2, 0, 1)).unsqueeze(0).type(torch.FloatTensor)
            if self.cuda:
                self.anchors = self.anchors.cuda()
                image        = image.cuda()

            loc, conf, landms = self.net(image)
            # after cat
            # torch.Size([1, 67200, 4])
            # torch.Size([1, 67200, 2])
            # torch.Size([1, 67200, 10])

            boxes   = decode(loc.data.squeeze(0), self.anchors, self.cfg['variance'])

            conf    = conf.data.squeeze(0)[:, 1:2]

            landms  = decode_landm(landms.data.squeeze(0), self.anchors, self.cfg['variance'])


            boxes_conf_landms = torch.cat([boxes, conf, landms], 1)
            boxes_conf_landms = non_max_suppression(boxes_conf_landms, self.confidence)
            if len(boxes_conf_landms) <= 0:
                return old_image

            if self.letterbox_image:
                boxes_conf_landms = retinaface_correct_boxes(boxes_conf_landms, \
                    np.array([self.input_shape[0], self.input_shape[1]]), np.array([im_height, im_width]))

        boxes_conf_landms[:, :4] = boxes_conf_landms[:, :4] * scale
        boxes_conf_landms[:, 5:] = boxes_conf_landms[:, 5:] * scale_for_landmarks

        for b in boxes_conf_landms:
            text = "{:.4f}".format(b[4])
            b = list(map(int, b))

            cv2.rectangle(old_image, (b[0], b[1]), (b[2], b[3]), (0, 0, 0), 2)
            cx = b[0]
            cy = b[1] + 12
            cv2.putText(old_image, 'person', (cx, cy),cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,0))

            for i in range(0, 106):
                cv2.circle(old_image, (b[2*i+5], b[2*i+6]), 1, (255, 255, 255), 1)
        demo = (b[107] - b[5])/(b[69] - b[107])

        if demo > 3 or demo < 0.4:
            f3 = 1
            self.count3 += 1
            self.count3 += 1
            if (self.count3 >= 10):
                cv2.putText(old_image, "lack of focus", (20, 150), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0))
        else:
            f3 = 0
            self.count3 = 0

        demo2 = (b[69] - b[5])/(b[38] - b[108])

        if demo2 > 1.2:
            f4 = 1
            self.count4 += 1
            self.count4 += 1
            if (self.count4 >= 5):
                cv2.putText(old_image, "lack of focus", (20, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0))
        else:
            f4 = 0
            self.count4 = 0
        return old_image