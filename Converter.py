# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 21:14:21 2022

@author: Zijian Zhong
"""

import numpy as np
import pdf2image
import cv2
import os
from PIL import Image
from fpdf import FPDF

crop_up = 200
crop_down = 200
out_page_height = 3883
out_page_width = 5597
pdf_dir = "./pdf_in"

out_slide_height = int(out_page_height/2)
out_slide_width = int(out_page_width/2)
out_positions = [(0, 0), (int(out_page_width/2),0), (0, int(out_page_height/2)), (int(out_page_width/2), int(out_page_height/2))]


pdf_lst = []
for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        pdf_lst.append((os.path.join(pdf_dir, file), file))

for pdf_dir, pdf_name in pdf_lst:
    pages = pdf2image.convert_from_path(pdf_dir, 500)
    pages_array = [np.array(page) for page in pages]

    empty_page = np.ones((out_page_height, out_page_width))*255
    new_pages = []

    position_counter = 0
    page_counter = 0
    for page in pages_array:
        page_gray = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)
        # Crop the upper and lower captions
        page_gray = page_gray[crop_up:-crop_down,:]
        print("Size of page: ", page_gray.shape)
        rows = page_gray.shape[0]
        cols = page_gray.shape[1]
        upper_page_gray = page_gray[0:rows//2, :]
        lower_page_gray = page_gray[rows//2:, :]
        
        if np.mean(upper_page_gray)<255:
            print("Find something on upper page")
            resized_half_page = cv2.resize(upper_page_gray, (out_slide_width, out_slide_height))
            resized_half_page = cv2.putText(resized_half_page, '%d'%position_counter, (out_slide_width-100, out_slide_height-50), cv2.FONT_HERSHEY_SIMPLEX, 
                    2, (0, 0, 0), 1, cv2.LINE_AA)
            empty_page[out_positions[position_counter%4][1]:(out_positions[position_counter%4][1]+out_slide_height), 
            out_positions[position_counter%4][0]:(out_positions[position_counter%4][0]+out_slide_width)]= resized_half_page
            position_counter += 1
            if position_counter!=0 and position_counter%4==0:
                if position_counter==4:
                    empty_page = cv2.putText(empty_page, pdf_name, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        2, (0, 0, 0), 1, cv2.LINE_AA)
                new_pages.append(empty_page)
                empty_page = np.ones((out_page_height, out_page_width))*255
                print("NEW PAGE APPENDED! ")
        if np.mean(lower_page_gray)<255:
            print("Find something on lower page")
            resized_half_page = cv2.resize(lower_page_gray, (out_slide_width, out_slide_height))
            resized_half_page = cv2.putText(resized_half_page, '%d'%position_counter, (out_slide_width-100, out_slide_height-50), cv2.FONT_HERSHEY_SIMPLEX, 
                    2, (0, 0, 0), 1, cv2.LINE_AA)
            empty_page[out_positions[position_counter%4][1]:(out_positions[position_counter%4][1]+out_slide_height), 
            out_positions[position_counter%4][0]:(out_positions[position_counter%4][0]+out_slide_width)]= resized_half_page
            position_counter += 1
            if position_counter!=0 and position_counter%4==0:
                if position_counter==4:
                    empty_page = cv2.putText(empty_page, pdf_name, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        2, (0, 0, 0), 1, cv2.LINE_AA)
                new_pages.append(empty_page)
                empty_page = np.ones((out_page_height, out_page_width))*255
                print("NEW PAGE APPENDED! ")
        
        print("Processing Page:", page_counter)
        page_counter+=1

    if position_counter%4 !=0:
        print("NEW PAGE APPENDED! for the last counter")
        new_pages.append(empty_page)

    # out_page_count = 0
    # for page in new_pages:
    #     cv2.imwrite("OUTPUT_%d.png"%out_page_count, page)
    #     out_page_count +=1 


    images = [Image.fromarray(page).convert("RGB") for page in new_pages]
    images[0].save(
        "OUT_%s.pdf"%pdf_name, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )