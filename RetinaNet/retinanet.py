import colorsys
import numpy as np
import torch
import torch.nn as nn
from PIL import ImageDraw, ImageFont

from nets.retinanet import retinanet
from utils.utils import (cvtColor, get_classes,
                         resize_image)
from utils.utils_bbox import decodebox, non_max_suppression


class Retinanet(object):
    _defaults = {
        "model_path"        : 'logs/Epoch40-Total_Loss20.3585.pth',
        "classes_path"      : 'model_data/voc_classes.txt',
        "input_shape"       : [600, 600],

        "phi"               : 2,
        "confidence"        : 0.5,

        "nms_iou"           : 0.3,


        "letterbox_image"   : True,

        "cuda"              : True
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

        self.class_names, self.num_classes  = get_classes(self.classes_path)

        hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))

        self.generate()

    def generate(self):

        self.net    = retinanet(self.num_classes, self.phi)

        device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net    = self.net.eval()
        print('{} model, anchors, and classes loaded.'.format(self.model_path))

        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()

    def detect_image(self, image):

        image       = cvtColor(image)

        image_data = resize_image(image, (self.input_shape[1], self.input_shape[0]), self.letterbox_image)


        with torch.no_grad():
            images = torch.from_numpy(image_data)
            if self.cuda:
                images = images.cuda()

            _, regression, classification, anchors,landmarks = self.net(images)

            outputs     = decodebox(regression, anchors, self.input_shape)
            results     = non_max_suppression(torch.cat([outputs, classification], axis=-1), self.input_shape, 
                                    self.image_shape, self.letterbox_image, conf_thres = self.confidence, nms_thres = self.nms_iou)
               
            if results[0] is None: 
                return image

            top_label   = np.array(results[0][:, 5], dtype = 'int32')
            top_conf    = results[0][:, 4]
            top_boxes   = results[0][:, :4]

        font        = ImageFont.truetype(font='model_data/simhei.ttf', size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness   = int(max((image.size[0] + image.size[1]) // np.mean(self.input_shape), 1))

        for i, c in list(enumerate(top_label)):
            predicted_class = self.class_names[int(c)]
            box             = top_boxes[i]
            score           = top_conf[i]

            top, left, bottom, right = box

            top     = max(0, np.floor(top).astype('int32'))
            left    = max(0, np.floor(left).astype('int32'))
            bottom  = min(image.size[1], np.floor(bottom).astype('int32'))
            right   = min(image.size[0], np.floor(right).astype('int32'))

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)
            label = label.encode('utf-8')
            print(label, top, left, bottom, right)
            
            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle([left + i, top + i, right - i, bottom - i], outline=self.colors[c])
            draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=self.colors[c])
            draw.text(text_origin, str(label,'UTF-8'), fill=(0, 0, 0), font=font)
            del draw

        return image
