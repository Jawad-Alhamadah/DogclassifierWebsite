import { React, forwardRef, useEffect, useState } from "react";
import useWindowDimensions from "../../CustomHooks/windowDimensions";
//import deviceConfig from "../../../deviceConfig"
const CanvasArea = forwardRef(function (props, ref) {
  //let [image, setImage] = useState(props.image);
  let [scale, setScale] = useState(1);
  const { height, width } = useWindowDimensions();
  let [ctx, setCtx] = useState("");
  let [isMouseDown, setIsMouseDown] = useState(false);
  let [resizedImage, setResizedImage] = useState(undefined);
  let [isMount, setIsMount] = useState(false);
  let [postion, setPostion] = useState({
    x: 0,
    y: 0,
    PrevX: 0,
    PrevY: 0,
  });

  useEffect(() => {
    setCtx(ref.current.getContext("2d", { willReadFrequently: true }));
    setScale(props.sliderScale);
  }, []);

  useEffect(() => {
    setScale(props.sliderScale);
    if (props.image !== "") rescaleImage();
  }, [props.sliderScale]);
  async function rescaleImage() {
    let ratio = (scale - 50) / 70;
    ctx.fillStyle = "#262a31";
    ctx.fillRect(0, 0, width, height);
    let resizedImg = await createImageBitmap(props.image, {
      resizeWidth: Math.ceil(props.image.width + props.image.width * ratio),
      resizeHeight: Math.ceil(props.image.height + props.image.height * ratio),
      resizeQuality: "high",
    });
    setResizedImage(resizedImg);
    ctx.drawImage(resizedImg, postion.x, postion.y);
    let centered_X = width / 2 - props.cropRect.width / 2;
    let centered_Y = height / 2 - props.cropRect.height / 1.4;

    let unshadedArea = ctx.getImageData(
      centered_X,
      centered_Y,
      props.cropRect.width,
      props.cropRect.height
    );

    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, width, height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "Red";
    ctx.putImageData(unshadedArea, centered_X, centered_Y);
    ctx.strokeRect(
      centered_X,
      centered_Y,
      props.cropRect.width,
      props.cropRect.height
    );
  }

  useEffect(() => {

  }, []);
  useEffect(() => {
    if (props.image !== "") props.setImage(props.image);
  }, [props, props.image]);

  useEffect(() => {
    if (props.image !== "") rescaleImage();
  }, [props.image]);

  useEffect(() => {
    if (props.image !== "") rescaleImage();
  }, [width, height, props.image]);


  async function handleMouseDown(event) {

    var clientY;
    var clientX;
    if (event.touches) {
      clientY = Math.round(event.touches[0].clientY)
      clientX = Math.round(event.touches[0].clientX)
    }
    else {
      clientY = event.clientY
      clientX = event.clientX
    }
    //console.log(event)
    // event.preventDefault()
    setPostion((prevState) => ({
      ...prevState,
      PrevX: clientX,
      PrevY: clientY,
    }));
    setIsMouseDown(true);
  }

  function handleMouseUp(event) {
    //console.log(event)
    // event.preventDefault()
    setIsMouseDown(false);
  }
  function handleMouseMove(event) {

    var clientY;
    if (event.touches) clientY = Math.round(event.touches[0].clientY)
    else { clientY = event.clientY }

    //console.log(clientY)
    // event.preventDefault()
    if (isMouseDown && props.image !== "") drawCanvasImage(event);
    //if (event.clientY < 195) setIsMouseDown(false);
    if (clientY < 195) setIsMouseDown(false);
  }
  async function drawCanvasImage(event) {
    var clientY;
    var clientX;
    if (event.touches) {
      clientY = Math.round(event.touches[0].clientY)
      clientX = Math.round(event.touches[0].clientX)
    }
    else {
      clientY = event.clientY
      clientX = event.clientX
    }

    let ratio = (scale - 50) / 70;
    let resizedImg;
    if (!isMount) {
      setIsMount(true);

      resizedImg = await createImageBitmap(props.image, {
        resizeWidth: Math.ceil(props.image.width + props.image.width * ratio),
        resizeHeight: Math.ceil(props.image.height + props.image.height * ratio),
        resizeQuality: "high",
      });
      setResizedImage(resizedImg);
    } else {
      resizedImg = resizedImage;
    }


    let centered_X = width / 2 - props.cropRect.width / 2;
    let centered_Y = height / 2 - props.cropRect.height / 1.4;
    ctx.fillStyle = "#262a31";
    ctx.fillRect(0, 0, width, height);
    let imgX = postion.x + (clientX - postion.PrevX);
    let imgY = postion.y + (clientY - postion.PrevY);

    ctx.drawImage(resizedImg, imgX, imgY);
    if (isMouseDown)
      setPostion((prevState) => ({
        ...prevState,
        PrevX: clientX,
        PrevY: clientY,
        x: imgX,
        y: imgY,
      }));
    let unshadedArea = ctx.getImageData(
      centered_X,
      centered_Y,
      props.cropRect.width,
      props.cropRect.height
    );

    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, width, height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "Red";
    ctx.putImageData(unshadedArea, centered_X, centered_Y);
    ctx.strokeRect(
      centered_X,
      centered_Y,
      props.cropRect.width,
      props.cropRect.height
    );
  }

  return (
    <canvas
      ref={ref}
      width={width}
      height={height - 200}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseMove={handleMouseMove}

      onTouchStart={handleMouseDown}
      onTouchEnd={handleMouseUp}
      onTouchMove={handleMouseMove}
    ></canvas>
  );
});

export default CanvasArea;
