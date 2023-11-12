import React from "react";
import {Card} from "react-bootstrap";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON,Tooltip } from "react-leaflet";
//import {Button, Alert,Breadcrumb,Card,Container,Row,Col,Nav,Navbar,NavDropdown} from 'react-bootstrap'
//<a href={wikiInfo.href}>{wikiInfo.breed}</a>
//<div id="paragraphs-div">
//{wikiInfo.paragraphs.map((paragraph) => <p class="para-styles">{paragraph}</p>)}
//</div>
//<h1 id ="main-title">{wikiInfo.breed}</h1>
function OSMap(props) {
  let locations = props.locations.map((position) => {
    console.log(position.hasOwnProperty("tags"))
    if (position.hasOwnProperty("tags")){
      
      
      return <Marker position={[position.lat, position.lon]}><Tooltip>{JSON.stringify(position.tags)}</Tooltip></Marker>
    }
    return <Marker position={[position.lat, position.lon]}><Popup>no tag</Popup></Marker>
  });
  
  return (
    <Card.Body>
  <div id="map" className="card-glassy text-white">
     
     <MapContainer
        center={[51.505, -0.09]}
        zoom={13}
        scrollWheelZoom={false}
        style={{ height: "100vh", width:"110vh"}}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[51.505, -0.09]}>
          
          <Tooltip><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/HTML5_logo_and_wordmark.svg/195px-HTML5_logo_and_wordmark.svg.png" alt="Girl in a jacket" width="20" height="20"></img></Tooltip>
          
       
        </Marker>
        {locations}
      </MapContainer>

     
    
    </div>
    </Card.Body>

    

  
  );
}

export default OSMap;
