import { React, useRef, useState, useEffect } from "react";
import CropToolsSection from "./MainComponents/CropToolsSection";
import CanvasArea from "./MainComponents/CanvasArea";
import NavBar from "./MainComponents/NavBar.js";
import { ToastContainer, toast } from 'react-toastify';
import { Slide, Zoom, Flip, Bounce } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import $ from"jquery"
function MainContent() {
  const canvas = useRef(null);
  const slider = useRef(null);
  let [image, setImage] = useState("");
  let [scale, setScale] = useState(1);

  useEffect(() => {
    setScale(slider.current.value);
  }, []);

  function handleSlide() {
    setScale(slider.current.value);
  }
  let cropRect = { x: 500, y: 300, width: 400, height: 400 };

  
  


  return (
    <div>
      
      <NavBar backgroundColor="mid-purple" />
     
      <div id="main">
        <div id="nav-and-tools-div">
          <div
            className=" text-warning custom-padding-top-1  
                        custom-font-size-small custom-font-bold 
                        custom-font-family 
                        capitalize center-text"
          >
            For best results, Include as much of the dog / human as possible. 
          </div>
          <CropToolsSection
            ref={canvas}
            cropRect={cropRect}
            setImage={setImage}
          />
          <label for="customRange1" class="form-label">
            .
          </label>
          <input
            ref={slider}
            type="range"
            class="form-range"
            id="customRange1"
            onChange={handleSlide}
          ></input>
        </div>
        <CanvasArea
          ref={canvas}
          sliderScale={scale}
          image={image}
          cropRect={cropRect}
          width={"500%"}
          height={"500%"}
          setImage={setImage}
        />
      </div>
    </div>
  );
}

export default MainContent;
