import torch
import torch.nn as nn
import torch.nn.functional as F

def point_form(boxes):
    return torch.cat((boxes[:, :2] - boxes[:, 2:]/2,
                     boxes[:, :2] + boxes[:, 2:]/2), 1)


def center_size(boxes):
    return torch.cat((boxes[:, 2:] + boxes[:, :2])/2,
                     boxes[:, 2:] - boxes[:, :2], 1)


def intersect(box_a, box_b):
    A = box_a.size(0)
    '''
    print('box_a.size')
    print(A)
    print('box_b.size')
    '''
    B = box_b.size(0)
    max_xy = torch.min(box_a[:, 2:].unsqueeze(1).expand(A, B, 2),
                       box_b[:, 2:].unsqueeze(0).expand(A, B, 2))

    min_xy = torch.max(box_a[:, :2].unsqueeze(1).expand(A, B, 2),
                       box_b[:, :2].unsqueeze(0).expand(A, B, 2))
    inter = torch.clamp((max_xy - min_xy), min=0)

    return inter[:, :, 0] * inter[:, :, 1]

def jaccard(box_a, box_b):

    inter = intersect(box_a, box_b)

    area_a = ((box_a[:, 2]-box_a[:, 0]) *
              (box_a[:, 3]-box_a[:, 1])).unsqueeze(1).expand_as(inter)  # [A,B]
    area_b = ((box_b[:, 2]-box_b[:, 0]) *
              (box_b[:, 3]-box_b[:, 1])).unsqueeze(0).expand_as(inter)  # [A,B]

    union = area_a + area_b - inter

    return inter / union  # [A,B]

def encode(matched, priors, variances):
    # matched [priors,4]
    # priors [priors,4]
    # variances [0.1,0.2]
    # 进行编码的操作
    g_cxcy = (matched[:, :2] + matched[:, 2:])/2 - priors[:, :2]
    # 中心编码
    g_cxcy /= (variances[0] * priors[:, 2:])
    
    # 宽高编码
    g_wh = (matched[:, 2:] - matched[:, :2]) / priors[:, 2:]
    g_wh = torch.log(g_wh) / variances[1]
    return torch.cat([g_cxcy, g_wh], 1)  # [num_priors,4]

def encode_landm(matched, priors, variances):
    # matched torch.Size([29126, 212])

    matched = torch.reshape(matched, (matched.size(0), 106, 2))

    #print(matched.shape)

    priors_cx = priors[:, 0].unsqueeze(1).expand(matched.size(0), 106).unsqueeze(2)
    priors_cy = priors[:, 1].unsqueeze(1).expand(matched.size(0), 106).unsqueeze(2)
    priors_w = priors[:, 2].unsqueeze(1).expand(matched.size(0), 106).unsqueeze(2)
    priors_h = priors[:, 3].unsqueeze(1).expand(matched.size(0), 106).unsqueeze(2)
    priors = torch.cat([priors_cx, priors_cy, priors_w, priors_h], dim=2)

    # 减去中心后除上宽高
    g_cxcy = matched[:, :, :2] - priors[:, :, :2]
    g_cxcy /= (variances[0] * priors[:, :, 2:])
    g_cxcy = g_cxcy.reshape(g_cxcy.size(0), -1)
    return g_cxcy

def log_sum_exp(x):
    x_max = x.data.max()
    return torch.log(torch.sum(torch.exp(x-x_max), 1, keepdim=True)) + x_max

def match(threshold, truths, priors, variances, labels, landms, loc_t, conf_t, landm_t, idx):
    # 门限值  真实框  先验框  [0.1,0.2] [1] [1,212]
    # loc_t   = torch.Tensor(num, num_priors, 4)
    # landm_t = torch.Tensor(num, num_priors, 212)
    # conf_t  = torch.LongTensor(num, num_priors)

    '''
    print('truth')
    print(truths.shape)
    print(priors.shape)
    print(point_form(priors).shape)
    print()
    '''
    overlaps = jaccard(
        truths,
        point_form(priors)
    )

    #   每一个真实框和先验框的交并比
    #   shape[A,B]

    best_prior_overlap, best_prior_idx = overlaps.max(1, keepdim=True)

    best_prior_idx.squeeze_(1)
    best_prior_overlap.squeeze_(1)

    best_truth_overlap, best_truth_idx = overlaps.max(0, keepdim=True)
    best_truth_idx.squeeze_(0)
    best_truth_overlap.squeeze_(0)

    best_truth_overlap.index_fill_(0, best_prior_idx, 2)

    for j in range(best_prior_idx.size(0)):
        best_truth_idx[best_prior_idx[j]] = j
    # best_truth_idx 长度是先验框的个数  存的是每个先验框对应的iou最大的真实框的索引数

    matches = truths[best_truth_idx]

    # Shape: [num_priors] 此处为每一个anchor对应的label取出来
    conf = labels[best_truth_idx]        
    matches_landm = landms[best_truth_idx]

    conf[best_truth_overlap < threshold] = 0    

    loc = encode(matches, priors, variances)
    landm = encode_landm(matches_landm, priors, variances)

    loc_t[idx] = loc

    conf_t[idx] = conf

    landm_t[idx] = landm


class MultiBoxLoss(nn.Module):
    def __init__(self, num_classes, overlap_thresh, neg_pos, variance, cuda=True):
        super(MultiBoxLoss, self).__init__()

        self.num_classes    = num_classes

        self.threshold      = overlap_thresh

        self.negpos_ratio   = neg_pos
        self.variance       = variance
        self.cuda           = cuda

    def forward(self, predictions, priors, targets):

        loc_data, conf_data, landm_data = predictions

        num         = loc_data.size(0)
        num_priors  = (priors.size(0))

        loc_t   = torch.Tensor(num, num_priors, 4)
        landm_t = torch.Tensor(num, num_priors, 212)
        conf_t  = torch.LongTensor(num, num_priors)

        for idx in range(num):
            # 获得真实框与标签
            truths = targets[idx][:, :4].data
            labels = targets[idx][:, -1].data
            landms = targets[idx][:, 4:216].data


            # 获得先验框
            defaults = priors.data

            match(self.threshold, truths, defaults, self.variance, labels, landms, loc_t, conf_t, landm_t, idx)

        zeros = torch.tensor(0)
        if self.cuda:
            loc_t = loc_t.cuda()
            conf_t = conf_t.cuda()
            landm_t = landm_t.cuda()
            zeros = zeros.cuda()

        pos1 = conf_t > zeros
        pos_idx1 = pos1.unsqueeze(pos1.dim()).expand_as(landm_data)
        landm_p = landm_data[pos_idx1].view(-1, 212)
        landm_t = landm_t[pos_idx1].view(-1, 212)
        loss_landm = F.smooth_l1_loss(landm_p, landm_t, reduction='sum')
        
        pos = conf_t != zeros
        pos_idx = pos.unsqueeze(pos.dim()).expand_as(loc_data)
        loc_p = loc_data[pos_idx].view(-1, 4)
        loc_t = loc_t[pos_idx].view(-1, 4)
        loss_l = F.smooth_l1_loss(loc_p, loc_t, reduction='sum')

        conf_t[pos] = 1
        batch_conf = conf_data.view(-1, self.num_classes)
        # 这个地方是在寻找难分类的先验框
        loss_c = log_sum_exp(batch_conf) - batch_conf.gather(1, conf_t.view(-1, 1))

        # 难分类的先验框不把正样本考虑进去，只考虑难分类的负样本
        loss_c[pos.view(-1, 1)] = 0
        loss_c = loss_c.view(num, -1)

        _, loss_idx = loss_c.sort(1, descending=True)
        _, idx_rank = loss_idx.sort(1)

        num_pos = pos.long().sum(1, keepdim=True)
        # 限制负样本数量
        num_neg = torch.clamp(self.negpos_ratio*num_pos, max=pos.size(1)-1)
        neg = idx_rank < num_neg.expand_as(idx_rank)

        pos_idx = pos.unsqueeze(2).expand_as(conf_data)
        neg_idx = neg.unsqueeze(2).expand_as(conf_data)
        
        # 选取出用于训练的正样本与负样本，计算loss
        conf_p = conf_data[(pos_idx+neg_idx).gt(0)].view(-1,self.num_classes)
        targets_weighted = conf_t[(pos+neg).gt(0)]
        loss_c = F.cross_entropy(conf_p, targets_weighted, reduction='sum')

        N = max(num_pos.data.sum().float(), 1)
        loss_l /= N
        loss_c /= N

        num_pos_landm = pos1.long().sum(1, keepdim=True)
        N1 = max(num_pos_landm.data.sum().float(), 1)
        loss_landm /= N1
        return loss_l, loss_c, loss_landm
