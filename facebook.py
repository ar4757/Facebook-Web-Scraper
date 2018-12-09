#facebook login
import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import re
import pygame
import mutagen.mp3
from tkinter import *

def listFriends(e, p, friendName):
	url='http://www.facebook.com'

	headers={'User-Agent':'Mozilla/5.0'}

	r=requests.get(url)

	soup=bs(r.text,'html.parser')

	ft='login_form'

	form=soup.find('form',{'id':'login_form'})


	inputs=form.find_all('input')

	load={}

	for i in inputs:
	    load[i.get('name')]=i.get('value')

	load['email']=e
	load['pass']=p
	s=HTMLSession()
	r=s.post(form.get('action'),data=load,headers=headers,cookies=r.cookies)
	print(r.url) #to verify login

	if len(friendName) == 0:
		username = re.search("https:\/\/www\.facebook\.com\/(.*?)\/friends", r.text).group(1) #viewing your own friends
	else:
		username = friendName #viewing someone else's friends
	
	initialFriendsLink = "https://m.facebook.com/" + username + "/friends?ft_ref=flsa"
	r = s.get(initialFriendsLink,headers=headers)
	currentText = r.text
	numFriends = int(re.search("Friends \((.*?)\)", currentText).group(1))

	allnames = []
	allusernames = []
	iterations = numFriends / 37 + 1
	i = 0
	while i < iterations:
		currentText = r.text
		#print(currentText)
		entries = re.findall("alt\=\"(.*?)\"", currentText)
		usernames = re.findall("class\=\"bp\" href=\"\/(.*?)\?", currentText)
		#print(entries)
		#print(len(entries))
		for entry in entries:
			if entry == "Facebook logo":
				pass
			else:
				#print(entry)
				allnames.append(entry)
		for user in usernames:
			if user == "friends/hovercard/mbasic/":
				pass
			else:
				#print(user)
				allusernames.append(user)
		i += 1
		try:
			regexText = re.escape(username) + "\/friends(.*?)\;"
			seeMoreFriendsLink = re.search(regexText, currentText)
			#print(seeMoreFriendsLink)
			nextLink = seeMoreFriendsLink.group(1)
			#print(nextLink)
			nextFriendsLink = "https://m.facebook.com/" + username +"/friends" + nextLink
			r = s.get(nextFriendsLink,headers=headers)
		except:
			break
	allnames = list(set(allnames))
	allnames.sort()
	for name in allnames:
		print(name)
	for user in allusernames:
		print(user)
	#fmt = '{:<8}{:<20}{}'

	#print(fmt.format('', 'Name', 'Username'))
	#for i, (name, user) in enumerate(zip(allnames, allusernames)):
    #		print(fmt.format(i, name, user))

	print("Total number of friends: " + str(numFriends))
	print("Number of friends fetched: " + str(len(allnames)))
	print("Why in the world are " + str(numFriends - len(allnames)) + " friends missing???")
	s.close()
	exit()

try:
	song_name = ""
	pygame.mixer.init(frequency=mutagen.mp3.MP3(song_name).info.sample_rate)
	pygame.mixer.music.load(song_name)
	pygame.mixer.music.play()
except:
	pass

master = Tk()
master.update_idletasks()
width = master.winfo_width() + 250
height = master.winfo_height()
x = (master.winfo_screenwidth() // 2) - (width // 2)
y = (master.winfo_screenheight() // 2) - (height // 2)
master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
master.title("Facebook Friends")
Label(master, text="Email").grid(row=0)
Label(master, text="Password").grid(row=1)
Label(master, text="Username of friend to creep on \n(if left blank, a list of your \nown friends is displayed)").grid(row=2)

e1 = Entry(master)
e2 = Entry(master, show="*")
e3 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

#e=input('enter email')
#e = ""

#p=input('enter password')
#p = ""

submitButton = Button(master, text="Submit", width=10, command=lambda:listFriends(e1.get(), e2.get(), e3.get()))
submitButton.grid(row=3, column=1)

master.mainloop()
