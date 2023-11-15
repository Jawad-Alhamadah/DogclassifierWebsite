import { React, useEffect } from "react";
import { Button, Col } from "react-bootstrap";
import { toast } from 'react-toastify';
import TutorialCard from "../HomePage/TutorialCard";
import deviceConfig from "../../deviceConfig"
import { useState } from 'react';
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//Photo by Andrej Lišakov on Unsplash

//Photo by Adrienn87 form PxHere
//<a href='https://www.freepik.com/vectors/background'>Background vector created by coolvector - www.freepik.com</a>
//<a href="https://www.freepik.com/vectors/background">Background vector created by freepik - www.freepik.com</a>


function HomeScreen(props) {

  // add text animation
  useEffect(() => {
    const firstPageTextObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const text = entry.target.querySelectorAll("div > div > span");

        if (entry.isIntersecting) {
          text.forEach((s) => s.classList.add("custom-title-main"));

          return; // if we added the class, exit the function
        }
        // We're not intersecting, so remove the class!
        text.forEach((s) => s.classList.remove("custom-title-main"));
      });
    });
    firstPageTextObserver.observe(document.querySelector(".square-wrapper"));
  }, []);


  useEffect(() => {
    switch (props.dog_or_human) {
      case "dog":
        toast.success(`Dog Detected !`, { theme: "dark", })
        break

      case "human":
        toast.success(`Person Detected !`, { theme: "dark", })
        break

      case "neither":

        toast.warning(`Image uploaded but no dog or human detected`,
          { theme: "dark", autoClose: 5000, pauseOnFocusLoss: true, pauseOnHover: true })
        break

      default:
        break

    }

  }, [props.dog_or_human])


  let mainContentLayoutClasses_mobileDevice = "flex-column-reverse d-flex text-center bg-color-white  gx-0 "
  let mainContentLayoutClasses_bigDevice = "justify-content-between row text-center bg-color-white  gx-0 "
  let minWidthBigDevice = deviceConfig.minWidthBigDevice//540

  var leftSideLayoutClasses_bigDevice = " justify-content-start custom-font-xxxlarge  custom-font-bold col-4 gx-4 custom-margin-left square-wrapper";
  var leftSideLayoutClasses_mobileDevice = "d-flex justify-content-between  custom-font-xxxlarge  custom-font-bold col-4 gx-4 custom-margin-left square-wrapper";
  //var wikiText = 'Want to learn more? Check the wikipedia page below'
  var WikiText_mobileDevice = ''
  var WikiText_bigDevice = "Want to learn more? Check the wikipedia page below"
  var leftSideTextClasses_bigDevice = "custom-margin-top-7 text-black  custom-font-bold custom-font-family capitalize"
  var leftSideTextClasses_mobileDevice = "text-black  custom-font-bold custom-font-family capitalize"

  var isMobileDevice = window.innerWidth <= minWidthBigDevice


  let [leftSideClass, setLeftSideClass] = useState(
    isMobileDevice ? leftSideLayoutClasses_mobileDevice : leftSideLayoutClasses_bigDevice)

  let [mainContentClasses, setMainContentClasses] = useState(
    isMobileDevice ? mainContentLayoutClasses_mobileDevice : mainContentLayoutClasses_bigDevice)

  let [wikiText, setWikiText] = useState(
    isMobileDevice ? WikiText_mobileDevice : WikiText_bigDevice)

  let [leftSideTextClasses, setLeftSideTextClasses] = useState(
    isMobileDevice ? leftSideTextClasses_mobileDevice : leftSideTextClasses_bigDevice)





  let wikipediaLink = "https://www.wikipedia.org"

  let human_or_dog_span = props.dog_or_human === "neither"
    ? (<span className="custom-font-xxlarge">Sorry! We couldn't detect a dog or a human.</span>)
    : (<span>you are a <span className="outline-text">{props.dog_or_human}</span> </span>)
  let breed_span = props.dog_or_human === "neither"
    ? (<span className="custom-font-xxlarge"> Please, try again with another image. </span>)
    : (<span>Your breed is <span className="outline-text">{props.breed}</span></span>)

  function resizeHandler() {

    let isMobile = window.innerWidth <= minWidthBigDevice
    if (isMobile) {
      setLeftSideClass(leftSideLayoutClasses_mobileDevice)
      setMainContentClasses(mainContentLayoutClasses_mobileDevice)
      setWikiText(WikiText_mobileDevice)
      setLeftSideTextClasses(leftSideTextClasses_mobileDevice)
      //$('#main-content').removeClass(mainContentlaptopClasses).addClass(mainContentphoneUIClasses)
      // $('#leftHalf').addClass('d-flex justify-content-between') 

      // $("#wiki-text").text(WikiText_mobile)
      // $("#left-side-html").removeClass("custom-margin-top-7")

    }

    let isLargeDevice = window.innerWidth > minWidthBigDevice
    if (isLargeDevice) {
      setLeftSideClass(leftSideLayoutClasses_bigDevice)
      setMainContentClasses(mainContentLayoutClasses_bigDevice)
      setWikiText(WikiText_bigDevice)
      setLeftSideTextClasses(leftSideTextClasses_bigDevice)
      // $('#main-content').addClass(mainContentlaptopClasses).removeClass(mainContentphoneUIClasses)
      // $('#leftHalf').removeClass('d-flex justify-content-start')           
      //$("#wiki-text").text(WikiText_bigDevice)
      // $("#left-side-html").addClass("custom-margin-top-7")
    }
  }

  window.addEventListener('resize', resizeHandler);

  let wikiLink =
    props.href === "none"
      ? null
      : (
        <div>
          <div id="wiki-text" className=" custom-font-xxlarge text-black custom-font-bold custom-font-family ">
            <span>{wikiText}</span>
          </div>

          <Button
            href={wikipediaLink + props.href}
            id="wikiButton"
            className=" custom-margin-left 
                              custom-font-size custom-font-bold custom-font-family  "
            variant="outline-danger"
          >
            Go to Wiki
          </Button>
        </div>
      );

  return (
    <div id="main-content" className={mainContentClasses}>

      <Col id="leftHalf" className={leftSideClass}>
        <div id="left-side-html" className={leftSideTextClasses}>
          <div>{human_or_dog_span}</div>
          <div>{breed_span}</div>
        </div>

        {wikiLink}
      </Col>


      <Col id="paragraphs-div">
        <TutorialCard
          image={props.image}
          dog_or_human={props.dog_or_human}
        ></TutorialCard>
      </Col>
    </div>
  );
}

export default HomeScreen;