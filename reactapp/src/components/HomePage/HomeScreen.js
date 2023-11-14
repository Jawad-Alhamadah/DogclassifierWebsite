import { React, useEffect } from "react";
import { Row, Button, Col } from "react-bootstrap";
import { ToastContainer, toast } from 'react-toastify';
import TutorialCard from "../HomePage/TutorialCard";
import deviceConfig from "../../deviceConfig"
import $ from"jquery"
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//Photo by Andrej Lišakov on Unsplash

//Photo by Adrienn87 form PxHere
//<a href='https://www.freepik.com/vectors/background'>Background vector created by coolvector - www.freepik.com</a>
//<a href="https://www.freepik.com/vectors/background">Background vector created by freepik - www.freepik.com</a>




function HomeScreen(props) {
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
  

  let phoneUIClasses = "flex-column-reverse d-flex"
  let laptopClasses = "justify-content-between row"
  let minWidthBigDevice = deviceConfig.minWidthBigDevice//540
  var mainContentLayoutClasses; 
  var leftSideLayoutClasses;
  var leftSideHtml;
  var wikiText = 'Want to learn more? Check the wikipedia page below'
  var mobileWikiText= ''
  var laptopWikiText= "Want to learn more? Check the wikipedia page below" 
  var isMobileDevice = $(window).width() <= minWidthBigDevice
  var isBigDevice = $(window).width() > minWidthBigDevice

 
  let wikipediaLink ="https://www.wikipedia.org"

  let human_or_dog_span = props.dog_or_human === "neither" 
                                              ? (<span className="custom-font-xxlarge">Sorry! We couldn't detect a dog or a human.</span>)
                                              : (<span>you are a <span className="outline-text">{props.dog_or_human}</span> </span>)
  let breed_span = props.dog_or_human === "neither" 
                                       ? (<span className="custom-font-xxlarge"> Please, try again with another image. </span>) 
                                       : (<span>Your breed is <span className="outline-text">{props.breed}</span></span>)



if( isMobileDevice ){
  mainContentLayoutClasses = 'text-center bg-color-white  gx-0 ' + phoneUIClasses
  leftSideLayoutClasses=" d-flex justify-content-between  custom-font-xxxlarge  custom-font-bold col-4 gx-4 custom-margin-left square-wrapper "

  wikiText = ""  
  
  leftSideHtml = (     
    <div id="left-side-html" className="text-black  custom-font-bold custom-font-family capitalize">
     <div>{human_or_dog_span}</div>
        <div>{breed_span}</div>
      </div>
  
      );

}

if( isBigDevice ){
  mainContentLayoutClasses = 'text-center bg-color-white  gx-0 ' + laptopClasses
  leftSideLayoutClasses=" justify-content-start custom-font-xxxlarge  custom-font-bold col-4 gx-4 custom-margin-left square-wrapper "

  wikiText = "Want to learn more? Check the wikipedia page below"

  leftSideHtml = (     
    <div id="left-side-html" className="custom-margin-top-7 text-black  custom-font-bold custom-font-family capitalize">
          
        <div>{human_or_dog_span}</div>
        <div>{breed_span}</div>
      </div>
  
      );

}
 function resizeHandler(){
  
    if($(window).width() <= minWidthBigDevice){
      
     $('#main-content').removeClass(laptopClasses).addClass(phoneUIClasses)
     $('#leftHalf').addClass('d-flex justify-content-between') 
     $("#wiki-text").text(mobileWikiText)
     $("#left-side-html").removeClass("custom-margin-top-7")
                      
    }
   console.log(window.innerWidth)
    if($(window).width() > minWidthBigDevice){
      
      $('#main-content').addClass(laptopClasses).removeClass(phoneUIClasses)
      $('#leftHalf').removeClass('d-flex justify-content-start')           
      $("#wiki-text").text(laptopWikiText)
      $("#left-side-html").addClass("custom-margin-top-7")
     }
 }


  $(window).resize(resizeHandler);



  switch(props.dog_or_human){
    case "dog":
      toast.success(`Dog Detected !`, {theme: "colored",})
      break

    case "human": 
      toast.success(`Person Detected !`, {theme: "dark",})
      break

    case "neither":
      toast.warning(`Image uploaded but no dog or human detected`, {theme: "dark",})
      break

    default:
      break

  }
 


  let wikiLink =
    props.href === "none" 
                ? null 
                : (
                <div>
                  <div id="wiki-text"className=" custom-font-xxlarge text-black custom-font-bold custom-font-family ">
                    <span>{wikiText}</span>
                  </div>
                  
                  <Button
                    href={wikipediaLink+props.href}
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
    <div id="main-content" className={mainContentLayoutClasses}>
       
      <Col id="leftHalf"  className={leftSideLayoutClasses}>
      {leftSideHtml}
      
        {wikiLink}
      </Col>
  

       <Col  id="paragraphs-div">
              <TutorialCard
                image={props.image}
                dog_or_human={props.dog_or_human}
              ></TutorialCard>
            </Col>
    </div>
  );
}

export default HomeScreen;