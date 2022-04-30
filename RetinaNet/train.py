#-------------------------------------#
#       对数据集进行训练
#-------------------------------------#
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.optim as optim
from torch.utils.data import DataLoader

from nets.retinanet import retinanet
from nets.retinanet_training import FocalLoss
from utils.callbacks import LossHistory
from utils.dataloader import RetinanetDataset, retinanet_dataset_collate
from utils.utils import get_classes
from utils.utils_fit import fit_one_epoch

if __name__ == "__main__":

    Cuda            = False

    classes_path    = 'model_data/voc_classes.txt'

    model_path      = 'logs/Epoch40-Total_Loss20.3585.pth'

    input_shape     = [600, 600]

    pretrained      = False

    Init_Epoch          = 0
    Freeze_Epoch        = 50
    Freeze_batch_size   = 2
    Freeze_lr           = 1e-4

    UnFreeze_Epoch      = 100
    Unfreeze_batch_size = 2
    Unfreeze_lr         = 1e-5

    Freeze_Train        = True

    num_workers         = 0

    train_annotation_path   = '2007_train.txt'
    val_annotation_path     = '2007_val.txt'

    class_names, num_classes = get_classes(classes_path)

    model = retinanet(num_classes, 1, pretrained)
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

    focal_loss      = FocalLoss()
    loss_history    = LossHistory("logs/")

    with open(train_annotation_path) as f:
        train_lines = f.readlines()
    with open(val_annotation_path) as f:
        val_lines   = f.readlines()
    num_train   = len(train_lines)
    num_val     = len(val_lines)

    if True:
        batch_size  = Freeze_batch_size
        lr          = Freeze_lr
        start_epoch = Init_Epoch
        end_epoch   = Freeze_Epoch
                        
        epoch_step      = num_train // batch_size
        epoch_step_val  = num_val // batch_size
        
        if epoch_step == 0 or epoch_step_val == 0:
            raise ValueError("数据集过小，无法进行训练，请扩充数据集。")
        
        optimizer       = optim.Adam(model_train.parameters(), lr)
        lr_scheduler    = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.96)

        train_dataset   = RetinanetDataset(train_lines, input_shape, num_classes, train = True)
        val_dataset     = RetinanetDataset(val_lines, input_shape, num_classes, train = False)
        gen             = DataLoader(train_dataset, shuffle = True, batch_size = batch_size, num_workers = num_workers, pin_memory=True,
                                    drop_last=True, collate_fn=retinanet_dataset_collate)
        gen_val         = DataLoader(val_dataset  , shuffle = True, batch_size = batch_size, num_workers = num_workers, pin_memory=True, 
                                    drop_last=True, collate_fn=retinanet_dataset_collate)

        #------------------------------------#
        #   冻结一定部分训练
        #------------------------------------#
        if Freeze_Train:
            for param in model.backbone_net.parameters():
                param.requires_grad = False
                
        for epoch in range(start_epoch, end_epoch):
            fit_one_epoch(model_train, model, focal_loss, loss_history, optimizer, epoch, 
                    epoch_step, epoch_step_val, gen, gen_val, end_epoch, Cuda)
            lr_scheduler.step()
            
    if True:
        batch_size  = Unfreeze_batch_size
        lr          = Unfreeze_lr
        start_epoch = Freeze_Epoch
        end_epoch   = UnFreeze_Epoch
                        
        epoch_step      = num_train // batch_size
        epoch_step_val  = num_val // batch_size
        
        if epoch_step == 0 or epoch_step_val == 0:
            raise ValueError("数据集过小，无法进行训练，请扩充数据集。")
        
        optimizer       = optim.Adam(model_train.parameters(), lr)
        lr_scheduler    = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.96)

        train_dataset   = RetinanetDataset(train_lines, input_shape, num_classes, train = True)
        val_dataset     = RetinanetDataset(val_lines, input_shape, num_classes, train = False)
        gen             = DataLoader(train_dataset, shuffle = True, batch_size = batch_size, num_workers = num_workers, pin_memory=True,
                                    drop_last=True, collate_fn=retinanet_dataset_collate)
        gen_val         = DataLoader(val_dataset  , shuffle = True, batch_size = batch_size, num_workers = num_workers, pin_memory=True, 
                                    drop_last=True, collate_fn=retinanet_dataset_collate)

        if Freeze_Train:
            for param in model.backbone_net.parameters():
                param.requires_grad = True
                
        for epoch in range(start_epoch, end_epoch):
            fit_one_epoch(model_train, model, focal_loss, loss_history, optimizer, epoch, 
                    epoch_step, epoch_step_val, gen, gen_val, end_epoch, Cuda)
            lr_scheduler.step()
