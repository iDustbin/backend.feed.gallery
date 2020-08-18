# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
from instaloader import *
from os import walk
import fnmatch
import os.path
import socket
import requests
from instaloader import Instaloader, Post, Profile, load_structure_from_file
from datetime import datetime
from itertools import dropwhile, takewhile
from io import BytesIO
from requests import get
#from PIL import Image, ImageDraw
from instaloader import *


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['JSON_SORT_KEYS'] = True
app.config['STATIC_FOLDER'] = 'static'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api/instagram/userinfo', methods=['GET', 'POST'])
def instagram_info():
    L = instaloader.Instaloader( compress_json=False )
   
    USER = 'idustbin'
    PASSWORD = 'EpRkyTLvC2QzaWyda^]'
    L.load_session_from_file(USER)

   
    print(request.get_json())
    PROFILE = request.get_json()
 
    response_object = {'status': 'success'}
    profile = instaloader.Profile.from_username(L.context, request.get_json()['profile'].lower())

    #L.login(USER, PASSWORD)
    #print("************")
    #return jsonify({})

    #likes = set()
    #print('Fetching likes of all posts of profile {}.'.format(profile.username))
    #likes = set(profile.get_likes())
    
    print('Fetching followers of profile {}.'.format(profile.username))
    followers = set(profile.get_followers())
    
    #context = { 
    #    'posts': get_likes(),
    #    'profile': profile,
    #}
    #print (followers)

    #return render(request, 'index.html', context)

@app.route('/api/instagram/download', methods=['post'])
def instagram_profile_download():

    L = instaloader.Instaloader( compress_json=False )

    USER = 'idustbin'

    PASSWORD = 'EpRkyTLvC2QzaWyda^]'

    #L.login(USER, PASSWORD)
    L.load_session_from_file(USER)

   
    print(request.get_json())
    PROFILE = request.get_json()
 
    response_object = {'status': 'success'}
    profile = instaloader.Profile.from_username(L.context, request.get_json()['profile'].lower())
    #user_profile = get_or_create_user_profile(PROFILE)
     

    for post in profile.get_posts():
            target = os.path.join(app.config['STATIC_FOLDER']+'/'+profile.username)
            L.dirname_pattern = target
            L.download_post(post, target=profile.username)
   
    #for story in L.get_stories():
     #story is a Story object
    #    for item in story.get_items():
                #item is a StoryItem object
     #       L.download_storyitem(item, ':stories')

            response_object['message'] = 'Profile downloaded'

    else:

        response_object['username'] = PROFILE


    return jsonify(profile.get_posts())
	
@app.route('/api/instagram/update', methods=['GET', 'POST'])
def instagram_update():
    L = instaloader.Instaloader( compress_json=False )
    USER = 'idustbin'

    L.load_session_from_file(USER)

    images = ['*.mp4','*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']
    matches = []
    f = []
    #USER = 'idustbin'
    #PASSWORD = 'Apple2019!'
    #L.login(USER, PASSWORD)
    print(request.get_json())
    PROFILE = request.get_json()
 
    response_object = {'status': 'success'}
    profile = instaloader.Profile.from_username(L.context, request.get_json()['profile'].lower())
    if request.method == 'POST':
        posts = list(profile.get_posts())
        
        #for story in L.get_stories():
        #     L.story.get_items()
        #SINCE = datetime.today()
        #UNTIL = datetime()
        SINCE = datetime(2020, 1, 1)
        UNTIL = datetime.today()
        #for post in profile.get_posts():
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            target = os.path.join(app.config['STATIC_FOLDER']+'/'+profile.username)
            L.dirname_pattern = target
            L.download_post(post, target=target)
            print(post.date)
        response_object['message'] = 'Profile Updated!'
        for (dirpath, dirnames, filenames) in walk(app.config['STATIC_FOLDER']+'/'+request.get_json()['profile'].lower()):
            for extensions in images:
                for filename in fnmatch.filter(filenames, extensions):
                    matches.append(dirpath + '/' + filename)
            break
        response_object['data'] = matches
    else:
        response_object['username'] = PROFILE
    print(response_object)
    return jsonify(response_object)


# add caption to image
@app.route('/api/instagram/update/caption', methods=['POST'])
def instagram_caption_update():
    L = instaloader.Instaloader( compress_json=False )
    post = Post.from_shortcode(L.context, SHORTCODE)

    # Render caption
    image = Image.open(BytesIO(get(post.url).content))
    draw = ImageDraw.Draw(image)
    color = 'rgb(0, 0, 0)'  # black color
    draw.text((300,100), post.caption.encode('latin1', errors='ignore'), fill=color)
    image.save('test.jpg')

    # Save image
    return (image.save)

@app.route('/api/instagram/update/stories', methods=['POST'])
def instagram_story_update():
    L = instaloader.Instaloader( compress_json=False )
   
    USER = 'idustbin'
    PASSWORD = 'EpRkyTLvC2QzaWyda^]'
    L.login(USER, PASSWORD)
    
    if request.method == 'POST':
        profile = instaloader.Profile.from_username(L.context, request.get_json()['profile'].lower())

    for story in L.get_stories():
    # story is a Story object
        for item in story.get_items():
        # item is a StoryItem object
            L.download_storyitem(item, ':stories')

@app.route('/api/instagram/update/follower', methods=['POST'])
def instagam_get_follower():
    L = instaloader.Instaloader( compress_json=False )
    USER = 'idustbin'
    PASSWORD = 'Apple2019!'


# sanity check routes
@app.route("/ip", methods=["GET"])
def ip():
    return jsonify({ 'ip' : request.remote_addr }), 200

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()