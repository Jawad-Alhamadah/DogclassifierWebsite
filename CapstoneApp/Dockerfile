FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /dogApp

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#COPY ./vgg16/vgg16-397923af.pth /root/.cache/torch/hub/checkpoints/vgg16-397923af.pth

EXPOSE 1000

#Todo  This works now. Time to create the Docker File for the react App

CMD ["python", "-m", "uvicorn", "server:app", "--proxy-headers","--host" ,"0.0.0.0","--port","1000"]

# RUN apk add build-base cmake git gtk+2.0-dev pkgconfig ffmpeg-dev

# RUN pip install starlette

# RUN pip install opencv_contrib_python

# RUN pip install opencv_python_headless




# COPY ./requirements.txt . 

# RUN pip install -r requirements.txt

#WORKDIR /dogApp

#COPY ./requirements.txt . 

#

#RUN pip install --upgrade setuptools

#

#COPY . .

#EXPOSE 8000

#CMD ["python", "-m", "uvicorn", "server:app", "--reload"]




