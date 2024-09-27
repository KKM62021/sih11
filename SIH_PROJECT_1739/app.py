import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from datetime import datetime
import suncalc

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploaded'
CONVERT_FOLDER = 'converted'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(CONVERT_FOLDER):
    os.makedirs(CONVERT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERT_FOLDER'] = CONVERT_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    sun_azimuth = None
    sun_elevation = None

    if request.method == "POST":
        # Handle file upload
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)

        # Handle date and time input
        if 'datetime' in request.form:
            try:
                user_datetime = request.form['datetime']
                date_time = datetime.strptime(user_datetime, '%Y-%m-%d %H:%M')
                latitude = 23.0225  # Your location
                longitude = 72.5714  # Your location

                # Get the sun position
                sun_position = suncalc.get_position(date_time, latitude, longitude)
                sun_azimuth = sun_position['azimuth'] * (180 / 3.14159)
                sun_elevation = sun_position['altitude'] * (180 / 3.14159)
                print(sun_azimuth, sun_elevation)

                # Adjust azimuth
                sun_azimuth = (sun_azimuth + 180) % 360

            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD HH:MM format.')

    # List uploaded files
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", uploaded_files=uploaded_files, sun_azimuth=sun_azimuth, sun_elevation=sun_elevation)

@app.route("/uploaded/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/visualize")
def visualize():
    return render_template("visualize.html")


@app.route("/convert", methods=["GET", "POST"])
def convert():
    if request.method == "POST":
        # Handle file upload for conversion
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            
            file_ext = os.path.splitext(file.filename)[1].lower()
            allowed_exts = ['.shp', '.dem', '.gbl', '.obj', '.json', '.geojson']
            if file_ext not in allowed_exts:
                flash(f"Unsupported file format: {file_ext}")
                return redirect(request.url)

            input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_path)

            # Create the output file name for the GLTF file
            output_filename = os.path.splitext(file.filename)[0] + ".gltf"
            output_path = os.path.join(app.config['CONVERT_FOLDER'], output_filename)

            # Call the conversion function
            try:
                convert_to_gltf(input_path, output_path)
                flash(f"File converted successfully to {output_filename}")
                return redirect(url_for('download_converted_file', filename=output_filename))
            except Exception as e:
                flash(f"Conversion failed: {str(e)}")
                return redirect(request.url)

    return render_template("convert.html")

@app.route("/converted/<filename>")
def download_converted_file(filename):
    return send_from_directory(app.config['CONVERT_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
