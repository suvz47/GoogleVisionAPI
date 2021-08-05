import configparser
import io
import os
from google.cloud import vision


config = configparser.ConfigParser()
config.read('./config.ini')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './' + config["CREDENTIALS"]["GOOGLE_APPLICATION_CREDENTIALS"]


def image_label(image_path, url=False):
    client = vision.ImageAnnotatorClient()
    if url == False:
        file_name = os.path.abspath(image_path)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    if url == True:
        image = vision.Image()
        image.source.image_uri = image_path

    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_data = [label.description for label in labels]

    return label_data

with open('./results.txt', 'w') as f:
    f.write("")

images_list = config["LOCAL_IMAGES"].keys()


print("Analyzing Local Images...")
with open('./results.txt', 'a') as f:
    f.write("Analyzing Local Images...\n")

for image_key in images_list:

    try:
        result = image_label('./images/' + config["LOCAL_IMAGES"][image_key])
        if len(result) == 0:
            result = ["No data found after analysis"]
        data = image_key + " : " + ','.join(result) + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(data)
        with open('./results.txt', 'a') as f:
            f.write(data.replace("~", ""))
    except:
        print(f"{image_key} could not be analyzed, skipping...")


url_list = config["IMAGE_LINKS"].keys()


print("\nAnalyzing Image from URLs...")
with open('./results.txt', 'a') as f:
    f.write("\nAnalyzing Image from URLs..\n")

for url_key in images_list:
    try:
        result = image_label(config["IMAGE_LINKS"][url_key], url= True)
        if len(result) == 0:
            result = ["No data found after analysis"]
        data = url_key + " : " + ','.join(result) + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print(data)
        with open('./results.txt', 'a') as f:
            f.write(data.replace("~", ""))
    except:
        print(f"{url_key} could not be analyzed, skipping...")


