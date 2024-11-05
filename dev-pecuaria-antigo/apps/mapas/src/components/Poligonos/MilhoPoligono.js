import React from "react";
import { Polygon, Popup } from "react-leaflet";
import { MilhoInfo } from "../../Informations/MilhoInfo";


const purpleOptions = { color: "purple" };

const MilhoPolygons = () => {
  return (
    <>
      { MilhoInfo.map((milho) => {
        return (
          <Polygon pathOptions={purpleOptions}  positions={milho.coord}>
            <Popup>{milho.name} </Popup>
          </Polygon>
        )
      }) }
    </>
  );
};

export default MilhoPolygons;
