from fastapi import FastAPI,UploadFile,File
import requests
from starlette.responses import JSONResponse
import cv2                     
import numpy as np
import torch
import torchvision.models as models
from PIL import Image
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
import cv2
import numpy as np
from bs4 import BeautifulSoup
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
import random
from pydantic import BaseModel,BaseConfig
import datetime
from unidecode import unidecode
import os

#toDO Download the Path vgg16. Then copy it into the correct place. 
#Todo, hopefully, that would stop the long download time from the server every time.

def scrap(url):
    page = requests.get(url) #url
    src = page.content
    soup = BeautifulSoup(src,'lxml')
    return soup


#BaseConfig.arbitrary_types_allowed = True
#python -m uvicorn server:app --reload
# or run this:    python -m uvicorn server:app --proxy-headers --host 0.0.0.0 --port 1000

breeds_dict ={0: 'Affenpinscher', 1: 'Afghan_hound', 2: 'Airedale_terrier', 3: 'Akita', 4: 'Alaskan_malamute', 5: 'American_eskimo_dog', 6: 'American_foxhound', 7: 'American_staffordshire_terrier', 8: 'American_water_spaniel', 9: 'Anatolian_shepherd_dog', 10: 'Australian_cattle_dog', 11: 'Australian_shepherd', 12: 'Australian_terrier', 13: 'Basenji', 14: 'Basset_hound', 15: 'Beagle', 16: 'Bearded_collie', 17: 'Beauceron', 18: 'Bedlington_terrier', 19: 'Belgian_malinois', 20: 'Belgian_sheepdog', 21: 'Belgian_tervuren', 22: 'Bernese_mountain_dog', 23: 'Bichon_frise', 24: 'Black_and_tan_coonhound', 25: 'Black_russian_terrier', 26: 'Bloodhound', 27: 'Bluetick_coonhound', 28: 'Border_collie', 29: 'Border_terrier', 30: 'Borzoi', 31: 'Boston_terrier', 32: 'Bouvier_des_flandres', 33: 'Boxer', 34: 'Boykin_spaniel', 35: 'Briard', 36: 'Brittany', 37: 'Brussels_griffon', 38: 'Bull_terrier', 39: 'Bulldog', 40: 'Bullmastiff', 41: 'Cairn_terrier', 42: 'Canaan_dog', 43: 'Cane_corso', 44: 'Cardigan_welsh_corgi', 45: 'Cavalier_king_charles_spaniel', 46: 'Chesapeake_bay_retriever', 47: 'Chihuahua', 48: 'Chinese_crested', 49: 'Chinese_shar-pei', 50: 'Chow_chow', 51: 'Clumber_spaniel', 52: 'Cocker_spaniel', 53: 'Collie', 54: 'Curly-coated_retriever', 55: 'Dachshund', 56: 'Dalmatian', 57: 'Dandie_dinmont_terrier', 58: 'Doberman_pinscher', 59: 'Dogue_de_bordeaux', 60: 'English_cocker_spaniel', 61: 'English_setter', 62: 'English_springer_spaniel', 63: 'English_toy_spaniel', 64: 'Entlebucher_mountain_dog', 65: 'Field_spaniel', 66: 'Finnish_spitz', 67: 'Flat-coated_retriever', 68: 'French_bulldog', 69: 'German_pinscher', 70: 'German_shepherd_dog', 71: 'German_shorthaired_pointer', 72: 'German_wirehaired_pointer', 73: 'Giant_schnauzer', 74: 'Glen_of_imaal_terrier', 75: 'Golden_retriever', 76: 'Gordon_setter', 77: 'Great_dane', 78: 'Great_pyrenees', 79: 'Greater_swiss_mountain_dog', 80: 'Greyhound', 81: 'Havanese', 82: 'Ibizan_hound', 83: 'Icelandic_sheepdog', 84: 'Irish_red_and_white_setter', 85: 'Irish_setter', 86: 'Irish_terrier', 87: 'Irish_water_spaniel', 88: 'Irish_wolfhound', 89: 'Italian_greyhound', 90: 'Japanese_chin', 91: 'Keeshond', 92: 'Kerry_blue_terrier', 93: 'Komondor', 94: 'Kuvasz', 95: 'Labrador_retriever', 96: 'Lakeland_terrier', 97: 'Leonberger', 98: 'Lhasa_apso', 99: 'Lowchen', 100: 'Maltese', 101: 'Manchester_terrier', 102: 'Mastiff', 103: 'Miniature_schnauzer', 104: 'Neapolitan_mastiff', 105: 'Newfoundland', 106: 'Norfolk_terrier', 107: 'Norwegian_buhund', 108: 'Norwegian_elkhound', 109: 'Norwegian_lundehund', 110: 'Norwich_terrier', 111: 'Nova_scotia_duck_tolling_retriever', 112: 'Old_english_sheepdog', 113: 'Otterhound', 114: 'Papillon', 115: 'Parson_russell_terrier', 116: 'Pekingese', 117: 'Pembroke_welsh_corgi', 118: 'Petit_basset_griffon_vendeen', 119: 'Pharaoh_hound', 120: 'Plott', 121: 'Pointer', 122: 'Pomeranian', 123: 'Poodle', 124: 'Portuguese_water_dog', 125: 'Saint_bernard', 126: 'Silky_terrier', 127: 'Smooth_fox_terrier', 128: 'Tibetan_mastiff', 129: 'Welsh_springer_spaniel', 130: 'Wirehaired_pointing_griffon', 131: 'Xoloitzcuintli', 132: 'Yorkshire_terrier'}
#allowed origins
##
#origins = ["http://localhost:3000","https://en.wikipedia.org"]
origins = ["http://localhost:3005","http://localhost:3006","https://en.wikipedia.org","http://192.168.1.6:3005"]
soup = scrap(url ="https://en.wikipedia.org/wiki/List_of_dog_breeds")
links =  soup.select("#mw-content-text > .mw-parser-output > div > ul > li > a")


#the response object
class WikiPage (BaseModel):
    breed :str
    href : str
   # paragraphs: list[str] = []
    dog_or_human:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
		allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=3600
)

#this function scraps a url and returns the Soup object that we can query for elements



@app.get("/sys/scrapWiki")
async def updateWiki ():
  
    soup = scrap(url ="https://en.wikipedia.org/wiki/List_of_dog_breeds")
    print("gs",links)
    links =  soup.select("#mw-content-text > .mw-parser-output > div > ul > li > a")
    print()
    return


@app.post("/",response_class=JSONResponse , response_model=WikiPage)
async def home(canvasImage: UploadFile = File(...)):
    print("... ... ... ...")
    #save the image to the server temporarily. we use time stamp to prevent overwriting images
    time_stamp = str(datetime.datetime.now()).split('.')[0].replace(" ","-").replace(":","-")
    temp_dog_image_path= f"upload\\dogImage-{time_stamp}.jpeg"
   
    #write image
    with open(temp_dog_image_path,"wb") as buffer:
        buffer.write(canvasImage.file.read())

    #make a prediction with the imageS
    prediction = run_app(temp_dog_image_path)
    breed= prediction[0]
    dog_or_human = prediction[1]
    print(dog_or_human)
    if(dog_or_human =="neither"):
            return WikiPage( breed = "neither" , href="none" ,dog_or_human=dog_or_human)


    dog_name = breed.replace('_'," ").lower()
    dog_name = dog_name.replace("-"," ").lower()

    
   
    
    #scrap wikipedia list of dog breeds for a link to the predicted breed
    #soup = scrap(url ="https://en.wikipedia.org/wiki/List_of_dog_breeds")
   #links =  soup.select("#mw-content-text > .mw-parser-output > div > ul > li > a") 
    
    link_to_breed_wiki =""
    data = []

    #cycle through the breed links to find one that matches
    for link in links:
        if link.get("title") is not None:

            #case names to lower case 
            #dog_name = breed.replace('_'," ").lower()
           # dog_name = dog_name.replace("-"," ").lower()
            dog_title =link.get("title").lower()
            if dog_name in unidecode(dog_title)  or  unidecode(dog_title)  in dog_name :
                 link_to_breed_wiki = link.get('href')
                 data.append({"breed":dog_name,"href":link_to_breed_wiki})
    
    #the model produces a breed that is more generalized than the wikipedia list we are scrapping.
    #for example, the model can predict a bulldog but wikipedia has atleast 7 sub-types of bulldog. We have no way to know which
    #refers to the one we are looking for.
    #because of this, we create a list of bulldogs and then pick which one to show randomly.
    random_sub_breed = random.randint(0,len(data)-1)
   
    selected_breed = data[random_sub_breed]

    #future improvent is to scrap the wiki for paragraphs of information. We leave that for the future.
    
    # soup = scrap(url =f"https://en.wikipedia.org{selected_breed['href']}")
    # Titleheading = soup.select("#firstHeading")
    # paragraphs = soup.select("p")
    # sub_headings = soup.select(".mw-headline")
    # unwanted_heading_ids ={"See_also","References", "External_links"}
    # sub_headings = [x for x in sub_headings if x.get("id") not in unwanted_heading_ids]
    # selected_breed["paragraphs"] = [x.text for x in paragraphs]
    #, paragraphs=selected_breed["paragraphs"]

    print(prediction)
    os.remove(temp_dog_image_path)
    return WikiPage( breed = selected_breed["breed"] , href=selected_breed["href"] ,dog_or_human=dog_or_human)

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

image_dim= 224
use_cuda = torch.cuda.is_available()
transform={}
transform["train"] = transforms.Compose([        
        transforms.Resize(image_dim),                    
        transforms.CenterCrop(image_dim),
      #  transforms.RandomGrayscale(p=1),
        transforms.RandomRotation(degrees=(0, 90)),
        transforms.RandomPosterize(bits=2),
        transforms.RandomAdjustSharpness(sharpness_factor=0.4, p=0.5),
        transforms.RandomEqualize(p=0.3),
        transforms.RandomAutocontrast(p=0.1),
        transforms.RandomHorizontalFlip(p=0.6),
        transforms.RandomPerspective(distortion_scale=0.7, p=0.2),
       # transforms.RandomAffine(degrees=(30, 70), translate=(0.1, 0.3), scale=(0.5, 0.75)),
        transforms.RandomInvert (p=0.1),
        transforms.RandomVerticalFlip(p=0.01),
        transforms.ColorJitter(brightness=0.4),
        transforms.ToTensor(),                    
        transforms.Normalize(                      
            mean=[0.485, 0.456, 0.406],              
            std=[0.229, 0.224, 0.225]                  
            )
        ])

transform["valid"] = transforms.Compose([
        #transforms.RandomGrayscale(p=1),
        transforms.Resize(image_dim),                    
        transforms.CenterCrop(image_dim),
        transforms.ToTensor(),                    
        transforms.Normalize(                      
            mean=[0.485, 0.456, 0.406],              
            std=[0.229, 0.224, 0.225]                  
            )
        ])


VGG16 = models.vgg16(pretrained=True)
if use_cuda:
    VGG16 = VGG16.cuda()
next(VGG16.parameters()).is_cuda

def face_detector(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0     

def dog_detector(img_path):
    max_dog_index = 268
    min_dog_index = 151
    prediction = VGG16_predict(img_path) 
    return prediction >= min_dog_index and prediction <= max_dog_index


def predict_breed_transfer(img_path):
    # load the image and return the predicted breed
    model_transfer.eval()
    target =torch.Tensor([5])
    target = torch.stack(tuple(target))
    data=[]
    image = Image.open(img_path)
    transformed_data= transform["valid"](image).cuda()
    data.append(transformed_data)
    data = torch.stack(data)
    
    if use_cuda:
        data, target = data.cuda(), target.cuda()
    output = model_transfer(data)
    pred = output.data.max(1, keepdim=True)[1]
    return breeds_dict[pred.item()]



def VGG16_predict(img_path):
 
    image=Image.open(img_path)
    transform = transforms.Compose([        
        transforms.Resize(256),                    
        transforms.CenterCrop(224),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),                    
        transforms.Normalize(                      
            mean=[0.485, 0.456, 0.406],              
            std=[0.229, 0.224, 0.225]                  
            )
        ])
    img_tensor = transform(image)
    batch = (img_tensor.unsqueeze(0)).cuda()

    prediction = VGG16(batch)
    prediction=prediction.cpu().detach().numpy()
    prediction = np.argmax(prediction)
    return prediction







model_transfer = models.vgg16(pretrained=True)
for par in model_transfer.parameters():
     par.requires_grad= False
model_transfer.classifier[6]=nn.Linear(model_transfer.classifier[6].in_features,133)


use_cuda = torch.cuda.is_available()
if use_cuda:
    model_transfer = model_transfer.cuda()
    




model_transfer.load_state_dict(torch.load('model_transfer.pt'))
criterion_transfer = nn.CrossEntropyLoss()
optimizer_transfer = optim.Adam(model_transfer.parameters(),lr=0.0001) 
 
def predict_breed_transfer(img_path):
    # load the image and return the predicted breed
    model_transfer.eval()
    target =torch.Tensor([5])
    target = torch.stack(tuple(target))
    data=[]
    image = Image.open(img_path)
    transformed_data= transform["valid"](image).cuda()
    data.append(transformed_data)
    data = torch.stack(data)
    
    if use_cuda:
        data, target = data.cuda(), target.cuda()
    output = model_transfer(data)
    pred = output.data.max(1, keepdim=True)[1]
    return breeds_dict[pred.item()]


def run_app(img_path):
     
    #image=Image.open(img_path)
   # plt.imshow(image)
    #plt.show(image)
    #print(img_path)

    is_dog = dog_detector(img_path)
    if is_dog:
    
        return (predict_breed_transfer(img_path),"dog")
    

    is_human = face_detector(img_path)
    if is_human:
        return (predict_breed_transfer(img_path),"human")
   

    return ("neither","neither")

