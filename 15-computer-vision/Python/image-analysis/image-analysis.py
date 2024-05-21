# import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
import os
from array import array
from PIL import Image, ImageDraw
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Azure AI Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)


        # Analyze image
        AnalyzeImage(image_file)

        # Generate thumbnail
        GetThumbnail(image_file)

    except Exception as ex:
        print(ex)

def AnalyzeImage(image_file):
    print('Analyzing', image_file)

    # Specify features to be retrieved
    features = [VisualFeatureTypes.description,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.categories,
                VisualFeatureTypes.brands,
                VisualFeatureTypes.objects,
                VisualFeatureTypes.adult]
    

    # Get image analysis
    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data , features)
        # Get image description
    for caption in analysis.description.captions:
        print("Description: '{}' (confidence: {:.2f}%)".format(caption.text,caption.confidence * 100))
        
    # Get image tags
    if (len(analysis.tags) > 0):
        print("Tags: ")
    for tag in analysis.tags:
        print(" -'{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence* 100))
    def GetThumbnail(image_file):
        print('Generating thumbnail')

    # Get image categories
    if (len(analysis.categories) > 0):
        print("Categories:")
    landmarks = []
    for category in analysis.categories:
    # Print the category
        print(" -'{}' (confidence: {:.2f}%)".format(category.name,
    category.score * 100))
    if category.detail:
    # Get landmarks in this category
        if category.detail.landmarks:
            for landmark in category.detail.landmarks:
                if landmark not in landmarks:landmarks.append(landmark)
    # If there were landmarks, list them
    if len(landmarks) > 0:
        print("Landmarks:")
    for landmark in landmarks:
        print(" -'{}' (confidence: {:.2f}%)".format(landmark.name,landmark.confidence * 100))

        # Get brands in the image
    if (len(analysis.brands) > 0):
        print("Brands: ")
    for brand in analysis.brands:
        print(" -'{}' (confidence: {:.2f}%)".format(brand.name,brand.confidence * 100))
    
    # Get moderation ratings
    ratings = 'Ratings:\n -Adult: {}\n -Racy: {}\n -Gore:{}'.format(analysis.adult.is_adult_content,analysis.adult.is_racy_content,analysis.adult.is_gory_content)
    print(ratings)
    # Generate a thumbnail
    with open(image_file, mode="rb") as image_data:
    # Get thumbnail data
        thumbnail_stream = cv_client.generate_thumbnail_in_stream(100, 100,image_data, True)
    # Save thumbnail image
    thumbnail_file_name = 'thumbnail.png'
    with open(thumbnail_file_name, "wb") as thumbnail_file:
        for chunk in thumbnail_stream:thumbnail_file.write(chunk)
        print('Thumbnail saved in.', thumbnail_file_name)



if __name__ == "__main__":
    main()
