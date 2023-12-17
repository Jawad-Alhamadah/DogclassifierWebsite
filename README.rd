# Dog Breed Classifier

A trained machine learning module that predicts dog breeds using an image.
It uses Fast Api python server and react front end to create a UI to communicate with the module.
Once the prediction is made, the server will scrap wikipedia for a link to the Dog breed.

## Installation
there are two ways to run this locally: 

#### 1. local direct install
I don't recommend this since it might install and update a few libriatires. If you have a local enviroment you don't want to mess with, its better not to do this.

But if you want to:
```bash

cd CapstoneApp
```

```bash

pip install -r requirments.txt
```
You also need the front-end dependences installed.

```bash

cd reactapp
```

```bash
npm install
```
##### Combine module
due to github limitation when handeling large files, i simply made a script to seperate the module into smaller chunks.

Navigate to the modelContainer folder and run this command:
```
python combine.py --filename model_transfer.pt --num-files 11 --ext pt --force-delete no
```
![alt text](./combine.png)
This will produce a model_transfer.pt file. move it into the "CapstoneApp" folder.

It should be in the same folder as the "server" python file.

### 2. Docker installation (recommended)

its a big project that can mess with your enviroment if you install it directly. If you are working on react or node projects locally, it might update some libraties you didn't want to update.

So instead of installing locally, use the docker-compose.yaml file instead.

insure that you have Docker-desktop and [Docker](https://docs.docker.com/engine/install/) installed first.

after installing docker, you need to combine the module into a single file.

##### Combine module
due to github limitation when handeling large files, i simply made a script to seperate the module into smaller files.

Navigate to the modelContainer folder and run this command:
```
python combine.py --filename model_transfer.pt --num-files 11 --ext pt --force-delete no
```

![alt text](./combine.png)

This will produce a model_transfer.pt file. move it into the "CapstoneApp" folder then run this command:

```
docker-compose up --build
```
this will take a while. The project will download plently of large libraries and files so go have some fun. Get lunch, watch Jojo's bizzare adventure, stare at your plants etc.

eventually, the installation will be done and the image will be up.

use this URL in a brower to connect locally to the image: 

```
http://localhost:3005/
```

