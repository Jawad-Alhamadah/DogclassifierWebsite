import { React, forwardRef, useState } from "react";
import ImageToCanvasButton from "./ImageToCanvasButton";
import axios from "axios";
import { createCanvas } from "canvas";
import { ToastContainer, toast } from 'react-toastify';
//import Button from "./StyleComponents/Button"
import {Row} from "react-bootstrap";
import useWindowDimensions from "../../CustomHooks/windowDimensions";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import { useHistory } from "react-router-dom";
const OSMQuery = require("../../../OSMQuerries/OSMQuerries")



const CropBar = forwardRef(function (props, ref) {
  const { height, width } = useWindowDimensions();
  const history = useHistory();
  let [isCropLoading, setIsCropLoading] = useState(false);

  async function crop(event) {
    setIsCropLoading(true)
    let ctx = ref.current.getContext("2d");
 
    //we subtract by three to avoid cropping the red outline while cropping the image
    //and we shift the corner of the crop by two to re-adjust the croping position
    let cropingWidth = props.cropRect.width - 3;
    let cropingHeight = props.cropRect.height - 3;

    //the crop position is based on window. We first center the postion by dividing by window width/height.
    //then we subtract the cropping box width and height to get the crop corner position
    let cropingPostion_X = width / 2 - props.cropRect.width / 2 + 2;
    let cropingPostion_Y = height / 2 - props.cropRect.height / 1.4 + 2;

    let imgData = ctx.getImageData(
      cropingPostion_X,
      cropingPostion_Y,
      cropingWidth,
      cropingHeight
    );
    let tempCanvas = createTemporaryImageCanvas(cropingWidth, cropingHeight, imgData);
    let  {fd,dataURL} = createFormDataFromCanvas(tempCanvas);


    
    // let MLModelResponse = await axios({
    //   method: "post",
    //   url: "http://127.0.0.1:1000",
    //   data: fd,
    //   headers: { "Content-Type": "multipart/form-data" },
    // });
    // var nearbyShelters = OSMQuery.NearbyShelters

    axios({
      method: "post",
      url: "http://192.168.1.6:1000",
      data: fd,
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then(
      (response) => {
        let href = response.data.href;
        let breed = response.data.breed;
        //let paragraphs = response.data.paragraphs;
        let dog_or_human = response.data.dog_or_human;

      
        history.push({
          pathname: "/wiki",
          search: "?query=abc",
          state: {
            breed: breed,
            href: href,
           // paragraphs: paragraphs,
            image: dataURL,
            dog_or_human: dog_or_human,
          },
        });
      },
      (error) => {
        toast.error("."+error, {
          
          theme: "dark",
          });
          
        setIsCropLoading(false)
        console.log(error);
      }
    );
  


    //var config = { headers: { "Content-Type": "text/xml" } };
   // let OSMResponse = await axios.post(
    //  "https://overpass-api.de/api/interpreter",
   //   nearbyShelters,
   //   config
    //);

    //reRouteToPage("/wiki",MLModelResponse,dataURL, OSMResponse);
  } /////////////////////

  async function drawUploadImage(data) {
   
  
    let img = data.image;

    let ctx = ref.current.getContext("2d");

    let resizedScales = resizeImage(
      img.width,
      img.height,
      ref.current.width,
      ref.current.height
    );
    let resizedImg = await createImageBitmap(img, {
      resizeWidth: resizedScales.width,
      resizeHeight: resizedScales.height,
      resizeQuality: "high",
    });
   
    ctx.drawImage(resizedImg, 0, 0);

    props.setImage(resizedImg);
  }
  //this function resizes images that far exceeds the size of the canvas.
  //this is useful to reduced the need to resize images when uploaded
  function resizeImage(imgWidth =224, imgHeight=224, canvasWidth=500, canvasHeight=500) {
    let ratio = 0.9; //default ratio incase both width and height are equal
    let isImageTooWide = width > canvasWidth;
    let isImageTooLong = height > canvasHeight;
    if (imgWidth > imgHeight) ratio = imgWidth / imgHeight;
    if (imgWidth < imgHeight) ratio = imgHeight / imgWidth;

    while (isImageTooWide || isImageTooLong) {
      isImageTooWide = imgWidth > canvasWidth;
      isImageTooLong = imgHeight > canvasHeight;

      if (imgWidth > imgHeight) {
        imgWidth = imgWidth - ratio * 5;
        imgHeight = imgHeight - 5;
        continue
      }

       imgWidth = imgWidth - 5;
       imgHeight = imgHeight - ratio * 5;
    }
    return { width: imgWidth, height: imgHeight };
  }

  function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(",")[0].indexOf("base64") >= 0)
      byteString = atob(dataURI.split(",")[1]);
    else byteString = unescape(dataURI.split(",")[1]);

    // separate out the mime component
    var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], { type: mimeString });
  }

  function createFormDataFromCanvas(tempCanvas) {
    var dataURL = tempCanvas.toDataURL("image/jpeg", 0.5);
    var blob = dataURItoBlob(dataURL);
    var fd = new FormData();
  
    fd.append("canvasImage", blob);
    return { fd, dataURL };
  }
  
  function createTemporaryImageCanvas(cropingWidth, cropingHeight, imgData) {
    let tempCanvas = createCanvas(cropingWidth, cropingHeight);
    let tempCtx = tempCanvas.getContext("2d");
    tempCtx.putImageData(imgData, 0, 0);
    return tempCanvas;
  }

  function reRouteToPage( path,response,dataURL, res) {
    let href =   response.data.href;
    let breed = response.data.breed;
    let dog_or_human = response.data.dog_or_human;
    
    history.push({
      pathname:path,
      search: "?query=abc",
      state: {
        breed: breed,
        href: href,
        // paragraphs: paragraphs,
        image: dataURL,
        dog_or_human: dog_or_human,
        locations: res.data.elements,
      },
    });
  }

    let cropButtonTextSpan = isCropLoading? <div>
                                             <span >Loading...</span>
                                             <span class=" spinner-border spinner-border-sm"></span>
                                            </div>
                                           :<span >Check dog breed</span>
  
  return (
    <div>
     
      <Row className="row justify-content-center pt-3  p-0 g-0">
        <ImageToCanvasButton
          drawUploadImage={drawUploadImage}
          className="col-2 bg-secondary m-1"
        />
        <Button
          onClick={crop}
          className="col-12 "
          variant="outline-warning"
          style={{ maxWidth: "15rem" }}
        >
          {cropButtonTextSpan}
        </Button>
      </Row>
    </div>
  );
});

export default CropBar;




