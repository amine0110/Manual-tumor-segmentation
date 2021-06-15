import os
import numpy as np
import png
import pydicom
from PIL import ImageTk, Image as image
from tkinter import *
import cv2
import scipy as sp
import scipy.ndimage
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



def get_names_of_imgs_inside_folder(directory):

    names = []

    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in [".dcm"]:
                names.append(filename)

    return names

def make_image_ready_to_display(n):

    names = get_names_of_imgs_inside_folder('Database')
    ds = pydicom.dcmread('Database//' + names[n])
    

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    im = image.fromarray(image_2d_scaled)
    tk_im = ImageTk.PhotoImage(im)


    return tk_im

def make_image_ready_to_display_directory(directory1):

    # names = get_names_of_imgs_inside_folder('Database')
    ds = pydicom.dcmread(directory1)
    

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    im = image.fromarray(image_2d_scaled)
    tk_im = ImageTk.PhotoImage(im)


    return tk_im


def get_patient_information(n):

    names = get_names_of_imgs_inside_folder('Database')
    ds = pydicom.dcmread('Database//' + names[n])
    #ds = pydicom.dcmread('Database//Image00002.dcm')

    v = str(ds.PatientName)
    patient_name = v[0:5]
    patient_id = ds.PatientID
    patient_birthday = ds.PatientBirthDate
    patient_study_id = ds.StudyID
    patient_study_day = ds.StudyDate
    return patient_name, patient_id, patient_birthday, patient_study_id, patient_study_day

def return_image(n):
    names = get_names_of_imgs_inside_folder('Database')
    ds = pydicom.dcmread('Database//' + names[n])
    

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    im = image.fromarray(image_2d_scaled)
    return im

def return_image_directory(directory):
    
    ds = pydicom.dcmread(directory)
    

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    im = image.fromarray(image_2d_scaled)
    return im

def retrun_shape(image_in):
    image = image_in#cv2.imread(image_in) 
    cv2.waitKey(0) 

    gray = image_in#cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    
    edged = cv2.Canny(gray, 30, 200) 
    cv2.waitKey(0) 
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(image, contours, -1, (0, 0, 0), 3) 
    #cv2.imshow('Contours', image) 
    th, im_th = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV);
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), (255,255,255));
    #cv2.imshow("Floodfilled Image", im_floodfill)

    cv2.waitKey(0)
    return im_floodfill

def get_number_pixels(image_shape):
    count = 0
    np.array(image_shape)
    for i in range(400):
        for j in range(500):
            if image_shape[i,j] == 0:
                count +=1
    return count

def convert_jpg(directory):
    ds = pydicom.dcmread('Database/Image00001.dcm') # pre-existing dicom file
    im_frame = image.open(directory) # the PNG file to be replace

    if im_frame.mode == 'L':
        # (8-bit pixels, black and white)
        np_frame = np.array(im_frame.getdata(),dtype=np.uint8)
        ds.Rows = im_frame.height
        ds.Columns = im_frame.width
        ds.PhotometricInterpretation = "MONOCHROME1"
        ds.SamplesPerPixel = 1
        ds.BitsStored = 8
        ds.BitsAllocated = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.PixelData = np_frame.tobytes()
        ds.save_as('0_new_result_bw.dcm')
    elif im_frame.mode == 'RGBA':
        # RGBA (4x8-bit pixels, true colour with transparency mask)
        np_frame = np.array(im_frame.getdata(), dtype=np.uint8)[:,:3]
        ds.Rows = im_frame.height
        ds.Columns = im_frame.width
        ds.PhotometricInterpretation = "RGB"
        ds.SamplesPerPixel = 3
        ds.BitsStored = 8
        ds.BitsAllocated = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.PixelData = np_frame.tobytes()
        ds.save_as('0015_result_rgb.dcm')

def anonyme(n):
    names = get_names_of_imgs_inside_folder('Database')
    ds = pydicom.dcmread('Database//' + names[n])
    #ds = pydicom.dcmread('Database//Image00002.dcm')

    ds.PatientName = ''
    ds.PatientID = ''
    ds.PatientBirthDate = ''
    ds.StudyID = ''
    ds.StudyDate = ''

    return ds.PatientName, ds.PatientID, ds.PatientBirthDate, ds.StudyID, ds.StudyDate

def visualisation_3d(image_in):
    image_in_array = np.array(image_in)
    x = []
    y = []

    for i in range(400):
        for j in range(500):
            if image_in_array[i,j] == 0:
                x.append(i)
                y.append(j)
    
    x = np.array(x)
    y = np.array(y)

    ax = plt.axes(projection='3d')
    z = range(0,np.size(x))
    z = np.array(z)
    ax.plot3D(x,y,z)
    plt.show()
