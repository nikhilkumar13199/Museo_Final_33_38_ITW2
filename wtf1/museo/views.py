# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# from django.contrib.comments import Comment
# Create your views here.

def index(request):
	cursor=connection.cursor()
	args={}
	cursor.execute('''select * from movies_list''')#this spits out the entire movies_list table
	row=cursor.fetchall()
	print('ROW:',row)# used for debugging 
	args['row']=row
	return render(request,'museo/index.html',args)

def register(request):
	if request.method=='POST':
		form=UserCreationForm(request.POST) 
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password2']
			user=authenticate(username=username ,password=password) #authenticate the user with the typed in details
			login(request,user)
			return redirect('/museo/index')
	else:
		form=UserCreationForm() #to use the inbuit django create new user form
	context={'form':form}
	return render(request,'museo/sign_up.html',context)

def feed(request):
	cursor=connection.cursor()
	args={}
	username=""
	userid=-1
	if request.user.is_authenticated:
		username=request.user.username #stores the logged in username
		userid=request.user.id #stores the logged in userid
	
	pidx=0
	pids=request.POST.get('upvote') #gets the post id of the post along with which the clicked radio button is present
	puds=request.POST.get('downvote') #gets the post id of corresponding post of clicked downvote radio button

	if pids!=None:
		pidx=int(pids)
	
	
	#if the current user id and post id is present in user_upvote table, it is already upvoted
	#if the current user id and post id is present in user_downvote table, it is already downvoted
	if pidx!=0:

		cursor.execute('''select * from user_upvote where user_id=%s and post_upvoted=%s;''',[userid,pidx])
		row2=cursor.fetchall()
		cursor.execute('''select * from user_downvote where user_id=%s and post_downvoted=%s;''',[userid,pidx])
		row3=cursor.fetchall()
		if len(row2)>0 or len(row3)>0:
			messages.warning(request,"This post is already upvoted/downvoted by you")
			print(1)
		else:
			cursor.execute('''insert into user_upvote set user_id=%s,post_upvoted=%s;''',[userid,pidx]) #if post is niether upvoted nor downvoted insert the post id of upvoted post and user id of user upvoting the post
	if puds!=None:
		cursor.execute('''select * from user_downvote where user_id=%s and post_downvoted=%s;''',[userid,puds])
		row2=cursor.fetchall()
		cursor.execute('''select * from user_upvote where user_id=%s and post_upvoted=%s;''',[userid,puds])
		row3=cursor.fetchall()
		print("fck")
		print(row3)
		if len(row2)>0 or len(row3)>0:
			messages.warning(request,"This post is already upvoted/downvoted by you") #if post is already upvoted/downvoted generate this warning message
			print(2)
		else:
			cursor.execute('''insert into user_downvote set user_id=%s,post_downvoted=%s''',[userid,puds]) #if post is niether upvoted nor downvoted insert the post id of downvoted post and user id of user downvoting the post
	
	cursor.execute('''select post_list.pid,post_list.uid,user_list.Name,post_list.content,post_list.upvotes,post_list.downvotes from post_list,user_list where post_list.uid=user_list.uid order by post_list.pid desc;''')
	row=cursor.fetchall()
	args['row']=row

	#used for debugging
	cursor.execute('''select post_upvoted from user_upvote where user_id=%s;''',[userid])
	upvoted_posts=cursor.fetchall()
	args['upvoted_posts']=upvoted_posts
	#used for debugging

	return render(request,'museo/feed.html',args)

def createpost(request):
	cursor=connection.cursor()
	args={}
	content=str(request.POST.get('content')) #get the content typed in the content field
	print(content)
	if content=="None" or content=="": #if content is not typed in and published button is clicked, do not publish an empty string
		print(2)
		print(content)
	else:
		
		cursor.execute('''insert into post_list(uid,upvotes,downvotes,content) values(%s,0,0,%s);''',[request.user.id,content])
		 # if content is a non empty string insert the details in the post_list
		print(2)

	return render(request,'museo/createpost.html',args)

def topusers(request):
	cursor=connection.cursor()
	args={}
	cursor.execute('''select * from upvotes_by_id left outer join user_list on upvotes_by_id.uid=user_list.uid;''')
	#upvotes_by_id is a sorted table descending order by total upvotes-total downvotes storing uid,total upvotes and total downvotes
	#this query gives sorted table with descending order by total upvotes-total downvotes along with the usernames
	row=cursor.fetchall()
	print('ROW:',row)
	args['row']=row
	return render(request,'museo/topusers.html',args)

def profile(request):
	cursor=connection.cursor()
	if request.user.is_authenticated:
		userid=request.user.id
		username=request.user.username
		cursor.execute('''select pid,upvotes,downvotes,content from post_list where uid=%s''',[userid])
		row=cursor.fetchall()
		cursor.execute('''select sum(upvotes) from post_list where uid=%s''',[userid])
		upvotes=cursor.fetchall()
		cursor.execute('''select sum(downvotes) from post_list where uid=%s''',[userid])
		downvotes=cursor.fetchall()
		args={'row':row}
		args['upv']=upvotes #counted total upvotes for logged in user
		args['dow']=downvotes #counted total downvotes for logged in user
	else:
		args={}
		return render(request,'museo/profile.html',args)

	return render(request,'museo/profile.html',args)

def index2(request):
	args={}
	return render(request,'museo/index2.html',args)

