import { Card, Button } from "react-bootstrap";
import { React, useEffect } from "react";
function TutorialCard(props) {
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

  let cardTitle =
    props.dog_or_human === "dog"
      ? `Cute as a Button!`
      : props.dog_or_human === "human"
        ? `Lookin' sharp!`
        : "Cool Image!";

  return (
    <div className="square-wrapper3">
      <div

        className="card-glassy text-white square-wrapper2"
        id="breed-glass-card"

      >
        <Card.Img variant="top" src={props.image} />
        <Card.Body>
          <Card.Title>{cardTitle}</Card.Title>
          <Card.Text>
            Want to check another image? Click on the button below
          </Card.Text>
          <Button
            variant="outline-info"
            href="home"
            className=" custom-font-size-2 custom-font-bold custom-font-family"
          >
            let's Go! →→
          </Button>
        </Card.Body>
      </div>
    </div>
  );
}

export default TutorialCard;
