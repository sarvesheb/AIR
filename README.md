# Image Manipulation using REST
External Modules used:
Flask
Pillow

 This is a very simple REST API built using Flask(Python) for Image Manipulation created for AIR internship
 The lightweight server can be initiated by executing the python file
 
 python apiX.py
 
 The output of this shows the port at which it has been hosted and makes the server stay alive and wait for request
 
 The subdomains serve specific functionalities as mentioned below
 
 POST /upload - This method accepts an image and a tag. We try resizing it to 800x800 but still maintaining the original aspect ratio. A 300x300 image is cropped out exactly from the centre and the image is compressed if it exceeds 512KB and finally saved]
 
 GET supports the following operations:
 
image/<id>/resize?height={value}&width={value} - returns a resized image with appropriate dimensions.
image/<id>/crop?height={value}&width={value} - returns a cropped image with appropriate dimensions.
images/<tag> - returns a list of images having the specified tag
 
 
PUT /image/<id>?tag={new-tag} - Updates the tag of the specified image to new-tag.
 
DELETE /image/<id> - Deletes the specified image from the database.

                
Since the amount of metadata required to be stored for each entry is very insignificant, all the queries are implemented based on file names.
Even if the DB is used, finally for differentiating multiple images stored, file naming convention is the way to implement. 
