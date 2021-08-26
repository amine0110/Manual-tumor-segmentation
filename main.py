from tkinter import *
import os
from functions import make_image_ready_to_display, get_patient_information
from functions import return_image
from functions import get_names_of_imgs_inside_folder
from functions import make_image_ready_to_display_directory
from functions import return_image_directory
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from functions import retrun_shape
from functions import get_number_pixels
from functions import convert_jpg
from functions import anonyme
from functions import visualisation_3d


window = Tk()
window.geometry('1220x730')
window.title('Detect regions')
window.configure(bg='#A9A9A9')


n_image = 0
lastx, lasty = 0, 0

mat_tz = np.ones((400,500))
mat_pz = np.ones((400,500))
mat_cz = np.ones((400,500))
mat_tumor = np.ones((400,500))

# This function is to clear the frame and put the new image with its indexe
def next_image():
    global n_image

    if n_image < 63:
        for item in zone_for_the_image.winfo_children():
            item.destroy()
        
        n_image +=1
        global image_to_display
        image_to_display = make_image_ready_to_display(n_image)

        create_image = Label(zone_for_the_image, image=image_to_display)
        create_image.pack()

        indexe_of_image = Label(zone_for_the_image, text=str(1 + n_image) + (" / 64"), bg='#2F4F4F', font="none 15")
        indexe_of_image.pack(pady=(20,0))

        for item in patient_info_frame.winfo_children():
            item.destroy()
        
        information = get_patient_information(n_image)
        info_title = Label(patient_info_frame, text="Patient's Information", font='none 18 bold', bg='#A9A9A9', padx=25)
        info_title.grid(row=0, column=0)

        
        info = "Name: "+ str(information[0]) + '\t' + '\t'+ 'ID: '+ str(information[1]) + '\n' + '\n' + 'Birthday: ' + str(information[2]) +'\t' +'\t'+ 'Study ID: ' + str(information[3]) +'\n' + '\n' + 'Study date: ' + str(information[4])

        info_label = Label(patient_info_frame, text=info, bg='#2F4F4F', font='none 12', fg='#ffffff')
        info_label.grid(row=1, column=0, pady=(20,0))


def previous_image():
    global n_image

    if n_image>0:
        for item in zone_for_the_image.winfo_children():
            item.destroy()
        n_image -=1
        global image_to_display
        image_to_display = make_image_ready_to_display(n_image)

        create_image = Label(zone_for_the_image, image=image_to_display)
        create_image.pack()

        indexe_of_image = Label(zone_for_the_image, text=str(1 + n_image) + (" / 64"), bg='#2F4F4F', font="none 15")
        indexe_of_image.pack(pady=(20,0))
        for item in patient_info_frame.winfo_children():
            item.destroy()
        
        information = get_patient_information(n_image)
        info_title = Label(patient_info_frame, text="Patient's Information", font='none 18 bold', bg='#A9A9A9', padx=25)
        info_title.grid(row=0, column=0)

        
        info = "Name: "+ str(information[0]) + '\t' + '\t'+ 'ID: '+ str(information[1]) + '\n' + '\n' + 'Birthday: ' + str(information[2]) +'\t' +'\t'+ 'Study ID: ' + str(information[3]) +'\n' + '\n' + 'Study date: ' + str(information[4])

        info_label = Label(patient_info_frame, text=info, bg='#2F4F4F', font='none 12', fg='#ffffff')
        info_label.grid(row=1, column=0, pady=(20,0))

def save_image():
    global n_image

    directory = filedialog.asksaveasfilename()
    if directory:
        image_to_save = return_image(n_image)
        image_to_save.save(directory)

def load_image():
    directory = filedialog.askopenfilename()
    if directory:
        for item in zone_for_the_image.winfo_children():
            item.destroy()
    
        global image_to_display
        image_to_display = make_image_ready_to_display_directory(directory)

        create_image = Label(zone_for_the_image, image=image_to_display)
        create_image.pack()
    
def dcm_to_jpg():
    directory = filedialog.askopenfilename()
    if directory:
        global image_to_display
        image_to_convert = return_image_directory(directory)
        image_to_convert.save('coverted.jpg')

def jpg_to_dcm():
    directory = filedialog.askopenfilename()
    convert_jpg(directory)
       
def display_in_canvas():
    image_canvas_1 = return_image(n_image)
    new_image = image_canvas_1.resize((500,400), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(new_image)
    canva.image = new_image
    canva.create_image(0,0, image = canva.image, anchor='nw')  

 
def xy(event):
    "Takes the coordinates of the mouse when you click the mouse"
    global lastx, lasty
    lastx, lasty = event.x, event.y
 
def addLine_tz(event):

    global lastx, lasty
    canva.create_line((lastx, lasty, event.x, event.y), width=3, fill='blue')
    lastx, lasty = event.x, event.y
    global mat_tz
    
    if lastx < 500 and lastx >=0 and lasty < 400 and lasty >=0:
        mat_tz[lasty][lastx] = 0 
        mat_tz[lasty+1][lastx+1] = 0 
        mat_tz[lasty-1][lastx-1] = 0 
        mat_tz[lasty+1][lastx-1] = 0 
        mat_tz[lasty-1][lastx+1] = 0 
        

def addLine_pz(event):

    global lastx, lasty
    canva.create_line((lastx, lasty, event.x, event.y), width=3, fill='green')
    lastx, lasty = event.x, event.y
    global mat_pz
    
    if lastx < 500 and lastx >=0 and lasty < 400 and lasty >=0:
        mat_pz[lasty][lastx] = 0 
        mat_pz[lasty+1][lastx+1] = 0 
        mat_pz[lasty-1][lastx-1] = 0 
        mat_pz[lasty+1][lastx-1] = 0 
        mat_pz[lasty-1][lastx+1] = 0 
    
    

def addLine_cz(event):

    global lastx, lasty
    canva.create_line((lastx, lasty, event.x, event.y), width=3, fill='yellow')
    lastx, lasty = event.x, event.y
    global mat_cz
    
    if lastx < 500 and lastx >=0 and lasty < 400 and lasty >=0:
        mat_cz[lasty][lastx] = 0 
        mat_cz[lasty+1][lastx+1] = 0 
        mat_cz[lasty-1][lastx-1] = 0 
        mat_cz[lasty+1][lastx-1] = 0 
        mat_cz[lasty-1][lastx+1] = 0 

def addLine_tumor(event):

    global lastx, lasty
    canva.create_line((lastx, lasty, event.x, event.y), width=3, fill='red')
    lastx, lasty = event.x, event.y
    global mat_tumor
    
    if lastx < 500 and lastx >=0 and lasty < 400 and lasty >=0:
        mat_tumor[lasty][lastx] = 0 
        mat_tumor[lasty+1][lastx+1] = 0 
        mat_tumor[lasty-1][lastx-1] = 0 
        mat_tumor[lasty+1][lastx-1] = 0 
        mat_tumor[lasty-1][lastx+1] = 0 
    
    
    

def detect_tz():
    mat_tz[:,:]=1
    canva.bind("<Button-1>", xy)
    canva.bind("<B1-Motion>", addLine_tz)
    

def detect_pz():
    mat_pz[:,:]=1
    canva.bind("<Button-1>", xy)
    canva.bind("<B1-Motion>", addLine_pz)

def detect_cz():
    mat_cz[:,:]=1
    canva.bind("<Button-1>", xy)
    canva.bind("<B1-Motion>", addLine_cz)

def detect_tumor():
    mat_tumor[:,:]=1
    canva.bind("<Button-1>", xy)
    canva.bind("<B1-Motion>", addLine_tumor)

       
def tz_area():
    image_mattt = (mat_tz*255).astype(np.uint8)
    image_shape = retrun_shape(image_mattt)
    gettt = get_number_pixels(image_shape)
    area = gettt * 0.7891**2
    volume = area*1.25

    new = Toplevel()
    new.geometry('400x130')
    new.title('Info')
    lab_title = Label(new, text='The results of this patient', font='agencyFR 20 bold')
    lab_title.pack()
    lab_area = Label(new, text='The area of the transition zone: '+ str(area)+ ' mm²', font='agencyFR 10')
    lab_area.pack(pady=(15,5))
    lab_volume = Label(new, text='The volume of the transition zone: '+ str(volume)+ ' mm²', font='agencyFR 10')
    lab_volume.pack()


def pz_area():
    image_mattt = (mat_pz*255).astype(np.uint8)
    image_shape = retrun_shape(image_mattt)
    gettt = get_number_pixels(image_shape)
    area = gettt * 0.7891**2
    volume = area*1.25

    new = Toplevel()
    new.geometry('400x130')
    new.title('Info')
    lab_title = Label(new, text='The results of this patient', font='agencyFR 20 bold')
    lab_title.pack()
    lab_area = Label(new, text='The area of the peripheral zone: '+ str(area)+ ' mm²', font='agencyFR 10')
    lab_area.pack(pady=(15,5))
    lab_volume = Label(new, text='The volume of the peripheral zone: '+ str(volume)+ ' mm²', font='agencyFR 10')
    lab_volume.pack()

def cz_area():
    image_mattt = (mat_cz*255).astype(np.uint8)
    image_shape = retrun_shape(image_mattt)
    gettt = get_number_pixels(image_shape)
    area = gettt * 0.7891**2
    volume = area*1.25

    new = Toplevel()
    new.geometry('400x130')
    new.title('Info')
    lab_title = Label(new, text='The results of this patient', font='agencyFR 20 bold')
    lab_title.pack()
    lab_area = Label(new, text='The area of the capsule zone: '+ str(area)+ ' mm²', font='agencyFR 10')
    lab_area.pack(pady=(15,5))
    lab_volume = Label(new, text='The volume of the capsule zone: '+ str(volume)+ ' mm²', font='agencyFR 10')
    lab_volume.pack()


def tumor_area():
    image_mattt = (mat_tumor*255).astype(np.uint8)
    image_shape = retrun_shape(image_mattt)
    gettt = get_number_pixels(image_shape)
    area = gettt * 0.7891**2
    volume = area*1.25
    
    new = Toplevel()
    new.geometry('400x130')
    new.title('Info')
    lab_title = Label(new, text='The results of this patient', font='agencyFR 20 bold')
    lab_title.pack()
    lab_area = Label(new, text='The area of the tumor zone: '+ str(area)+ ' mm²', font='agencyFR 10')
    lab_area.pack(pady=(15,5))
    lab_volume = Label(new, text='The volume of the tumor zone: '+ str(volume)+ ' mm²', font='agencyFR 10')
    lab_volume.pack()

def get_anonyme_and_display():

    for item in patient_info_frame.winfo_children():
        item.destroy()

    information = anonyme(n_image)
    info_title = Label(patient_info_frame, text="Patient's Information", font='none 18 bold', bg='#A9A9A9', padx=25)
    info_title.grid(row=0, column=0)

    
    info = "Name: "+ str(information[0]) + '\t' + '\t'+ 'ID: '+ str(information[1]) + '\n' + '\n' + 'Birthday: ' + str(information[2]) +'\t' +'\t'+ 'Study ID: ' + str(information[3]) +'\n' + '\n' + 'Study date: ' + str(information[4])

    info_label = Label(patient_info_frame, text=info, bg='#2F4F4F', font='none 12', fg='#ffffff')
    info_label.grid(row=1, column=0, pady=(20,0))

def visual_3d():
    image_mattt = (mat_tz*255).astype(np.uint8)
    image_shape = retrun_shape(image_mattt)
    func = visualisation_3d(image_shape)

if __name__ == '__main__':
    # # # # # # # # # # # # # # # # # # # # # # 
    # This part is for displaying the images  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    total_first_frame = Frame(window, bg='#2F4F4F', width=400, height=450)
    total_first_frame.grid(row=0, column=0, rowspan=2, padx=(10,0), pady=(10,0))
    total_first_frame.grid_propagate(0)

    display_title = Label(total_first_frame, text='Look for the image', font="none 15 bold", bg='#2F4F4F', fg='#ffffff')
    display_title.grid(row=0, column=0, pady=(0,10))

    zone_for_the_image = Frame(total_first_frame, width=380, height=400, bg='#2F4F4F')
    zone_for_the_image.grid(row=1, column=0, pady=(0,10), padx=(6.5,0))


    # # # # # # # # # # # # # # # # # # # # # # #
    # This part is for the tools (button, ...)  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    tool_zone = Frame(window, bg='#2F4F4F', width=200, height=450)
    tool_zone.grid(row=0, column=1, rowspan=2, padx=(40,40), pady=(10,0))
    tool_zone.grid_propagate(0)

    tool_title = Label(tool_zone, text='TOOLS', font="none 15 bold", bg='#2F4F4F', fg='#ffffff')
    tool_title.grid(pady=(0,10), padx=(18,0))

    # Load button
    load_button = Button(tool_zone, text='Load', width=18, font="none 12", command=load_image)
    load_button.grid(padx=(18,0), pady=(20,0))

    # Save button
    save_button = Button(tool_zone, text='Save', width=18, font="none 12", command=save_image)
    save_button.grid(padx=(16,0), pady=(15,0))

    # Dicom to Jpeg
    dcm_jpg = Button(tool_zone, text='Dcm to Jpg', width=18, font="none 12", command=dcm_to_jpg)
    dcm_jpg.grid(padx=(16,0), pady=(15,0))

    # Dicom to png
    jpg_dcm = Button(tool_zone, text='Jpg to Dcm', width=18, font="none 12", command=jpg_to_dcm) 
    jpg_dcm.grid(padx=(16,0), pady=(15,0))

    # TZ button
    TZ = Button(tool_zone, text="TZ", width=10, font="none 12 bold",fg='blue', command=detect_tz)
    TZ.grid(padx=(16,0), pady=(15,0))


    # PZ button
    PZ = Button(tool_zone, text="PZ", width=10, font="none 12 bold",fg='green', command=detect_pz)
    PZ.grid(padx=(16,0), pady=(10,0))

    # CZ button
    CZ = Button(tool_zone, text="CZ", width=10, font="none 12 bold",fg='#FFD700', command=detect_cz)
    CZ.grid(padx=(16,0), pady=(10,0))

    # Tumor button
    tumor = Button(tool_zone, text="Tumor", width=10, font="none 12 bold",fg='red', command=detect_tumor)
    tumor.grid(padx=(16,0), pady=(10,0))
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    # # # # # # # # # # # # # # # # # # #
    # This part is to select the zones  #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    total_second_frame = Frame(window, bg='#2F4F4F', width=520, height=450)
    total_second_frame.grid(row=0, column=2, rowspan=2, padx=(0,10), pady=(10,0))
    total_second_frame.grid_propagate(0)

    # This label is for the title of selecting an area
    title_select = Label(total_second_frame, text='Select the zone', font="none 15 bold", bg='#2F4F4F', fg='#ffffff')
    title_select.grid(row=0, column=0, pady=(0,10), padx=130)

    # The canvas to image for selecting the zones
    canva = Canvas(total_second_frame, width=500, height=400, bg='#A9A9A9')
    canva.grid(row=1, column=0, padx=(8,10))

    #canva.bind("<Button-1>", xy)
    #canva.bind("<B1-Motion>", addLine)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # This label is for displaying the first image once we run the program
    first_image = make_image_ready_to_display(0)
    init_image = Label(zone_for_the_image, image=first_image)
    init_image.pack()


    indexe_of_image = Label(zone_for_the_image, text=str(n_image+1)+(" / 64"), bg='#2F4F4F', font="none 15")
    indexe_of_image.pack(pady=(20,0))

    # Here I put a frame for the buttons so that I can control its places
    buttons_frame = Frame(window, width = 400, bg='#A9A9A9')
    buttons_frame.grid(row=2, column=0, pady=20)

    # This button is for the backward, which means go to previous image
    backward_button = Button(buttons_frame, text='back', width=13, font='none 12 bold', command=previous_image)
    backward_button.grid(row=0, column=0, padx=(0,100))

    # This button is for the forward, which means go to the next image
    forward_button = Button(buttons_frame, text='next', width=13, font='none 12 bold', command=next_image)
    forward_button.grid(row=0, column=1)


    display_in_canvas_button = Button(window, text="display", width=13, font='none 12 bold', command=display_in_canvas)
    display_in_canvas_button.grid(row=2, column=1)

    frame_anonyme_3d = Frame(window)
    frame_anonyme_3d.grid(row=3, column=1)
    anonyme_image = Button(frame_anonyme_3d, text='Anonyme', width=13, font='none 12 bold', command=get_anonyme_and_display)
    anonyme_image.grid()

    visu_3d = Button(frame_anonyme_3d, text="3D visual", width=13, font='none 12 bold', command=visual_3d)
    visu_3d.grid()

    frame_buttons_mask_surface = Frame(window, bg='#2F4F4F', width=400, height=100)
    frame_buttons_mask_surface.grid(row=2, column=2)
    frame_buttons_mask_surface.grid_propagate(0)

    area_tz_buttn = Button(frame_buttons_mask_surface, text='TZ area', width=15, font='none 12 bold',command=tz_area)
    area_tz_buttn.grid( pady=(10,10), row=0, column=0, padx=(35,15))
    area_pz_buttn = Button(frame_buttons_mask_surface, text='PZ area', width=15, font='none 12 bold', command=pz_area)
    area_pz_buttn.grid(pady=(10,10), row=0, column=1)
    area_cz_buttn = Button(frame_buttons_mask_surface, text='CZ area', width=15, font='none 12 bold', command=cz_area)
    area_cz_buttn.grid(pady=(0,10), row=1, column=0, padx=(35,15))
    area_tumor_buttn = Button(frame_buttons_mask_surface, text='Tumor area', width=15, font='none 12 bold', command=tumor_area)
    area_tumor_buttn.grid(pady=(0,10), row=1, column=1)



    # # # # # # # # # # # # # # # # # # # # #
    # The label for the patient information #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    patient_info_frame = Frame(window, width=300, height=100, bg='#A9A9A9')
    patient_info_frame.grid(row=3, column=0)
    #patient_info_frame.grid_propagate(0)

    info_title = Label(patient_info_frame, text="Patient's Information", font='none 18 bold', bg='#A9A9A9', padx=25)
    info_title.grid(row=0, column=0)

    information = get_patient_information(n_image)
    info = "Name: "+ str(information[0]) + '\t' + '\t'+ 'ID: '+ str(information[1]) + '\n' + '\n' + 'Birthday: ' + str(information[2]) +'\t' +'\t'+ 'Study ID: ' + str(information[3]) +'\n' + '\n' + 'Study date: ' + str(information[4])

    info_label = Label(patient_info_frame, text=info, bg='#2F4F4F', font='none 12', fg='#ffffff')
    info_label.grid(row=1, column=0, pady=(20,0))

    my_name_frame = Frame(window, width=400, height=130, bg='#2F4F4F')
    my_name_frame.grid(row=3, column=2, pady=(20,0))
    my_name_frame.grid_propagate(0)

    made_by_lab = Label(my_name_frame, text='Made by:', bg='#2F4F4F', fg='#FFFFFF', font='agencyFR 20')
    made_by_lab.pack(padx=100)
    my_name_lab = Label(my_name_frame, text="Mohammed El Amine", bg='#2F4F4F', fg='#FFFFFF', font='agencyFR 15')
    my_name_lab.pack()
    my_last_name_lab = Label(my_name_frame, text='MOKHTARI', bg='#2F4F4F', fg='#FFFFFF', font='agencyFR 15')
    my_last_name_lab.pack()



    window.mainloop()
