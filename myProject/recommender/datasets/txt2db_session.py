#!/usr/bin/env python
#coding:utf-8
 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myProject.settings")
 
'''
When the version of Django more than 1.7, the following two statement should be added.

import django
django.setup()

Otherwise, there may be errors-- django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

 
import django
if django.VERSION >= (1, 7):  #recognize the version of django automatically
    django.setup()
 
 
def main():

    from recommender.models import Session,User
    
    f = open('test.dat')
    SessionList = []
    for line in f:
        session_id,timestamp,course_id,category = line.split(',')
        user = User(user_id= session_id)
        user.save()
        session = Session(timestamp=timestamp, course_id=course_id , category=category)
        session.session_id = user
        session.save()
    f.close()

 
if __name__ == "__main__":
    main()
    print('Done!')
