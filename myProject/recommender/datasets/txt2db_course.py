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
if django.VERSION >= (1, 7): #recognize the version of django automatically
    django.setup()
 
 
def main():

    from recommender.models import Course
    
    f = open('courses.txt')
    CourseList = []
    for line in f:
        course_id,category = line.split(',')
        
        course = Course(cour_id=course_id , cour_cate=category)
        
        course.save()
    f.close()


 
if __name__ == "__main__":
    main()
    print('Done!')
