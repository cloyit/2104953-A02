import torch
import torch.nn as nn

def calc_iou(a, b):
    area = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    iw = torch.min(torch.unsqueeze(a[:, 3], dim=1), b[:, 2]) - torch.max(torch.unsqueeze(a[:, 1], 1), b[:, 0])
    ih = torch.min(torch.unsqueeze(a[:, 2], dim=1), b[:, 3]) - torch.max(torch.unsqueeze(a[:, 0], 1), b[:, 1])
    iw = torch.clamp(iw, min=0)
    ih = torch.clamp(ih, min=0)
    ua = torch.unsqueeze((a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1]), dim=1) + area - iw * ih
    ua = torch.clamp(ua, min=1e-8)
    intersection = iw * ih
    IoU = intersection / ua

    return IoU

def get_target(anchor, bbox_annotation, classification, cuda):

    print('get_target')

    IoU = calc_iou(anchor[:, :], bbox_annotation[:, :4])

    IoU_max, IoU_argmax = torch.max(IoU, dim=1)
    # class [anchors,20]
    targets = torch.ones_like(classification) * -1
    print(targets.shape)
    if cuda:
        targets = targets.cuda()

    targets[torch.lt(IoU_max, 0.4), :] = 0

    positive_indices = torch.ge(IoU_max, 0.5)

    print(positive_indices.shape)

    assigned_annotations = bbox_annotation[IoU_argmax, :]
    print(assigned_annotations.shape)

    targets[positive_indices, :] = 0
    targets[positive_indices, assigned_annotations[positive_indices, 4].long()] = 1
    #Iou大于0.5的先验框的对应种类置1，其他种类是0, 0.4-0.5之间的是-1

    num_positive_anchors = positive_indices.sum()
    return targets, num_positive_anchors, positive_indices, assigned_annotations

def encode_bbox(assigned_annotations, positive_indices, anchor_widths, anchor_heights, anchor_ctr_x, anchor_ctr_y):

    assigned_annotations = assigned_annotations[positive_indices, :]
    print('encode_bbox')
    print(assigned_annotations.shape)
    # torch.Size([32, 5])  筛选之后的

    anchor_widths_pi = anchor_widths[positive_indices]
    anchor_heights_pi = anchor_heights[positive_indices]
    anchor_ctr_x_pi = anchor_ctr_x[positive_indices]
    anchor_ctr_y_pi = anchor_ctr_y[positive_indices]

    print(anchor_ctr_x_pi.shape)

    gt_widths = assigned_annotations[:, 2] - assigned_annotations[:, 0]
    gt_heights = assigned_annotations[:, 3] - assigned_annotations[:, 1]
    gt_ctr_x = assigned_annotations[:, 0] + 0.5 * gt_widths
    gt_ctr_y = assigned_annotations[:, 1] + 0.5 * gt_heights

    gt_widths = torch.clamp(gt_widths, min=1)
    gt_heights = torch.clamp(gt_heights, min=1)

    targets_dx = (gt_ctr_x - anchor_ctr_x_pi) / anchor_widths_pi
    targets_dy = (gt_ctr_y - anchor_ctr_y_pi) / anchor_heights_pi
    targets_dw = torch.log(gt_widths / anchor_widths_pi)
    targets_dh = torch.log(gt_heights / anchor_heights_pi)

    targets = torch.stack((targets_dy, targets_dx, targets_dh, targets_dw))
    print(targets.shape)
    targets = targets.t()
    print(targets.shape)
    return targets

class FocalLoss(nn.Module):
    def __init__(self):
        super(FocalLoss, self).__init__()

    def forward(self, classifications, regressions, anchors, landmarks, annotations, alpha = 0.25, gamma = 2.0, cuda = True):

        batch_size = classifications.shape[0]

        dtype = regressions.dtype
        anchor = anchors[0, :, :].to(dtype)

        anchor_widths = anchor[:, 3] - anchor[:, 1]
        anchor_heights = anchor[:, 2] - anchor[:, 0]
        anchor_ctr_x = anchor[:, 1] + 0.5 * anchor_widths
        anchor_ctr_y = anchor[:, 0] + 0.5 * anchor_heights

        regression_losses = []
        classification_losses = []
        landmarks_losses = []
        for j in range(batch_size):


            bbox_annotation = annotations[j]
            classification = classifications[j, :, :]
            regression = regressions[j, :, :]
            landmark = landmarks[j,:,:]

            print(bbox_annotation.shape)
            print(classification.shape)
            print(regression.shape)
            print(landmark.shape)

            classification = torch.clamp(classification, 1e-4, 1.0 - 1e-4)
            
            if len(bbox_annotation) == 0:

                alpha_factor = torch.ones_like(classification) * alpha
                if cuda:
                    alpha_factor = alpha_factor.cuda()
                alpha_factor = 1. - alpha_factor
                focal_weight = classification
                focal_weight = alpha_factor * torch.pow(focal_weight, gamma)

                bce = - (torch.log(1.0 - classification))
                
                cls_loss = focal_weight * bce
                
                classification_losses.append(cls_loss.sum())

                if cuda:
                    regression_losses.append(torch.tensor(0).to(dtype).cuda())
                    landmarks_losses.append(torch.tensor(0).to(dtype).cuda())
                else:
                    regression_losses.append(torch.tensor(0).to(dtype))
                    landmarks_losses.append(torch.tensor(0).to(dtype))
                    
                continue

            #在进行编码的时候，我们需要找到每一个真实框对应的先验框，我们把和真实框重合程度在0.5以上的作为正样本，在0.4以下的作为负样本，在0.4和0.5之间的作为忽略样本。
            targets, num_positive_anchors, positive_indices, assigned_annotations = \
                get_target(anchor, bbox_annotation, classification, cuda)

            alpha_factor = torch.ones_like(targets) * alpha
            if cuda:
                alpha_factor = alpha_factor.cuda()

            alpha_factor = torch.where(torch.eq(targets, 1.), alpha_factor, 1. - alpha_factor)
            focal_weight = torch.where(torch.eq(targets, 1.), 1. - classification, classification)
            focal_weight = alpha_factor * torch.pow(focal_weight, gamma)

            bce = - (targets * torch.log(classification) + (1.0 - targets) * torch.log(1.0 - classification))
            cls_loss = focal_weight * bce

            zeros = torch.zeros_like(cls_loss)
            if cuda:
                zeros = zeros.cuda()
            cls_loss = torch.where(torch.ne(targets, -1.0), cls_loss, zeros)

            classification_losses.append(cls_loss.sum() / torch.clamp(num_positive_anchors.to(dtype), min=1.0))

            if positive_indices.sum() > 0:
                # assigned_annotations torch.Size([67995, 5])
                # assigned_annotations = bbox_annotation[IoU_argmax, :]
                # 把iou最大的对应的真实框参数对照着填进去
                # positive_indices torch.Size([67995])  iou大于0.5的地方为true
                targets = encode_bbox(assigned_annotations, positive_indices, anchor_widths, anchor_heights, anchor_ctr_x, anchor_ctr_y)

                regression_diff = torch.abs(targets - regression[positive_indices, :])
                regression_loss = torch.where(
                    torch.le(regression_diff, 1.0 / 9.0),
                    0.5 * 9.0 * torch.pow(regression_diff, 2),
                    regression_diff - 0.5 / 9.0
                )
                regression_losses.append(regression_loss.mean())
            else:
                if cuda:
                    regression_losses.append(torch.tensor(0).to(dtype).cuda())
                else:
                    regression_losses.append(torch.tensor(0).to(dtype))

        c_loss = torch.stack(classification_losses).mean()
        r_loss = torch.stack(regression_losses).mean()
        loss = c_loss + r_loss
        return loss, c_loss, r_loss
