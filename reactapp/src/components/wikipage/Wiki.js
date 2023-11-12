import React from "react";
import NavBar from "../CropPage/MainComponents/NavBar";
import HomeScreen from "../HomePage/HomeScreen";
import { ToastContainer, toast } from 'react-toastify';
import { Slide, Zoom, Flip, Bounce } from 'react-toastify';
import OSMap from "../HomePage/OSMap";

//import {Button, Alert,Breadcrumb,Card,Container,Row,Col,Nav,Navbar,NavDropdown} from 'react-bootstrap'
//<a href={wikiInfo.href}>{wikiInfo.breed}</a>
//<div id="paragraphs-div">
//{wikiInfo.paragraphs.map((paragraph) => <p class="para-styles">{paragraph}</p>)}
//</div>
//<h1 id ="main-title">{wikiInfo.breed}</h1>

function Wiki(props) {
  const wikiInfo = props.location.state || {};
  
  return (
    <div>
      
      <NavBar backgroundColor="dark-purple" />
      <div id="text-body">
      <img
        src="glass1.jpg"
        className="custom-fade-in-2"
        id="home-page-background"
        alt="backGround"
      ></img>
        <div id="whole-page-home">
          <div>
            <HomeScreen
              breed={wikiInfo.breed}
              href={wikiInfo.href}
              dog_or_human={wikiInfo.dog_or_human}
              image={wikiInfo.image}
            />
          </div>
          {/*<OSMap locations={wikiInfo.locations} />  include future map here*/}
        </div>
      </div>
    </div>
  );
}

export default Wiki;
