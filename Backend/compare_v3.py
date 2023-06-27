from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request
from flask_cors import CORS
import shutil
import os
from PIL import Image
import io
import base64
import zipfile

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return 'Welcome to the image comparison API!'

@app.route('/compare', methods=['POST'])
def compare():
    # Check if the 'image1' and 'image2' files were uploaded
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({
            'result': 'failure',
            'message': 'Please upload two images.'
        })

    # Get the uploaded images
    image1 = request.files['image1']
    image2 = request.files['image2']

    # Save the uploaded images to the server
    image1_path = os.path.join(app.config['UPLOAD_FOLDER'], image1.filename)
    image2_path = os.path.join(app.config['UPLOAD_FOLDER'], image2.filename)
    image1.save(image1_path)
    image2.save(image2_path)

    # Load the images
    image2 = Image.open(image2_path)
    image1 = Image.open(image1_path)
    compared_image_red, compared_image_green, column, row = compare_images(image1, image2)

    # Generate ZIP files
    zip_path_red = generate_zip(compared_image_red, "red")
    zip_filename_red = 'sub_images_red.zip'
    zip_path_green = generate_zip(compared_image_green, "green")
    zip_filename_green = 'sub_images_green.zip'

    # Encode compared images as base64 strings
    compared_image_base64_red = image_to_base64(compared_image_red)
    compared_image_base64_green = image_to_base64(compared_image_green)

    return jsonify({
        'result': 'success',
        'message': 'Image comparison completed.',
        'column': column,
        'row': row,
        'compared_image_red': compared_image_base64_red,
        'zip_path_red': zip_path_red,
        'zip_filename_red': zip_filename_red,
        'compared_image_green': compared_image_base64_green,
        'zip_path_green': zip_path_green,
        'zip_filename_green': zip_filename_green
    })

def compare_images(image1, image2):
    sub_images1 = divide_image(image1)
    sub_images2 = divide_image(image2)

    height, width= image1.size
    column, row= height//10, width//10

    subheight, subwidth = sub_images1[0].size
    new_image_greenfinal = Image.new("RGB", (height, width), (0,0,0,0))
    new_image_redfinal = Image.new("RGB", (height, width), (0,0,0,0))
    u,v = 0,0
    for i in range(len(sub_images2)):
        
        new_image_red = Image.new("RGB", (subheight, subwidth), (0,0,0,0))
        new_image_green = Image.new("RGB", (subheight, subwidth), (0,0,0,0))
        for x in range(subheight):
          for y in range(subwidth):
            try:
                pixel1 = sub_images1[i].getpixel((x, y))
                pixel2 = sub_images2[i].getpixel((x, y))
            except IndexError:
                # When the image width or height is different,
                # there will be some pixels at the end of the image
                # that will not have a corresponding pixel in the other image.
                # In this case, we just skip those pixels.
                continue

            if pixel1 != pixel2:
                new_image_green.putpixel((x, y), (0,255, 0))
                new_image_red.putpixel((x, y), (255,0, 0))
            elif pixel1==(0,0,0):
                continue
            else:
                new_image_green.putpixel((x, y), pixel1)
                new_image_red.putpixel((x, y), pixel1)

        if u == column*10:
          v += subheight
          u = 0
        new_image_greenfinal.paste(new_image_green, (u,v))
        new_image_redfinal.paste(new_image_red, (u,v))
        u += subwidth
    return new_image_redfinal, new_image_greenfinal, column, row

def generate_zip(compared_image, colour):
    # Create a temporary directory to store the sub images
    temp_directory = f'temp_sub_images_{colour}'
    os.makedirs(temp_directory, exist_ok=True)

    # Save the sub images of differences
    sub_images = divide_image(compared_image)
    for i, sub_image in enumerate(sub_images):
        sub_image_path = os.path.join(temp_directory, f'difference_{i+1}.png')
        sub_image.save(sub_image_path)

    # Create a zip file containing the sub images
    zip_path = f'sub_images_{colour}.zip'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for root, _, files in os.walk(temp_directory):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=os.path.basename(file_path))

    shutil.rmtree(temp_directory)

    return zip_path

def divide_image(image):
    width, height = image.size
    sub_width = 10
    sub_height = 10
    sub_images = []

    for i in range(height // 10):
        for j in range(width // 10):
            left = j * sub_width
            upper = i * sub_height
            right = left + sub_width
            lower = upper + sub_height
            sub_image = image.crop((left, upper, right, lower))
            sub_images.append(sub_image)

    return sub_images

def image_to_base64(image):
    # Convert PIL image to base64-encoded string
    buffered = io.BytesIO()
    image.save(buffered, format='PNG')
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_image

@app.route('/download_zip', methods=['GET'])
def download_zip():
    zip_path = request.args.get('zip_path')
    zip_filename = request.args.get('zip_filename')
    directory = os.path.dirname(zip_path)
    return send_from_directory(directory='', path=zip_path, as_attachment=True, download_name=zip_filename)

if __name__ == '__main__':
    app.run()
