import flask
from PIL import Image
import random
import os
from io import BytesIO
from flask import request,send_file , render_template


TEMPLATE_DIR=f"{os.getcwd()}/templates"
#print(TEMPLATE_DIR)
app = flask.Flask(__name__,static_folder=TEMPLATE_DIR)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('/index.html',vars=["REST","API","Server"])

@app.route('/upload', methods=['POST'])
def upload():
    tag=request.form.get('tag')
    img = Image.open(request.files['file'])
    id=random.randint(0,32000)
    while (str(id)+" ") in os.listdir():
        id=random.randint(0,32000)

    width,height=img.size
    if height> width:
        x=height/800
        height=int(height/x)
        width=int(width/x)


    else:

        x=width/800
        height=int(height/x)
        width=int(width/x)

    img=img.resize((width,height))

#cropping to 300x300
    width, height = img.size   # Get dimensions
    left = (width - 300)/2
    top = (height - 300)/2
    right = (width + 300)/2
    bottom = (height + 300)/2
    img = img.crop((left, top, right, bottom))



    img.save(f"{id} - {tag}.jpeg","jpeg",dpi=(72,72))
    file_size=os.path.getsize(f"{id} - {tag}.jpeg")/1024
    if file_size>512:
        img=Image.open(f"{id} - {tag}.jpeg","jpeg")
        to_reduce=(512/file_size)*100
        img.save(f"{id} - {tag}.jpeg","jpeg",quality=to_reduce)
    return render_template('index.html',vars=[f"ID:{id}","File Upload","Success"])
    #return send_file(f"{id} - {tag}.jpeg", mimetype='image/gif')

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=50)#The kwarg quality=50 is for displaying the compressed version as requested
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/image/<int:id>/resize', methods=['GET'])
def resize(id):
    
    height=int(request.args.get('height'))
    width=int(request.args.get('width'))
    

    size=(width,height)
    for m in os.listdir():
        if str(id) in m and "crop" not in m:
            print(m)
            im = Image.open(m)
            im=im.resize(size)
            
            # abc=im.show()
            # print(abc)
            # im.save(f'{os.getcwd()}/{m}', "JPEG")
            # return send_file(f'{os.getcwd()}/{m}', mimetype='image/gif')

            return serve_pil_image(im)

    return render_template('index.html',vars=[f"ID:{id}","Not","Found"])


@app.route('/image/<int:id>/crop', methods=['GET'])
def crop(id):
    new_height=int(request.args.get('height'))
    new_width=int(request.args.get('width'))

    for m in os.listdir():
        if str(id) in m and "crop" not in m:
            im = Image.open(m)
            
            width, height = im.size   # Get dimensions
  
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2


            im = im.crop((left, top, right, bottom))
            
            # im.save(f'{os.getcwd()}/crop-{m}', "JPEG")
            # return send_file(f'{os.getcwd()}/crop-{m}', mimetype='image/gif')
            return serve_pil_image(im)

    return f'Image with id:{id} not found'

@app.route('/serve_img/<id>', methods=['GET'])
def display_links(id):

    for m in os.listdir():
        print(m)
        if id in m:
            print(m)
            return send_file(f'{os.getcwd()}/{m}', mimetype='image/jpeg')





@app.route('/images/<tag>', methods=['GET'])
def all_links(tag):
    big_html=""
    for m in os.listdir():
        if str(" "+tag) in m:
            id=m.replace(f" - {tag}.jpeg","")
            big_html=big_html+f'<a href="../serve_img/{id}">{id}</a><br>'

    return big_html

@app.route('/image/<id>', methods=['PUT'])
def change_tag(id):
    new_tag=request.args.get('tag')
    for m in os.listdir():
        if str(id) in m:
            os.rename(m,f"{id} - {new_tag}.jpeg")

    return render_template('index.html',vars=[f"File Name","Updated","Successfully"])

@app.route('/image/<id>', methods=['DELETE'])
def delete_file(id):
    
    for m in os.listdir():
        if str(id) in m:
            os.remove(m)

    return render_template('index.html',vars=[f"File","Deleted","Successfully"])






app.run()