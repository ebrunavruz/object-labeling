
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:36:54 2019

@author: ebru
"""

import json
import cv2
import urllib
import numpy as np
import sys

#Reading json files
with open("newj.json") as json_file:
    json_data1 = json.load(json_file)


with open("test.json") as json_file:
    json_data2 = json.load(json_file)
  
size_of_image1=len(json_data1["data"])
size_of_image2=len(json_data2["data"])

new_json={}
data=[]
frm_dict={}
new_json['data']=data

def new_coordinates(x0_1,x0_2,x1_1,x1_2,y0_1,y0_2,y1_1,y1_2):
    x0_new=(x0_1+x0_2)/2;
    x1_new=(x1_1+x1_2)/2;
    y0_new=(y0_1+y0_2)/2;
    y1_new=(y1_1+y1_2)/2;       
    return  x0_new,x1_new,y0_new,y1_new;

def create_obj_dict(x0_new,x1_new,y0_new,y1_new):
    obj_dict={} 
    obj_dict['label']=objects1[ii]["label"]  
    obj_dict['x0']=x0_new
    obj_dict['x1']=x1_new                          
    obj_dict['y0']=y0_new                        
    obj_dict['y1']=y1_new
    return obj_dict;

def create_frame():
    frm_dict={}
    frm_dict['frame_height']=json_data2['data'][j]['frame_height']
    frm_dict['frame_url']=frame_url1
    frm_dict['frame_width']=json_data2['data'][j]['frame_width']
    frm_dict['objects']=[]
    return frm_dict;

url1=[]  
url2=[] 
def single(x0,x1,y0,y1):
    x0_new=x0;
    x1_new=x1;
    y0_new=y0;
    y1_new=y1;       
    return  x0_new,x1_new,y0_new,y1_new;

eslesenler=[];
eslesmeyenler=[];

for i in range(size_of_image1):
    for j in range(size_of_image2):
        frame_url1=(json_data1["data"][i]["frame_url"])
        frame_url2=(json_data2["data"][j]["frame_url"])
        if (frame_url1==frame_url2):
           frm_dict=create_frame() 
           objects1=(json_data1["data"][i]["objects"]) #images
           objects2=(json_data2["data"][j]["objects"]) #images
           num_of_objects1=len(objects1) #objects lerin icinde kac tane yerin isaretlenmis oldugunu verir
           num_of_objects2=len(objects2)
           for jj in range(num_of_objects2):
               for ii in range(num_of_objects1):  
                                           
                       if (objects1[ii]["label"]==objects2[jj]["label"]):
                           x0_1=objects1[ii]["x0"] 
                           x0_2=objects2[jj]["x0"]
                           x1_1=objects1[ii]["x1"]
                           x1_2=objects2[jj]["x1"]
                           y0_1=objects1[ii]["y0"]
                           y0_2=objects2[jj]["y0"]
                           y1_1=objects1[ii]["y1"]
                           y1_2=objects2[jj]["y1"]
                           frame_url=(json_data2["data"][j]["frame_url"])
                                   
                           #Calculating the Intersection over Union                  
                           Area_1=(x1_1 - x0_1) * (y1_1 - y0_1);
                           Area_2=(x1_2 - x0_2) * (y1_2 - y0_2);
                           
                           x_left=max(x0_1,x0_2)
                           y_bottom=max(y0_1,y0_2)
                           x_right=min(x1_1,x1_2)
                           y_top=min(y1_1,y1_2) 
                          
                           if (x_right > x_left) & (y_top > y_bottom):
                              Area_int = (x_right - x_left) * (y_top - y_bottom);
                              IoU = Area_int / (Area_1 + Area_2 - Area_int);
                              if IoU>0.8:
                                 x0_new,x1_new,y0_new,y1_new= new_coordinates(x0_1,x0_2,x1_1,x1_2,y0_1,y0_2,y1_1,y1_2)
                                 obj_dict=create_obj_dict(x0_new,x1_new,y0_new,y1_new)
                                 eslesenler.append(objects1[ii])
                                 eslesenler.append(objects2[jj])
                                 frm_dict['objects'].append(obj_dict)      
                           
                           for x in range (num_of_objects1):
                               if objects1[ii] not in eslesenler:
                                   if objects1[ii] not in eslesmeyenler:
                                       url1.append(json_data1["data"][i]["frame_url"])
                                       eslesmeyenler.append(json_data1["data"][i]["objects"][ii])    
                                         
                           for k in range (num_of_objects2):
                               if objects2[jj] not in eslesenler:
                                   if objects2[jj] not in eslesmeyenler:
                                       url2.append(json_data2["data"][j]["frame_url"])
                                       eslesmeyenler.append(json_data2["data"][j]["objects"][jj])
                                       
           for f in range(len(eslesmeyenler)-1):
               if (eslesmeyenler[f]["label"]==eslesmeyenler[f+1]["label"]):
                   x0_1=int(eslesmeyenler[f]["x0"])
                   y0_1=int(eslesmeyenler[f]["y0"])
                   y1_1=int(eslesmeyenler[f]["y1"])
                   x1_1=int(eslesmeyenler[f]["x1"])
        
                   x0_2=int(eslesmeyenler[f+1]["x0"])
                   y0_2=int(eslesmeyenler[f+1]["y0"])
                   y1_2=int(eslesmeyenler[f+1]["y1"])
                   x1_2=int(eslesmeyenler[f+1]["x1"])
                   url_response = urllib.request.urlopen(frame_url1)
                   img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                   img = cv2.imdecode(img_array, -1)
                   img2 = cv2.imdecode(img_array, -1)
                   img=cv2.rectangle(img, (x0_1, y1_1), (x1_1, y0_1), (255, 0, 0), 3)
                   img2=cv2.rectangle(img2, (x0_2, y1_2), (x1_2, y0_2), (0,191,255), 3)
                   cv2.imshow('First image',img)
                   cv2.imshow('Second image',img2)                          
                   cv2.waitKey(0)
                   cv2.destroyAllWindows() 
                   key=True
                   while (key):
                       x0_1=(eslesmeyenler[f]["x0"])
                       y0_1=(eslesmeyenler[f]["y0"])
                       y1_1=(eslesmeyenler[f]["y1"])
                       x1_1=(eslesmeyenler[f]["x1"])
        
                       x0_2=(eslesmeyenler[f+1]["x0"])
                       y0_2=(eslesmeyenler[f+1]["y0"])
                       y1_2=(eslesmeyenler[f+1]["y1"])
                       x1_2=(eslesmeyenler[f+1]["x1"])
                       val=input("If 1st image correct press 1,if 2nd correct press 2, if both correct press 3 otherwise press 4 ?")
                       if val=="1":
                           x0_new,x1_new,y0_new,y1_new = single(x0_1,x1_1,y0_1,y1_1) ;
                           obj_dict=create_obj_dict(x0_new,x1_new,y0_new,y1_new);
                           frm_dict['objects'].append(obj_dict)                       
                           break
                       elif val=="2":
                           x0_new,x1_new,y0_new,y1_new = single(x0_2,x1_2,y0_2,y1_2);
                           obj_dict=create_obj_dict(x0_new,x1_new,y0_new,y1_new);
                           frm_dict['objects'].append(obj_dict)                       
                           break
                       elif val=="3":     
                           x0_new,x1_new,y0_new,y1_new = new_coordinates(x0_1,x0_2,x1_1,x1_2,y0_1,y0_2,y1_1,y1_2) 
                           obj_dict=create_obj_dict(x0_new,x1_new,y0_new,y1_new);
                           frm_dict['objects'].append(obj_dict)                       
                           break
                       elif val=="4":                                   
                           break;
                       elif val=="q":
                           sys.exit()
                       else:
                           print("plese give valid number")
                           cv2.imshow('First image',img)
                           cv2.imshow('Second image',img2)                          
                           cv2.waitKey(0)
                           cv2.destroyAllWindows()
           eslesenler=[];
           eslesmeyenler=[];
           if (len(frm_dict["objects"])!=0):
               new_json['data'].append(frm_dict)  
with open('new_json.json', 'w') as outfile:
    json.dump(new_json, outfile)
