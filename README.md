# 2020Spring 32933 Research_Project
## E-Learning Recommender System Based on Deep Learning
This is for 32933 research project in UTS. 
Group members are Jinyan Dong, Shaojie Miao, Liangliang gu.
Supervised by Professor Guangquan Zhang and PhD Qian Zhang.

##Reference

The SR-GNN models are referenced by  https://github.com/CRIPAC-DIG/SR-GNN

```
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
```

##Get Start

In shell
```
$ git clone https://github.com/ovllya126/2020Spr_Research_Project.git
```
After download
```
$ cd myProject/
$ pip install -r requirements.txt
```
After installation
```
$ python manage.py migrate
$ python manage.py runserver
```
In local web browser, use url 'http://127.0.0.1:8000/recommender/' to visit the home page of our project.

