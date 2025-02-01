from flask import Flask, render_template, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Folder where images are stored
images_folder = "images"
caption_file = "captions.txt"


# Read captions from file
def load_captions():
    captions = {}
    if os.path.exists(caption_file):
        with open(caption_file, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    captions[parts[0]] = parts[1]
    return captions


# Get list of image files in the images folder
def get_image_files():
    if os.path.exists(images_folder):
        return [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return []


# API to fetch images and captions
@app.route("/api/images", methods=["GET"])
def get_images():
    captions = load_captions()
    image_files = get_image_files()

    # Create list of image-caption pairs
    slides = [
        {
            "image": f"/images/{image}",  # Path to access image
            "caption": captions.get(image, "A special moment ❤")  # Default caption if not found
        }
        for image in image_files
    ]
    return jsonify(slides)


# Serve image files from the 'images' folder
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(images_folder, filename)


# Main route to serve the HTML frontend
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # Ensure the images folder exists
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    app.run(debug=True)
