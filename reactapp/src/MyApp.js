import React from "react";
import MainContent from "./components/CropPage/MainContent";
import { Switch, Route } from "react-router-dom";
import Wiki from "./components/wikipage/Wiki";
import { createCanvas } from "canvas";
import { Slide, Zoom, Flip, Bounce } from 'react-toastify';
import { ToastContainer, toast } from 'react-toastify';
//import {Button, Alert,Breadcrumb,Card,Container,Row,Col,Nav,Navbar,NavDropdown} from 'react-bootstrap'
class MyApp extends React.Component {
  render(props) {
    return (
      <div>
         <ToastContainer
      position="top-right"
      autoClose={5000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="dark"
      transition={Flip}
      />
        <Switch>
       
          <Route exact path={["/home", "/"]}>
              <MainContent />
          </Route>

          <Route exact path="/wiki" component={Wiki}></Route>
        </Switch>
      </div>
    );
  }
}

export default MyApp;
