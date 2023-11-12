import {React} from 'react' 
import { useState } from 'react';


function ImageToCanvasButton (props){

 const [imageInfo,setImageInfo]=useState({
                        image : '',
                        ImageWidth:0,
                        ImageHeight:0,
                        imageSrc:''
                    })
   function InitializeImage(event) {
       
        let img = new Image()
        let newState;
        if(!event.target.files[0]) return
         setImageInfo(async () => {
            img.src = URL.createObjectURL((event.target).files[0]);
           
            img.onload = () =>{
                newState = {
                    image: img,
                    ImageWidth: img.width,
                    ImageHeight: img.height,
                    imageSrc: img.src
                }
                 props.drawUploadImage(newState)
            }
            return await newState
        })
    }
        return (
            <div className={props.className}>
            <input type="file"    onChange={InitializeImage}/>
          </div>


          
        )
}

export default ImageToCanvasButton