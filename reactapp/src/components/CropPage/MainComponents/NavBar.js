import { React } from "react";
import { Nav, Navbar, Container, Button } from "react-bootstrap";
//Button, Alert,Breadcrumb,Card,,Row,Col,
function NavBar(props) {
  let loginButtons = [];
  loginButtons.push(
    <Nav.Link
      className={props.textColor + "    rounded hover-shadow ripple"}
      variant="secondary"
      href="home"
    >
      {" "}
      Predict
    </Nav.Link>
  );
  //add sticky for sticky
  return (
    <Navbar bg=" " expand="lg" className={props.backgroundColor+" custom-navbar"} >
      <Container >
        
          <div >
            <Navbar.Brand href="home">
              <img
                src="/doglogo.png"
                width="75%"
                height="75%"
                className="d-inline-block align-top  custom-navbar"
                alt="Logo"
              />
            </Navbar.Brand>
          </div>
        
      <Button
        variant="outline-warning"
        href="home"
        
        size="lg"
      >
        Home
      </Button>
      
      
      </Container>

    </Navbar>
  );
}

export default NavBar;
