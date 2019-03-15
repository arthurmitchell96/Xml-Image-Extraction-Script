import xml.etree.ElementTree as ET
import os
import numpy
from PIL import Image, ImageOps, ImageStat
import pandas as pd
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
#import cv2


directory = 'labimage labelled2/'


instar1_path = 'sorted_and_cropped/instar1/'
instar2_path = 'sorted_and_cropped/instar2/'
instar3_path = 'sorted_and_cropped/instar3/'
instar4_path = 'sorted_and_cropped/instar4/'
instar5_path = 'sorted_and_cropped/instar5/'
instar6_path = 'sorted_and_cropped/instar6/'
instar1_count = 0
instar2_count = 0
instar3_count = 0
instar4_count = 0
instar5_count = 0
instar6_count = 0
#list_of_numbers = list()
#list_of_files = list()
#edit_list_of_files = list()
#host_list = list()
locust_list = list()
instar_list = list()
def get_files(direc):
    for sub_dir, dirs, files in os.walk(direc, topdown=True):
        for file in files:
           if (sub_dir != '' and file != ''):
               dir_send = str(sub_dir) + '/'
               crop_n_sort(dir_send, file)
            #print(d)
def crop_n_sort(directory, file):

    name_of_doc = os.path.splitext(file)
    root = ''
    #only opening xml files
    if (os.path.splitext(directory +  file)[1] == '.xml'):
        try:
            filename = os.fsdecode(file)
            tree = ET.parse(directory + filename)
            root = tree.getroot()
        except FileNotFoundError:
                print('no file')
                
        #print(root)
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0 

        global instar1_count
        global instar2_count
        global instar3_count
        global instar4_count
        global instar5_count
        global instar6_count
        global count
        #opening the relevant images
        input_img =directory+ name_of_doc[0]+'.JPG'
        #arry_img = cv2.imread(input_img, 3)
        try:
            arry_img = Image.open(input_img)
                

            print('image converted')
        except FileNotFoundError:
            print('no image')
            return 0

       # box_size = (xmax - xmin) * (ymax-ymin)
        #cycles through xml tags to find objects
        for node in root:
            #print (node)
            hostname = node.tag
            #host_list.append(hostname)
            #hostname = hostname + '/object'
            #print (hostname)
            #print (node.find('/name').text)
            
        
            if (hostname == 'object'):
                xmin = 0
                xmax = 0
                ymin = 0
                ymax = 0 
                width = int(root.find('size/width').text)
                height = int(root.find('size/height').text)
                xmin = int(node.find('bndbox/xmin').text)
                ymin= int(node.find('bndbox/ymin').text)
                xmax = int(node.find('bndbox/xmax').text)
                ymax = int(node.find('bndbox/ymax').text)
                box_height = (xmax-xmin)
                box_width = (ymax-ymin)
                #img_height_shift = 300-box_height
                #shift_h = img_height_shift/2

                #img_width_shift = 200-box_height
                #shift_w = img_width_shift/2
                
#                    if ( width< (ymax + shift_w)):
#                        shift_w = (ymax+shift_w)-width
#                    if (ymin - shift_w <0):
#                        shift_w = shift_w-(ymin-shift_w)
#                    if (xmax + shift_h > height):
#                        shift_h = (xmax+shift_h)-height
#                    if (ymin - shift_h <0):
#                        shift_h = 0-(xmin-shift_h)
                
                #ymax= ymax + shift_w
                #ymin = ymin - shift_w
                #xmax= xmax + shift_h
                #xmin = xmin - shift_h
                
                box_height = int(xmax-xmin)
                box_width = int(ymax-ymin)

                #new_img = Image.new("RGB",(box_height,box_width), "black")

                if(ymax < width and xmax<height):
                    if(xmin>0 and ymin > 0):
                        new_img=arry_img.crop((xmin,ymin,xmax,ymax))
                        r, g, b = new_img.split()
                        blue_hist = b.histogram()
                        #blue_hist = hist[256:512]
                        blue = ImageStat.Stat(blue_hist)
                        try:
                            blue_std = int(blue.stddev[0])
                        except ZeroDivisionError:
                            continue
                        
                        if (box_width < 350 and node.find('name').text == 'locust_1'):
                            print ('instar 1')
                            #img = Image.fromarray(new_img,'RGB')
                            if (blue_std > 45):
                                new_img.save(instar1_path + name_of_doc[0]+'_instar_1_' + str(instar1_count) + '.jpg')
                                
                            #locust_list.append(root.find('object/name').text)
                                locust_list.append( name_of_doc[0]+'_instar_1_' + str(instar1_count) + '.jpg')
                                instar_list.append('1')
                                instar1_count = instar1_count + 1
                                
                        elif (hostname == 'object'and node.find('name').text == 'locust_2'):
                            print ('instar 2')
                            new_img.save(instar2_path +name_of_doc[0]+'_instar_2_'+ str(instar2_count) + '.jpg')
                            
                            #locust_list.append(root.find('object/name').text)
                            locust_list.append( name_of_doc[0]+'_instar_2_' + str(instar2_count) + '.jpg')
                            instar_list.append('2')
                            instar2_count = instar2_count + 1
                        elif (box_width < 500 and node.find('name').text == 'locust_3'):
                            print ('instar 3')
                            
                           
                            new_img.save(instar3_path +name_of_doc[0]+'_instar_3_'+ str(instar3_count) + '.jpg')
                            
                            #locust_list.append(root.find('object/name').text)
                            locust_list.append( name_of_doc[0]+'_instar_3_' + str(instar3_count) + '.jpg')
                            instar_list.append('3')
                            instar3_count = instar3_count + 1
                        elif (box_width < 600 and node.find('name').text == 'locust_4'):
                            print ('instar 4')
                            #img = Image.fromarray(new_img,'RGB')
                            new_img.save(instar4_path +name_of_doc[0]+'_instar_4_'+ str(instar4_count) + '.jpg')
                            
                            #locust_list.append(root.find('object/name').text)
                            locust_list.append(name_of_doc[0]+'_instar_4_' + str(instar4_count) + '.jpg')
                            instar_list.append('4')
                            instar4_count = instar4_count + 1
                        elif (box_height < 900 and node.find('name').text == 'locust_5'):
                            print ('instar 5')
                            #img = Image.fromarray(new_img,'name_of_doc')
                            new_img.save(instar5_path +name_of_doc[0]+'_instar_5_'+ str(instar5_count) + '.jpg')
                            
                            #locust_list.append(root.find('object/name').text)
                            locust_list.append( name_of_doc[0]+'_instar_5_' + str(instar5_count) + '.jpg')
                            instar_list.append('5')
                            instar5_count = instar5_count + 1
                        elif (hostname == 'object'and node.find('name').text == 'locust_6'):
                            print ('instar 6')
                            #img = Image.fromarray(new_img,'RGB')
                            new_img.save(instar6_path +name_of_doc[0]+'_instar_6_'+ str(instar6_count) + '.jpg')
                            locust_list.append( name_of_doc[0]+'_instar_6_' + str(instar6_count) + '.jpg')
                            instar_list.append('6')
                            instar6_count = instar6_count + 1
            
                                #locust_list.append(root.find('object/name').text)
                        
    return 1
            #print (box_size)
    
            #width = int(root.find('size/width').text)
            #height = int(root.find('size/height').text)

        #size = width * height

        #percent = (box_size/size) 
        #print(percent)
        #list_of_files.append(filename)
        
        #list_of_numbers.append(percent)
    

get_files(directory)    
print (instar1_count)
print (instar2_count)
print (instar3_count)
print (instar4_count)
print (instar5_count)
print (instar6_count)

locust_arr=numpy.array(locust_list)
cat_arr = numpy.asarray(instar_list)
final_arr = numpy.column_stack((locust_arr, cat_arr))
save_arr = numpy.asarray(final_arr)
print(save_arr)
pd.DataFrame(save_arr).to_csv("lables.csv")
