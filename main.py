from google.cloud import vision
from google.cloud.vision import types
from googleapiclient.discovery import build
from os.path import isfile, join
import os, io
from os import listdir
from PIL import Image, ImageDraw
import numpy as np
import collections
import pandas as pd
import matplotlib.pyplot as plt
import time
import pyautogui
import tempfile2
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
#from google.colab import auth
import json

def video_search(api_key,youtube):
    type(youtube)
    #place your search
    w_print = str(input("Search:                                  "))
    req = youtube.search().list(q=w_print, part='snippet', type='video', maxResults=1)
    type(req)
    res = req.execute()
    #get video ID
    videoid=res['items'][0]['id']['videoId']
    req2= youtube.videos().list(part='snippet,contentDetails', id=videoid)
    print("Tittle: ",res['items'][0]['snippet']['title'])
    print('Link: https://www.youtube.com/watch?v='+res['items'][0]['id']['videoId'])
    return res;

def get_tags(res,api_key,youtube):
    item_list = []
    lista_tags = []
    a = 0
    #get tags
    for item in res['items']:
        item_list.append(str(item['id']['videoId']))
        videoid = item_list[a]  # example
        req2 = youtube.videos().list(part='snippet,contentDetails', id=videoid)
        res2 = req2.execute()
        res2['items']
        a = a + 1
        for i in range(len(res2['items'][0]['snippet']['tags'])):
            lista_tags.append(res2['items'][0]['snippet']['tags'][i])
    return lista_tags;

def listToString(s):
    # initialize an empty string
    str1 = " "
    # return string
    return (str1.join(s))

def sample_classify_text(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """
    client = vision.ImageAnnotatorClient()
    aux = []
    client = language_v1.LanguageServiceClient()

    # text_content = 'That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    response = client.classify_text(document)
    aux.append(response.categories)
    # Loop through classified categories returned from the API
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print(u"Category name: {}".format(category.name))
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        print(u"Confidence: {}".format(category.confidence))
def auth_token():
    #auth.authenticate_user()
    #gauth = GoogleAuth()
    #gauth.credentials = GoogleCredentials.get_application_default()
    #drive = GoogleDrive(gauth)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='Insert_google_cloud_credentials'
    client = vision.ImageAnnotatorClient()
    #fluff, id = link.split('=')
    #print(id)
    #return;

if __name__ == '__main__':
    print("Youtube Video Analycer")
    key = 'Inser_google_Cloud_key'
    utube = build('youtube', 'v3', developerKey=key)
    auth_token()
    video=video_search(key,utube)
    tags = get_tags(video,key,utube)
    print(tags)
    descripcion = listToString(tags)
    res3 = sample_classify_text(descripcion)
    print("close")
