from django.shortcuts import render,redirect

# Create your views here.

from recommender.models import User,Session,Course

from .getrec import get_recommends

def home_page(request):	

	found = False
	usrid = request.session.get('id')

	if request.method == "POST":
		username = request.POST.get("user_name")
		password = request.POST.get("pwd")
		users = User.objects.values('user_id','user_name')

		for user in users:
			if user['user_name'] == username and password == '123':
				found = True
				user_id = user['user_id']
				break

		if found == False:
			error_msg = 'Sorry, your username or password is not correct, please try again.'
			return render(request, 'recommender/home_page.html', {'login_error_msg': error_msg})
		else:
			request.session['id'] = user_id
			return redirect('/recommender/user_center/')

	content = {'found':found, 'userid': usrid }
	return render(request, 'recommender/home_page.html',content)

def user_center(request):
	user_id = request.session.get('id')
	user = User.objects.filter(user_id = user_id).values()
	username = user[0]['user_name']
	userid = user[0]['user_id']
	gender = user[0]['user_gender']
	state = user[0]['user_state']
	email = user[0]['user_email']
	content = {'username':username, 'userid':userid, 'gender':gender, 'state':state, 'email':email}

	sessions = Session.objects.filter(session_id = user_id).values()
	length = len(sessions)
	if(length%5 ==0):
		row_num = length/5
	else:
		row_num = length/5 + 1
	content['row_num'] = row_num
	content['courseids'] = sessions

	recommends_arr = get_recommends(sessions)

	content['recommends_arr'] = recommends_arr

	return render(request, 'recommender/personal_page.html',content) 


def log_out(request):
	request.session['id'] = ''
	return render(request, 'recommender/home_page.html')

def show_courses(request):
	user_id = request.session.get('id')
	content = {'userid':user_id}

	course_0 = Course.objects.filter(cour_cate = '0\n').values('cour_id')[0:101]
	course_1 = Course.objects.filter(cour_cate = '1\n').values('cour_id')[0:101]
	course_2 = Course.objects.filter(cour_cate = '2\n').values('cour_id')[0:101]
	course_3 = Course.objects.filter(cour_cate = '3\n').values('cour_id')[0:101]
	course_4 = Course.objects.filter(cour_cate = '4\n').values('cour_id')[0:101]
	course_5 = Course.objects.filter(cour_cate = '5\n').values('cour_id')[0:101]
	course_6 = Course.objects.filter(cour_cate = '6\n').values('cour_id')[0:101]
	course_7 = Course.objects.filter(cour_cate = '7\n').values('cour_id')[0:101]
	course_8 = Course.objects.filter(cour_cate = '8\n').values('cour_id')[0:101]
	course_9 = Course.objects.filter(cour_cate = '9\n').values('cour_id')[0:101]
	content['course_0'] = course_0
	content['course_1'] = course_1
	content['course_2'] = course_2
	content['course_3'] = course_3
	content['course_4'] = course_4
	content['course_5'] = course_5
	content['course_6'] = course_6
	content['course_7'] = course_7
	content['course_8'] = course_8
	content['course_9'] = course_9
	
	return render(request, 'recommender/course.html',content) 


