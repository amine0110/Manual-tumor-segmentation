[![GitHub issues](https://img.shields.io/github/issues/amine0110/Manual-tumor-segmentation)](https://github.com/amine0110/Manual-tumor-segmentation/issues) [![GitHub license](https://img.shields.io/github/license/amine0110/Manual-tumor-segmentation)](https://github.com/amine0110/Manual-tumor-segmentation) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydicom)
# Manual tumor segmentation
This project was a homework about creating a plateforme using Python that helps the doctors to segment the tumors or organs manualy then calculate their volume or surface.

## Tool to create this app
To create this app, I used `Python` and `Tkinter` for the GUI, then I used other libraries to do the other features (the conversions ...)

## Features of this app 
- Friendly with dicom files
- Convert dicoms into JPG or PNG
- Convert normal image (JPG or PNG) into dicoms
- Extrat the patient information
- Anonymize the patient informations
- Segment the area directly in the canvas
- Calculate the volume and the surface of the selected area

## Little explanation
To convert a dicom image into normal RGB or grayscale image, all you need to do is to extract the pixel_array information from the dicom file than scale it to match a normal image's values.

```Python
ds.pixel_array.astype(float)
image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
```

And to extract the patient's information, you can use these commands:

```Python
patient_name = v[ 0 : 5 ]
patient_id = ds.PatientID
patient_birthday = ds.PatientBirthDate
patient_study_id = ds.StudyID
patient_study_day = ds.StudyDate
```
____________________________________________________________

![uRXIxzYB](https://user-images.githubusercontent.com/37108394/122125699-14a4dc00-ce31-11eb-9005-5652e45c3418.png)

- 1: Here we can display the images that we have in the database, so that we choose the frame that contains the areas needed.
- 2: These buttons to configure which area we will select and save.
- 3: These buttons change the frame displayed.
- 4: These are the patient information of the image displayed.
- 5: This button is to put the image in the canvas (to do the segmentation).
- 6: This button to anonymize the images.
- 7: These buttons to calculate the areas of each selected part.
- 8: This is the canvas where we put the image and do the segmentation.
- 9: This button is to convert images from DICOM into JPEG
- 10: This button is to save the image displayed in section 1.
- 11: This button is to load a new DICOM image.
- 12: This button is to convert images from JPEG into DICOM.
