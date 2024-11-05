import React from "react";
import { Polygon, Popup } from "react-leaflet";
import { GadoLeiteInfo } from "../../Informations/GadoLeiteInfo";


const greenOptions = { color: "black" };

const GadoLeitePolygons = () => {
  return (
    <>
     
     { GadoLeiteInfo.map((gadoLeite) => {
        return (
          <Polygon pathOptions={greenOptions}  positions={gadoLeite.coord}>
            <Popup>{gadoLeite.name} </Popup>
          </Polygon>
        )
      }) }

      
      
    </>
  );
};

export default GadoLeitePolygons;
