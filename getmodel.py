#!/usr/bin/env python36
# -*- coding: utf-8 -*-

"""
@inproceedings{Wu:2019ke,
title = {{Session-based Recommendation with Graph Neural Networks}},
author = {Wu, Shu and Tang, Yuyuan and Zhu, Yanqiao and Wang, Liang and Xie, Xing and Tan, Tieniu},
year = 2019,
booktitle = {Proceedings of the Twenty-Third AAAI Conference on Artificial Intelligence},
location = {Honolulu, HI, USA},
month = jul,
volume = 33,
number = 1,
series = {AAAI '19},
pages = {346--353},
url = {https://aaai.org/ojs/index.php/AAAI/article/view/3804},
doi = {10.1609/aaai.v33i01.3301346},
editor = {Pascal Van Hentenryck and Zhi-Hua Zhou},
}
"""

import argparse
import pickle
import sys
import torch

from recommender.utils import Data, split_validation
from recommender.model import *

def getopt():
    sys.argv = ['']
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='yoochoose1_64', help='dataset name: diginetica/yoochoose1_4/yoochoose1_64/sample')
    parser.add_argument('--batchSize', type=int, default=100, help='input batch size')
    parser.add_argument('--hiddenSize', type=int, default=100, help='hidden state size')
    parser.add_argument('--epoch', type=int, default=30, help='the number of epochs to train for')
    parser.add_argument('--lr', type=float, default=0.001, help='learning rate')  # [0.001, 0.0005, 0.0001]
    parser.add_argument('--lr_dc', type=float, default=0.1, help='learning rate decay rate')
    parser.add_argument('--lr_dc_step', type=int, default=3, help='the number of steps after which the learning rate decay')
    parser.add_argument('--l2', type=float, default=1e-5, help='l2 penalty')  # [0.001, 0.0005, 0.0001, 0.00005, 0.00001]
    parser.add_argument('--step', type=int, default=1, help='gnn propogation steps')
    parser.add_argument('--patience', type=int, default=10, help='the number of epoch to wait before early stop ')
    parser.add_argument('--nonhybrid', action='store_true', help='only use the global preference to predict')
    parser.add_argument('--validation', action='store_true', help='validation')
    parser.add_argument('--valid_portion', type=float, default=0.1, help='split the portion of training set as validation set')
    opt = parser.parse_args()
    return opt


def main():
    opt = getopt()

    #load data from file
    train_data = pickle.load(open('./recommender/datasets/yoochoose1_64/train.txt', 'rb'))
    if opt.validation:
        train_data, valid_data = split_validation(train_data, opt.valid_portion)
        test_data = valid_data
    else:
        test_data = pickle.load(open('./recommender/datasets/yoochoose1_64/test.txt', 'rb'))
    
    #process data 
    train_data = Data(train_data, shuffle=True)
    test_data = Data(test_data, shuffle=False)
    
    #get node num
    if opt.dataset == 'diginetica':
        n_node = 43098
    elif opt.dataset == 'yoochoose1_64' or opt.dataset == 'yoochoose1_4':
        n_node = 37484
    else:
        n_node = 310

    #get model
    model = trans_to_cuda(SessionGraph(opt, n_node))

    #train model
    model.scheduler.step()
    model.train()

    #save model
    torch.save(model, ('./model_saved.pth'))


if __name__ == '__main__':
    main()



