import { React, useEffect } from "react";
import { Row, Col, Card, Button, Form } from "react-bootstrap";
import { Link } from "react-router-dom";
import useWindowDimensions from "../CustomHooks/windowDimensions";
 
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
//Photo by Andrej Lišakov on Unsplash

//Photo by Adrienn87 form PxHere
function ConactUsPage() {
 
  const { height, width } = useWindowDimensions();
  return (
      <div id="main-content" className="bg-color-black ">
        <div className="square-wrapper2">
          <img src="globe5.jpg" height={height}  id="third-page-background"></img>
        </div>
        <div className=" custom-flex-center">
          <Row className="square-wrapper3  " style={{ width: "100%", height: "100%" }}>
            <div className="col-7 text-white"> ITS ME</div>
            <div style={{ width: "27rem", height: "30rem" }} className="card-glassy text-white col-4">
              <Card.Body>
                <Form>
                  <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="name@example.com" />
                  </Form.Group>
                  <Form.Group className="mb-3"
                    controlId="exampleForm.ControlTextarea1">
                    <Form.Label>Example textarea</Form.Label>
                    <Form.Control as="textarea" rows={3} />
                  </Form.Group>
                </Form>
                <Card.Title>Upload and Crop</Card.Title>
                <Card.Text>
                  upload an image. Resize it, move it to position and Crop! We
                  will give you as much product information as we can
                </Card.Text>
                <Button variant="outline-info" href="crop" className=" custom-font-size-2 custom-font-bold custom-font-family">
                  LETS GO!
                </Button>
              </Card.Body>
            </div>
          </Row>
        </div>
      </div>
  );
}

export default ConactUsPage;
