import numpy as np
import torch
from torchvision.ops import nms

def retinaface_correct_boxes(result, input_shape, image_shape):
    new_shape   = image_shape*np.min(input_shape/image_shape)

    offset      = (input_shape - new_shape) / 2. / input_shape
    scale       = input_shape / new_shape
    
    scale_for_boxs      = [scale[1], scale[0], scale[1], scale[0]]
    scale_for_landmarks = [scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1], scale[0], scale[1],
                           scale[0],
                           scale[1], scale[0], scale[1], scale[0], scale[1], scale[0]
                           ]

    offset_for_boxs         = [offset[1], offset[0], offset[1],offset[0]]
    offset_for_landmarks    = [offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0], offset[1], offset[0],
                               offset[1], offset[0],
                               offset[1], offset[0], offset[1], offset[0], offset[1], offset[0]
                               ]

    result[:, :4] = (result[:, :4] - np.array(offset_for_boxs)) * np.array(scale_for_boxs)
    result[:, 5:] = (result[:, 5:] - np.array(offset_for_landmarks)) * np.array(scale_for_landmarks)

    return result

def decode(loc, priors, variances):

    #anchors的形状  中心点的x，y  框的长、宽
    #x1,y1,x2,y2
    boxes = torch.cat((priors[:, :2] + loc[:, :2] * variances[0] * priors[:, 2:],
                    priors[:, 2:] * torch.exp(loc[:, 2:] * variances[1])), 1)
    boxes[:, :2] -= boxes[:, 2:] / 2
    boxes[:, 2:] += boxes[:, :2]
    return boxes

def decode_landm(pre, priors, variances):
    landms = torch.cat((priors[:, :2] + pre[:, :2] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 2:4] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 4:6] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 6:8] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 8:10] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 10:12] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 12:14] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 14:16] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 16:18] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 18:20] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 20:22] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 22:24] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 24:26] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 26:28] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 28:30] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 30:32] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 32:34] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 34:36] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 36:38] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 38:40] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 40:42] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 42:44] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 44:46] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 46:48] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 48:50] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 50:52] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 52:54] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 54:56] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 56:58] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 58:60] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 60:62] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 62:64] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 64:66] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 66:68] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 68:70] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 70:72] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 72:74] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 74:76] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 76:78] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 78:80] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 80:82] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 82:84] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 84:86] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 86:88] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 88:90] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 90:92] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 92:94] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 94:96] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 96:98] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 98:100] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 100:102] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 102:104] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 104:106] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 106:108] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 108:110] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 110:112] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 112:114] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 114:116] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 116:118] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 118:120] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 120:122] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 122:124] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 124:126] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 126:128] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 128:130] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 130:132] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 132:134] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 134:136] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 136:138] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 138:140] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 140:142] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 142:144] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 144:146] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 146:148] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 148:150] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 150:152] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 152:154] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 154:156] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 156:158] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 158:160] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 160:162] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 162:164] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 164:166] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 166:168] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 168:170] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 170:172] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 172:174] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 174:176] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 176:178] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 178:180] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 180:182] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 182:184] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 184:186] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 186:188] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 188:190] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 190:192] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 192:194] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 194:196] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 196:198] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 198:200] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 200:202] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 202:204] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 204:206] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 206:208] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 208:210] * variances[0] * priors[:, 2:],
                        priors[:, :2] + pre[:, 210:212] * variances[0] * priors[:, 2:],
                        ), dim=1)

    return landms

def iou(b1,b2):
    b1_x1, b1_y1, b1_x2, b1_y2 = b1[0], b1[1], b1[2], b1[3]
    b2_x1, b2_y1, b2_x2, b2_y2 = b2[:, 0], b2[:, 1], b2[:, 2], b2[:, 3]

    inter_rect_x1 = np.maximum(b1_x1, b2_x1)
    inter_rect_y1 = np.maximum(b1_y1, b2_y1)
    inter_rect_x2 = np.minimum(b1_x2, b2_x2)
    inter_rect_y2 = np.minimum(b1_y2, b2_y2)
    
    inter_area = np.maximum(inter_rect_x2 - inter_rect_x1, 0) * \
                 np.maximum(inter_rect_y2 - inter_rect_y1, 0)
    
    area_b1 = (b1_x2-b1_x1)*(b1_y2-b1_y1)
    area_b2 = (b2_x2-b2_x1)*(b2_y2-b2_y1)
    
    iou = inter_area/np.maximum((area_b1 + area_b2 - inter_area), 1e-6)
    return iou

def non_max_suppression(detection, conf_thres=0.5, nms_thres=0.3):

    mask        = detection[:, 4] >= conf_thres
    print(mask.shape)
    detection   = detection[mask]

    if len(detection) <= 0:
        return []

    keep = nms(
        detection[:, :4],
        detection[:, 4],
        nms_thres
    )
    best_box = detection[keep]
    return best_box.cpu().numpy()
