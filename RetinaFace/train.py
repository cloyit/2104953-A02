import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.optim as optim
from torch.utils.data import DataLoader

from nets.retinaface import RetinaFace
from nets.retinaface_training import MultiBoxLoss, weights_init
from utils.anchors import Anchors
from utils.callbacks import LossHistory
from utils.config import cfg_mnet, cfg_re50
from utils.dataloader import DataGenerator, detection_collate
from utils.utils_fit import fit_one_epoch

if __name__ == "__main__":
    Cuda = True

    training_dataset_path = './data/widerface/train/label.txt'

    backbone    = "resnet50"

    pretrained  = False

    model_path  = "model_data/Retinaface_resnet50.pth"

    Freeze_Train = True

    num_workers = 0

    if backbone == "mobilenet":
        cfg = cfg_mnet
    elif backbone == "resnet50":  
        cfg = cfg_re50
    else:
        raise ValueError('Unsupported backbone - `{}`, Use mobilenet, resnet50.'.format(backbone))

    model = RetinaFace(cfg = cfg, pretrained = pretrained)
    if not pretrained:
        weights_init(model)
    if model_path != '':
        print('Load weights {}.'.format(model_path))
        device          = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_dict      = model.state_dict()
        pretrained_dict = torch.load(model_path, map_location = device)
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if np.shape(model_dict[k]) == np.shape(v)}
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)

    model_train = model.train()
    if Cuda:
        model_train = torch.nn.DataParallel(model)
        cudnn.benchmark = True
        model_train = model_train.cuda()

    anchors = Anchors(cfg, image_size = (cfg['train_image_size'], cfg['train_image_size'])).get_anchors()
    if Cuda:
        anchors = anchors.cuda()

    criterion       = MultiBoxLoss(2, 0.35, 7, cfg['variance'], Cuda)
    # 第一个参数是分类数  0.35是得分门限  7是正负样本的比例
    loss_history    = LossHistory("logs/")

    if True:

        lr              = 1e-3
        Batch_size      = 4
        Init_Epoch      = 0
        Freeze_Epoch    = 1
        
        optimizer       = optim.Adam(model_train.parameters(), lr, weight_decay = 5e-4)
        lr_scheduler    = optim.lr_scheduler.StepLR(optimizer, step_size = 1, gamma = 0.92)

        train_dataset   = DataGenerator(training_dataset_path, cfg['train_image_size'])
        gen             = DataLoader(train_dataset, shuffle=True, batch_size=Batch_size, num_workers=num_workers, pin_memory=True,
                                drop_last=True, collate_fn=detection_collate)

        epoch_step      = train_dataset.get_len() // Batch_size

        if Freeze_Train:
            for param in model.body.parameters():
                param.requires_grad = False

        for epoch in range(Init_Epoch, Freeze_Epoch):
            # 训练模型  模型  loss  选择器  multiboxloss  epoch  每个epoch中的batchsize  dataloader  冻结的epoch数  先验框  权重  cuda
            fit_one_epoch(model_train, model, loss_history, optimizer, criterion, epoch, epoch_step, gen, Freeze_Epoch, anchors, cfg, Cuda)
            lr_scheduler.step()

    if True:

        lr              = 1e-4
        Batch_size      = 2
        Freeze_Epoch    = 1
        Unfreeze_Epoch  = 10

        optimizer       = optim.Adam(model_train.parameters(), lr, weight_decay = 5e-4)
        lr_scheduler    = optim.lr_scheduler.StepLR(optimizer, step_size = 1, gamma = 0.92)

        train_dataset   = DataGenerator(training_dataset_path, cfg['train_image_size'])
        gen             = DataLoader(train_dataset, shuffle=True, batch_size=Batch_size, num_workers=num_workers, pin_memory=True,
                                drop_last=True, collate_fn=detection_collate)

        epoch_step      = train_dataset.get_len() // Batch_size

        if Freeze_Train:
            for param in model.body.parameters():
                param.requires_grad = True

        for epoch in range(Freeze_Epoch,Unfreeze_Epoch):
            fit_one_epoch(model_train, model, loss_history, optimizer, criterion, epoch, epoch_step, gen, Unfreeze_Epoch, anchors, cfg, Cuda)
            lr_scheduler.step()
