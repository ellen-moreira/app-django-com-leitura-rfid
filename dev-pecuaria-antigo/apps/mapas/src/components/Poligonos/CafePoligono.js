import React from "react";
import { Polygon, Popup } from "react-leaflet";

import { coffePolygon } from "../../Informations/coffePolygon";

const greenOptions = { color: "green" };

const CafePolygons = () => {
  return (
    <>
      { coffePolygon.map((coffee) => {
        return (
          <Polygon pathOptions={greenOptions}  positions={coffee.coord}>
            <Popup>{coffee.name} </Popup>
          </Polygon>
        )
      }) }

 
     
    
      
    </>
  );
};

export default CafePolygons;
