import React from "react";
import { Polygon } from "react-leaflet";
import { CampusInfo } from "../../Informations/CampusInfo";


const greenOptions = { color: "blue" };

const CampusPolygon = () => {
  return (
    <>
      { CampusInfo.map((campus) => {
        return (
          <Polygon pathOptions={greenOptions}  positions={campus.coord}>
          </Polygon>
        )
      }) }
      
      
    </>
  );
};

export default CampusPolygon;
