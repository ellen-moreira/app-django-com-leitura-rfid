import React from "react";
import { Polygon, Popup } from "react-leaflet";
import {CaprinoOvinoInfo} from "../../Informations/CaprinoOvinoInfo"

const greenOptions = { color: "green" };

const CaprinoOvinoPolygon = () => {
  return (
    <>
       { CaprinoOvinoInfo.map((caprinoOvino) => {
        return (
          <Polygon pathOptions={greenOptions}  positions={caprinoOvino.coord}>
            <Popup>{caprinoOvino.name} </Popup>
          </Polygon>
        )
      }) }

      
    </>
  );
};

export default CaprinoOvinoPolygon;
