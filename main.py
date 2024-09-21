from flask import Flask, render_template, request, flash, session, send_from_directory, redirect
import os, cv2
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
EDITED_FOLDER = 'edited'
ALLOWED_EXTENSIONS = {'png','webp' ,'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EDITED_FOLDER'] = EDITED_FOLDER
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
def processimage(filename, operation, output_format):
    print(f"The operation is {operation} and file name is {filename}")
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Base name without extension
    base_name = filename.split('.')[0]
    imgProcessed = None

    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #newfilename = f"static/{base_name}.png"  
        cv2.imwrite(filename, imgProcessed)
        
    elif operation == "cblur":
        imgProcessed = cv2.GaussianBlur(img, (15, 15), 0)
        
    elif operation == "crgb":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if imgProcessed is not None:
        if output_format == "cpng":
            new_filename = f"static/{base_name}.png"
            cv2.imwrite(new_filename, imgProcessed)
        elif output_format == "cjpeg":
            new_filename = f"static/{base_name}.jpeg"
            cv2.imwrite(new_filename, imgProcessed)
        elif output_format == "cwebp":
            new_filename = f"static/{base_name}.webp"
            cv2.imwrite(new_filename, imgProcessed)
        else:
            print("Error: Unsupported output format.")
            return None
        cv2.imwrite(os.path.join(app.config['EDITED_FOLDER'], new_filename), imgProcessed)
        return new_filename
    
    else:
        print("Error: Unsupported operation.")
        return None
'''   
def processimage(filename, operation, output_format):
    print(f"The operation is {operation} and file name is {filename}")
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Base name without extension
    base_name = filename.split('.')[0]
    imgProcessed = None

    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif operation == "cblur":
        imgProcessed = cv2.GaussianBlur(img, (15, 15), 0)
    elif operation == "crgb":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if imgProcessed is not None:
        # Set output directory and format
        output_directory = 'edited'  # Make sure this folder exists
        if output_format == "cpng":
            new_filename = f"{base_name}_edited.png"
        elif output_format == "cjpeg":
            new_filename = f"{base_name}_edited.jpeg"
        elif output_format == "cwebp":
            new_filename = f"{base_name}_edited.webp"
        else:
            print("Error: Unsupported output format.")
            return None
        
        # Save processed image in edited folder
        cv2.imwrite(os.path.join(output_directory, new_filename), imgProcessed)
        return new_filename  # Return only the new filename
    else:
        print("Error: Unsupported operation.")
        return None

    
@app.route('/')
def home():
    processed_image = session.get('processed_image')  
    return render_template('index.html', processed_image=processed_image)
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/instructions')
def instrctions():
    return render_template('instructions.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['EDITED_FOLDER'], filename, as_attachment=True)



@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get('operation')
        output_format = request.form.get('format')
        
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Error! No file selected"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            newfilename = processimage(filename, operation, output_format)
            
            if newfilename:
                session['processed_image'] = newfilename  # Save just the filename
                flash(f"Your image has been processed. You can download it <a href='/{newfilename}' target='_blank'>here</a>.")
            else:
                flash("There was an error processing your image.")
                
            return redirect('/')  # Redirect to home to display processed image

    return render_template('instructions.html')
'''
@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get('operation')
        output_format = request.form.get('format')
        # return "POST request is here"
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "Error! No file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            newfilename = processimage(filename, operation, output_format)
            
            if newfilename:
                session['processed_image'] = newfilename
                flash(f"Your image has been processed <a href='/{newfilename}' target='_blank'>here</a>")
            else:
                flash("There was an error processing your image.")
            return render_template('index.html')

    return render_template('instructions.html')
'''
    
if __name__ == '__main__':
    app.run(debug=True)
