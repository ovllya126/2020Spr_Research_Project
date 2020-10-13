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
import time
import csv
import pickle
import operator
import datetime
import os
import sys
import torch
from torch import nn
from torch.nn import Module, Parameter
import torch.nn.functional as F

from .utils import build_graph, Data, split_validation
from .model import *



def get_recommends(session_list):
    
    #preprocess user's session list
    session_list = preprocess(session_list)
    
    #process the list to sequense
    tra = Data(session_list, shuffle=True)
    
    #get the model from saved file
    net = torch.load('./model_saved.pth')
    net.eval()

    slices = tra.generate_batch(net.batch_size)
    for i in slices:
        targets, scores = forward(net, i, tra)
        break

    #get recommenders
    sub_scores = scores.topk(20)[1]
    sub_scores = trans_to_cpu(sub_scores).detach().numpy()
    
    topscores = sub_scores[-1][0:5]

    #recover the initial course id according to item dictionary saved previously
    with open('./recommender/datasets/item_dict.pkl', 'rb') as f:
        item_dict =  pickle.load(f)

    result = []
    for score in topscores:
        for key in item_dict:
            if item_dict[key] == score:
                result.append(key)
                break

    return result


def preprocess(prolist):
    sess_clicks = {}
    sess_date = {}
    ctr = 0
    curid = -1
    curdate = None
    for data in prolist:
        sessid = data['session_id_id']
        if curdate and not curid == sessid:
            date = ''
            if opt.dataset == 'yoochoose':
                date = time.mktime(time.strptime(curdate[:19], '%Y-%m-%dT%H:%M:%S'))
            else:
                date = time.mktime(time.strptime(curdate, '%Y-%m-%d'))
            sess_date[curid] = date
        curid = sessid
        
        item = data['course_id']
        
        curdate = ''
        
        curdate = data['timestamp']
        
        if sessid in sess_clicks:
            sess_clicks[sessid] += [item]
        else:
            sess_clicks[sessid] = [item]
        ctr += 1
    date = ''
    
    date = time.mktime(time.strptime(curdate[:19], '%Y-%m-%dT%H:%M:%S'))
    
    sess_date[curid] = date

    

    splitdate = 0
    dates = list(sess_date.items())
    tra_sess = filter(lambda x: x[1] > splitdate, dates)
    tra_sess = sorted(tra_sess, key=operator.itemgetter(1)) 

    tra_ids, tra_dates, tra_seqs = obtian_tra(tra_sess,sess_clicks)
    tr_seqs, tr_dates, tr_labs, tr_ids = process_seqs(tra_seqs, tra_dates)
    tra = (tr_seqs, tr_labs)
    return tra


def obtian_tra(tra_sess,sess_clicks):
    item_dict = {}
    train_ids = []
    train_seqs = []
    train_dates = []
    item_ctr = 1
    for s, date in tra_sess:
        seq = sess_clicks[s]
        outseq = []
        for i in seq:
            if i in item_dict:
                outseq += [item_dict[i]]
            else:
                outseq += [item_ctr]
                item_dict[i] = item_ctr
                item_ctr += 1
        if len(outseq) < 2:  # Doesn't occur
            continue
        train_ids += [s]
        train_dates += [date]
        train_seqs += [outseq]
    #print(item_ctr)     # 43098, 37484
    return train_ids, train_dates, train_seqs

def process_seqs(iseqs, idates):
    out_seqs = []
    out_dates = []
    labs = []
    ids = []
    for id, seq, date in zip(range(len(iseqs)), iseqs, idates):
        for i in range(1, len(seq)):
            tar = seq[-i]
            labs += [tar]
            out_seqs += [seq[:-i]]
            out_dates += [date]
            ids += [id]
    return out_seqs, out_dates, labs, ids




if __name__ == '__main__':
    main()



