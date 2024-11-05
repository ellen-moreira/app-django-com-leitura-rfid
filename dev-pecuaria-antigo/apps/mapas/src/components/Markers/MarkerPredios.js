import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";
import markeredificios from "../../icones.png/pino-de-localizacao.png";
import imgPredioH from "../../ImgLugares/PredioH.png";
import { buildingMarkers } from '../../Informations/markers'

const Iconlugar = new L.Icon({
  iconUrl: markeredificios,
  iconRetinaUrl: markeredificios,
  popupAnchor: [-0, -0],
  iconSize: [32, 32],
});


const LocalMarkers = () => {
  

  return (
    <>     
      { buildingMarkers.map((building) => {
        return (
          <Marker icon={Iconlugar} position={building.coord}>
            <Popup>{building.name} <div className="pop-up-container">
          <img src={imgPredioH} alt="Prédio H" />
        </div></Popup>
          </Marker>
        )
      }) }

      
    </>
  );
};

export default LocalMarkers;
