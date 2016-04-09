# -*- coding: utf-8 -*-
"""
 Project - Image Mosaics

@author: Khirthana Subramanian


Instructions to run code:
  python Project-ImageMosaics.py input_image_filename data_foldername output_mosaic_filename
  
  example: python Project-ImageMosaics.py panda.jpg C:\project-image-mosaics\data mosaic-panda.png
  
  prompts for other inputs once input_image_filename, data_foldername, output_mosaic_filename are valid

Code outline:
reads data images, computes & stores data image filename & histogram
then reads input image, divides it into subimages, loops through subimages & replace it with best matching data image
once all subimages are replaced, saves created mosaic to file
"""

import argparse
import cv2
import numpy as np
import scipy as sp
import os  
import json
from scipy.linalg import norm
import datetime

#dictionary to store data images' filename and computed histograms
data={}

#dimensions of subimage
subimage_w=0
subimage_h=0


def load_image(imgfile,img_w,img_h,mosaic_filename):
    now=datetime.datetime.now()
    
    print 'Opening ', imgfile
    
#reads and resize input image 
    img = cv2.imread(imgfile)
    resized_image = cv2.resize(img, (img_w,img_h))
     
#divides input image into sub-images
 #loops through subimages to compare with data images & replace all subimages with data images
    i=0
    j=0
    
    x1=0
    x2=subimg_w
    y1=0
    y2=subimg_h
    
    total_subimg_row=img_h/subimg_h
    total_subimg_column=img_w/subimg_w
    total_subimg=total_subimg_row*total_subimg_column
    
    print 'Creating mosaic'
    while j<total_subimg:
        
        #subimage is computed
        subimg = resized_image[y1:y2, x1:x2]
    
        #calls compare method
        compare(subimg,resized_image,y1,y2,x1,x2)
        
        j=j+1
        
        if i<(total_subimg_column-1):
            i=i+1
            x1=x2
            x2=x2+subimg_w
        else:
            i=0
            y1=y2
            y2=y2+subimg_h
            x1=0
            x2=subimg_w
    	  	
    #once all sub-image is replaced; mosaic is saved to file
    print 'Saving mosaic', mosaic_filename
    cv2.imwrite(mosaic_filename,resized_image)
    
    #total time taken to create mosaic image is computed & printed
    now2=datetime.datetime.now()
    totaltime=now2-now
    print 'time taken to create mosaic: ', totaltime




def load_database(folder_name):

    print 'Loading Database of Images'
    
    #loops through all images files in data folder
    for root, dirs, files in os.walk(folder_name, topdown=False):
        for name in files:
            
            #reads data image
            data_img = cv2.imread(os.path.join(root, name))
            
            #resize data image corresponding to subimage size
            resize_data = cv2.resize(data_img, (subimg_w,subimg_h))
            
            #computes, normalizes histogram & stores in dictionary data
            hist = cv2.calcHist([resize_data], [0, 1, 2],None, [8, 8,8], [0, 256, 0, 256, 0, 256])    
            
            hist=hist.flatten()/sum(hist.flatten())
            
            hist=hist.tolist()
            
            data[os.path.join(root, name)] = hist


    #saves dictionary to json file to access it without calling load_database function repetitively
    with open('data.json', 'w') as fp:
		json.dump(data, fp)              
		
  
  
  
def compare(subimg,img,y1,y2,x1,x2):
#loops through database images  
 #compares subimage's histogram to database img's histogram
  #replace the best database image to subimage position on input image

   
    #computes & normalizes histogram of subimage 
    hist = cv2.calcHist([subimg], [0, 1, 2],None, [8, 8, 8], [0, 256, 0, 256, 0, 256])    
    
    hist=hist.flatten()/sum(hist.flatten())
    

    data_norm={}
    
    #reads json file which contain data images' filename & histogram
    with open('data.json', 'r') as fp:
        data = json.load(fp)     
        for key, value in data.items():
            filename=key
            
            #computes norm of diferrence between subimg's histogram and data img's histogram 
            difference_norm=norm(value-hist)
            
            #computed norm and corresponding data image file is stored in dictionary data_norm
            data_norm[filename] = difference_norm
            
                
    #finds smallest value which corresponds to data image which matches best with subimage 
    data_filename=min(data_norm,key=data_norm.get)
    
    data_image = cv2.imread(data_filename)
            
    data_img_resize=cv2.resize(data_image, (subimg_w,subimg_h))
    
    #subimage of input image is replaced by corresponding data image
    img[y1:y2,x1:x2]=data_img_resize
                        
   
   
   
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='CSCI 4220U Lab 3.')
   parser.add_argument('imgfile', help='Image file')
   parser.add_argument('folder_name', help='folder containing image database')
   parser.add_argument('mosaic_filename', help='filename to save output mosaic image')
   args = parser.parse_args()
   
#verifies if arguments are valid otherwise prompts user to enter valid inputs again     
   
   #verifies if data folder name is valid
   input1=True
   data_folder_path=args.folder_name
   while(input1):
       
       #if valid, prompts dimension to resize data image
       if(os.path.exists(data_folder_path)):
            input1=False
            
            while(True):
                w = raw_input('Enter width to resize data image(e.g.:10 or 20): ')
                try:
                   subimg_w = int(w)
                except ValueError:
                   print('Error: width input is not an int!')
                   continue
                else:
                   break
            while(True):
                h = raw_input('Enter height to resize data image(e.g.:10 or 20): ')
                try:
                   subimg_h = int(h)
                except ValueError:
                   print('Error: height input is not an int!')
                   continue
                else:
                   break
            
            #calls function to load database images & compute its histogram
            #load_database(data_folder_path)
       else:
            print 'Error: Data images folder does not exist!'
            data_folder_path = raw_input('Please enter data images folder path: ')
            

   #verifies if input image filename is valid
   input2=True
   imgfile=args.imgfile
   while(input2):
       
       #if valid,prompts dimensions to resize input image 
       if(os.path.isfile(imgfile)):
            input2=False
            
            while(True):
                img_w = raw_input('Enter image width to resize (e.g.:2000): ')
                try:
                    image_width = int(img_w )
                except ValueError:
                    print('Error: width input is not an int!')
                    continue
                else:
                    break
            while(True):
                img_h = raw_input('Enter image height to resize (e.g.:2000): ')
                try:
                   image_height = int(img_h)
                except ValueError:
                   print('Error: height input is not an int!')
                   continue
                else:
                   break
               
            #calls function to load image and compute mosaic       
            load_image(imgfile,image_width,image_height,args.mosaic_filename)
       else:
             print('Error: Input image does not exist!')
             imgfile= raw_input('Enter the input image filename: ')
             
             