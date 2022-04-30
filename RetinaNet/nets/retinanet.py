import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from nets.mobilenet025 import MobileNetV1
from utils.anchors import Anchors


class PyramidFeatures(nn.Module):
    #  [512, 1024, 2048]
    def __init__(self, C3_size, C4_size, C5_size, feature_size=256):
        super(PyramidFeatures, self).__init__()

        self.P5_1 = nn.Conv2d(C5_size, feature_size, kernel_size=1, stride=1, padding=0)
        self.P5_2 = nn.Conv2d(feature_size, feature_size, kernel_size=3, stride=1, padding=1)

        self.P4_1 = nn.Conv2d(C4_size, feature_size, kernel_size=1, stride=1, padding=0)
        self.P4_2 = nn.Conv2d(feature_size, feature_size, kernel_size=3, stride=1, padding=1)

        self.P3_1 = nn.Conv2d(C3_size, feature_size, kernel_size=1, stride=1, padding=0)
        self.P3_2 = nn.Conv2d(feature_size, feature_size, kernel_size=3, stride=1, padding=1)

        self.P6 = nn.Conv2d(C5_size, feature_size, kernel_size=3, stride=2, padding=1)

        self.P7_1 = nn.ReLU()
        self.P7_2 = nn.Conv2d(feature_size, feature_size, kernel_size=3, stride=2, padding=1)

    def forward(self, inputs):
        C3, C4, C5 = inputs
        _, _, h4, w4 = C4.size()
        _, _, h3, w3 = C3.size()

        # 75,75,512 -> 75,75,256
        P3_x = self.P3_1(C3)
        # 38,38,1024 -> 38,38,256
        P4_x = self.P4_1(C4)
        # 19,19,2048 -> 19,19,256
        P5_x = self.P5_1(C5)

        # 19,19,256 -> 38,38,256
        P5_upsampled_x = F.interpolate(P5_x, size=(h4, w4))
        # 38,38,256 + 38,38,256 -> 38,38,256
        P4_x = P5_upsampled_x + P4_x
        # 38,38,256 -> 75,75,256
        P4_upsampled_x = F.interpolate(P4_x, size=(h3, w3))
        # 75,75,256 + 75,75,256 -> 75,75,256
        P3_x = P3_x + P4_upsampled_x

        # 75,75,256 -> 75,75,256
        P3_x = self.P3_2(P3_x)
        # 38,38,256 -> 38,38,256
        P4_x = self.P4_2(P4_x)
        # 19,19,256 -> 19,19,256
        P5_x = self.P5_2(P5_x)

        # 19,19,2048 -> 10,10,256
        P6_x = self.P6(C5)

        P7_x = self.P7_1(P6_x)
        # 10,10,256 -> 5,5,256
        P7_x = self.P7_2(P7_x)

        return [P3_x, P4_x, P5_x, P6_x, P7_x]


class RegressionModel(nn.Module):
    def __init__(self, num_features_in, num_anchors=9, feature_size=256):
        super(RegressionModel, self).__init__()

        self.conv1  = nn.Conv2d(num_features_in, feature_size, kernel_size=3, padding=1)
        self.act1   = nn.ReLU()

        self.conv2  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act2   = nn.ReLU()

        self.conv3  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act3   = nn.ReLU()

        self.conv4  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act4   = nn.ReLU()

        self.output = nn.Conv2d(feature_size, num_anchors * 4, kernel_size=3, padding=1)

    def forward(self, x):
        out = self.conv1(x)
        out = self.act1(out)

        out = self.conv2(out)
        out = self.act2(out)

        out = self.conv3(out)
        out = self.act3(out)

        out = self.conv4(out)
        out = self.act4(out)

        out = self.output(out)

        out = out.permute(0, 2, 3, 1)

        return out.contiguous().view(out.shape[0], -1, 4)

class ClassificationModel(nn.Module):
    def __init__(self, num_features_in, num_anchors=9, num_classes=80, feature_size=256):
        super(ClassificationModel, self).__init__()

        self.num_classes = num_classes
        self.num_anchors = num_anchors

        self.conv1  = nn.Conv2d(num_features_in, feature_size, kernel_size=3, padding=1)
        self.act1   = nn.ReLU()

        self.conv2  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act2   = nn.ReLU()

        self.conv3  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act3   = nn.ReLU()

        self.conv4  = nn.Conv2d(feature_size, feature_size, kernel_size=3, padding=1)
        self.act4   = nn.ReLU()

        self.output = nn.Conv2d(feature_size, num_anchors * num_classes, kernel_size=3, padding=1)
        self.output_act = nn.Sigmoid()

    def forward(self, x):
        out = self.conv1(x)
        out = self.act1(out)

        out = self.conv2(out)
        out = self.act2(out)

        out = self.conv3(out)
        out = self.act3(out)

        out = self.conv4(out)
        out = self.act4(out)

        out = self.output(out)
        out = self.output_act(out)

        out1 = out.permute(0, 2, 3, 1)

        batch_size, height, width, channels = out1.shape

        out2 = out1.view(batch_size, height, width, self.num_anchors, self.num_classes)

        return out2.contiguous().view(x.shape[0], -1, self.num_classes)




#---------------------------------------------------#
#   人脸关键点预测
#---------------------------------------------------#
class LandmarkHead(nn.Module):
    def __init__(self,inchannels=256,num_anchors=9):
        super(LandmarkHead,self).__init__()
        self.conv1x1 = nn.Conv2d(inchannels,num_anchors*212,kernel_size=(1,1),stride=1,padding=0)

    def forward(self,x):
        out = self.conv1x1(x)
        out = out.permute(0,2,3,1).contiguous()

        return out.view(out.shape[0], -1, 212)

class retinanet(nn.Module):
    def __init__(self, num_classes, phi, pretrained=False):
        super(retinanet, self).__init__()
        self.pretrained = pretrained
        #-----------------------------------------#
        #   取出三个有效特征层，分别是C3、C4、C5
        #   假设输入图像为600,600,3
        #   当我们使用resnet50的时候
        #   C3     75,75,512
        #   C4     38,38,1024
        #   C5     19,19,2048
        #-----------------------------------------#
        self.backbone_net =MobileNetV1()
        fpn_sizes = {
            0: [128, 256, 512],
            1: [128, 256, 512],
            2: [512, 1024, 2048],
            3: [512, 1024, 2048],
            4: [512, 1024, 2048],
        }[phi]

        self.fpn = PyramidFeatures(fpn_sizes[0], fpn_sizes[1], fpn_sizes[2])

        self.regressionModel        = RegressionModel(256)
        self.classificationModel    = ClassificationModel(256, num_classes=num_classes)
        self.anchors = Anchors()
        self._init_weights()
        self.LandmarkHead = self._make_landmark_head(fpn_num=5, inchannels=256)

    def _init_weights(self):
        if not self.pretrained:
            for m in self.modules():
                if isinstance(m, nn.Conv2d):
                    n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif isinstance(m, nn.BatchNorm2d):
                    m.weight.data.fill_(1)
                    m.bias.data.zero_()
        
        prior = 0.01
        self.classificationModel.output.weight.data.fill_(0)
        self.classificationModel.output.bias.data.fill_(-math.log((1.0 - prior) / prior))
        self.regressionModel.output.weight.data.fill_(0)
        self.regressionModel.output.bias.data.fill_(0)

    def _make_landmark_head(self,fpn_num=5,inchannels=64,anchor_num=9):
        landmarkhead = nn.ModuleList()
        for i in range(fpn_num):
            landmarkhead.append(LandmarkHead(inchannels,anchor_num))
        return landmarkhead

    def forward(self, inputs):

        p3, p4, p5 = self.backbone_net(inputs)


        features = self.fpn([p3, p4, p5])

        regression      = torch.cat([self.regressionModel(feature) for feature in features], dim=1)
        classification  = torch.cat([self.classificationModel(feature) for feature in features], dim=1)
        ldm_regressions = torch.cat([self.LandmarkHead[i](feature) for i, feature in enumerate(features)], dim=1)

        print(regression.shape)
        print(classification.shape)
        print(ldm_regressions.shape)

        anchors = self.anchors(features)

        return features, regression, classification, anchors,ldm_regressions
