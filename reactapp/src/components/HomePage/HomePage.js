import { React, useEffect } from "react";
//import useWindowDimensions from "../CustomHooks/windowDimensions";
import HomeScreen from "./HomeScreen"
import TutorialScreen from "./TutorialScreen";
import ContactUsPage from "./ContactUsPage"



//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//Photo by Andrej Lišakov on Unsplash

//Photo by Adrienn87 form PxHere
function HomePage() {
  useEffect(() => {

    const secondPageBackGroundObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const image = entry.target.querySelectorAll("img");
        if (entry.isIntersecting) {
          image.forEach((s) => s.classList.add("custom-fade-in", "slide-down"));
          return; // if we added the class, exit the function
        }
        // We're not intersecting, so remove the class!
        image.forEach((s) =>
          s.classList.remove("custom-fade-in", "slide-down")
        );
      });
    });
    secondPageBackGroundObserver.observe(
      document.querySelector(".square-wrapper2")
    );

    const secondPageCardObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const text = entry.target.querySelectorAll("div");
        if (entry.isIntersecting) {
          text.forEach((s) => s.classList.add("custom-fade-in"));
          return; // if we added the class, exit the function
        }
        // We're not intersecting, so remove the class!
        text.forEach((s) => s.classList.remove("custom-fade-in"));
      });
    });
    secondPageCardObserver.observe(document.querySelector(".square-wrapper3"));
  }, []);
  // const { height, width } = useWindowDimensions();
  return (
    <div id="whole-page-home">
      <HomeScreen />

      <TutorialScreen />
      <ContactUsPage />

    </div>
  );
}

export default HomePage;
