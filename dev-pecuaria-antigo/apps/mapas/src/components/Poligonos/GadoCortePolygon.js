import React from "react";
import { Polygon, Popup } from "react-leaflet";
import { GadoCorteInfo } from "../../Informations/GadoCorteInfo";

const greenOptions = { color: "orange" };

const GadoCortePolygon = () => {
  return (
    <>
       { GadoCorteInfo.map((gadoCorte) => {
        return (
          <Polygon pathOptions={greenOptions}  positions={gadoCorte.coord}>
            <Popup>{gadoCorte.name} </Popup>
          </Polygon>
        )
      }) }
      
      
    </>
  );
};

export default GadoCortePolygon;
