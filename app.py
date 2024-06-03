from flask import Flask, render_template,request,redirect,url_for,flash, jsonify
import os
import numpy as np
import cv2 
from werkzeug.utils import secure_filename
from expansion import expand_histogram

app=Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = 'static/raw/' 
app.config['DOWNLOAD_EQ_FOLDER'] = 'static/equalized/'
app.config['DOWNLOAD_EX_FOLDER'] = 'static/expanded/'
intensity_histo = [i for i in range(256) ]

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#validar si la extension del archivo es valida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#ruta principal
@app.route('/')
def index():
    return render_template("index.html")

#ruta para subir la imagen
@app.route('/upload',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash("Archivo no encontrado")
        return redirect(request.url)
    file = request.files['file']
    if file.filename=="":
        flash("Archivo no seleccionado")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_to_save)
        return redirect(url_for("upload",filename=filename))
    else:
        flash("Archivo no permitido")
        return redirect("/")

@app.route('/upload/<filename>')
def upload(filename):
    return render_template("upload.html", filename=filename)

@app.route('/histograma/<filename>/<folder>',methods=['GET'])
def histogram_raw(filename,folder):
    path_to_image = os.path.join(app.config[folder], filename)
    image = cv2.imread(path_to_image)
    #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    #calculating histograms for each channel
    b_histo = np.array(cv2.calcHist([image],[0], None, [256], [0,256])).flatten().tolist()
    g_histo = np.array(cv2.calcHist([image],[1], None, [256], [0,256])).flatten().tolist()
    r_histo = np.array(cv2.calcHist([image],[2], None, [256], [0,256])).flatten().tolist()

    histogram_values = {
        'Red': r_histo,
        'Green': g_histo,
        'Blue': b_histo,
        "intensity": intensity_histo
    } 
    return jsonify(histogram_values)

@app.route('/display_image/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='raw/' + filename), code=301)

@app.route('/display_equalized_image/<filename>')
def display_equalized_image(filename):
    return redirect(url_for('static', filename='equalized/' + filename), code=301)

#display_expanded_image
@app.route('/display_expanded_image/<filename>')
def display_expanded_image(filename):
    return redirect(url_for('static', filename='expanded/' + filename), code=301)

@app.route("/equalized/<filename>")
def equalized(filename):
    path_to_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(path_to_image)
    B = image[:,:,0] #blue layer
    G = image[:,:,1] #green layer
    R = image[:,:,2] #red layer
    
    b_equi = cv2.equalizeHist(B)
    g_equi = cv2.equalizeHist(G)
    r_equi = cv2.equalizeHist(R)

    new_filename='equalized_'+filename
    equi_im = cv2.merge([b_equi,g_equi,r_equi])
    equalized_filename = 'static/equalized/'+new_filename
    cv2.imwrite(equalized_filename, equi_im)
    new_filename = secure_filename(new_filename)
    return render_template("equalized.html", filename= new_filename )

#expanded
@app.route('/expanded/<filename>')
def expanded(filename):
    path_to_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(path_to_image)
    #seperating colour channels
    B = image[:,:,0] #blue layer
    G = image[:,:,1] #green layer
    R = image[:,:,2] #red layer
    #calculating histograms for each channel
    B_histo = cv2.calcHist([B],[0], None, [256], [0,256])
    G_histo = cv2.calcHist([G],[0], None, [256], [0,256])
    R_histo = cv2.calcHist([R],[0], None, [256], [0,256])
    print("\n\nExpandiendo ps")
    print(B_histo)
    print("\n")

    b_equi = expand_histogram(B_histo, B)
    g_equi = expand_histogram(G_histo, G)
    r_equi = expand_histogram(R_histo, R)
    print(b_equi)
    new_filename='expanded_'+filename
    
    equi_im = cv2.merge([b_equi,g_equi,r_equi])
    equalized_filename = 'static/expanded/'+new_filename
    cv2.imwrite(equalized_filename, equi_im)
    new_filename = secure_filename(new_filename)
    
    return render_template("expanded.html", filename= new_filename ) 

if __name__=="__main__":
    app.run()