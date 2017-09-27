# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
	return render(request, 'index.html', {})
	

from InstagramAPI import InstagramAPI
import sys
import operator
from django.views.decorators.csrf import csrf_exempt
import credentials
@csrf_exempt
def getFollowingSuggestion(request):
	if(request.method == "GET"):
		values = request.GET
		username = values.get("username")
		enteredUsername = username + ""

		# For Python 3+
		if sys.version[0]>="3":
			raw_input=input

		API = InstagramAPI(credentials.username, credentials.password)
		API.login()
		print "logged in"

		API.searchUsername(username)
		user = API.LastJson.get("user")
		print user 
		print "\n"
		if(user is None):
			print "username does not exist"
			return JsonResponse({"error":True})
			
		numFollowing = user.get("following_count")
		if(numFollowing==0):
			print "user has 0 followings"
			return JsonResponse({"error":True})
			
		userId = user.get("pk")
		API.getUserFollowings(userId);
		followings = API.LastJson.get("users")
		alreadyFollowing = {username:True}

		# Store previous followings usernames
		for user in range(len(followings)):
			user = followings[user]
			username = user.get("username")
			alreadyFollowing[username]=True

		# Analyze followings of the user's most recent followings 
		visitedUsers = {}
		numCompleted=0
		for i in range(0, min(len(followings), 30)):
			next_max_id = True
			while next_max_id:
				user = followings[i]
				uid = user.get("pk")
				username = user.get("username")
				print "getting followings for userid " + str(uid)
				#first iteration hack
				if next_max_id == True: next_max_id=''
				_ = API.getUserFollowings(uid, maxid=next_max_id)
				#following = API.getTotalFollowings(userids[index])
				users = API.LastJson.get('users',[])
				#print users
				if(users):
					for user in users:
						username = user["username"]
						# Update visited usernames dictionary
						if(visitedUsers.get(username) is not None):
							freq = visitedUsers[username]
							freq+=1
							visitedUsers[username] = freq
						else:
							visitedUsers[username] = 1
						numCompleted+=1
				next_max_id = API.LastJson.get('next_max_id','')
		print str(numCompleted) + " followings analyzed"
		sortedSuggestions = sorted(visitedUsers.items(), key=operator.itemgetter(1), reverse=True)

		uniqueSuggestions=[]
		for i in range(len(sortedSuggestions)):
			tuple = sortedSuggestions[i]
			key = tuple[0]
			value = tuple[1]
			if(alreadyFollowing.get(key) is None):
				uniqueSuggestions.append((key,value))

		top3Suggestions=[]
		for j in range(0, min(3, len(uniqueSuggestions))):
			print uniqueSuggestions[j]
			top3Suggestions.append(uniqueSuggestions[j])
			
		return JsonResponse({"numAnalyzed":numCompleted, 
				"enteredUsername":enteredUsername,
				"suggestions":top3Suggestions})
		