from itertools import product as product
from math import ceil
import torch

# 实现规定好真实框的尺寸  把真实框转成先验框  预测框直接回归到先验框上
class Anchors(object):
    def __init__(self, cfg, image_size=None):
        super(Anchors, self).__init__()
        self.min_sizes  = cfg['min_sizes']
        self.steps      = cfg['steps']
        self.clip       = cfg['clip']

        self.image_size = image_size

        #ceil 向上取整数
        #三个特征层的尺寸
        self.feature_maps = [[ceil(self.image_size[0]/step), ceil(self.image_size[1]/step)] for step in self.steps]

    def get_anchors(self):
        anchors = []
        for k, f in enumerate(self.feature_maps):
            #k 0 1 2
            #f [80,80] [40,40] [20,20]
            min_sizes = self.min_sizes[k]

            for i, j in product(range(f[0]), range(f[1])):
                #product返回笛卡尔积
                #从0,0 遍历到80,80
                for min_size in min_sizes:
                    s_kx = min_size / self.image_size[1]
                    s_ky = min_size / self.image_size[0]
                    dense_cx = [x * self.steps[k] / self.image_size[1] for x in [j + 0.5]]
                    dense_cy = [y * self.steps[k] / self.image_size[0] for y in [i + 0.5]]
                    for cy, cx in product(dense_cy, dense_cx):
                        anchors += [cx, cy, s_kx, s_ky]

        output = torch.Tensor(anchors).view(-1, 4)

        if self.clip:
            #将输入input张量每个元素的夹紧到区间 [min,max][min,max]，并返回结果到一个新张量。
            output.clamp_(max=1, min=0)
        return output

