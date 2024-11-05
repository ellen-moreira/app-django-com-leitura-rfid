import React from "react";
import { Marker, Popup, Polygon } from "react-leaflet";
import L from "leaflet";
import markercafe from "../../icones.png/coffee_beam_20595.png";
import { talhao1 } from "../../coordenadas/CoordCafe";

const myIcon = new L.Icon({
  iconUrl: markercafe,
  iconRetinaUrl: markercafe,
  popupAnchor: [-0, -0],
  iconSize: [32, 32],
});
const purpleOptions = { color: "purple" };
const CafeMarkers = () => {
  return (
    <>
      <Marker icon={myIcon} position={[-21.3519095, -46.5211916]}>
        <Popup>
          <a>TALHÃO</a>
          <p>T-3</p>
        </Popup>
      </Marker>

      <Marker icon={myIcon} position={[-21.3521843, -46.521033]}>
        <Popup>
          <a>TALHÃO</a>
          <p>T-4</p>
        </Popup>
      </Marker>
      <Polygon pathOptions={purpleOptions} positions={talhao1}>
                  <Popup>talhao1</Popup>
                </Polygon>
                <Marker icon={myIcon} position={[-21.3519095, -46.5211916]}>
                <Popup>
                  <a>TALHÃO</a>
                  <p>T-3</p>
                </Popup>
              </Marker>

              <Marker icon={myIcon} position={[-21.3521843, -46.521033]}>
                <Popup>
                  <a>TALHÃO</a>
                  <p>T-4</p>
                </Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.35171, -46.520575]}>
                <Popup>
                  <a>TALHÃO</a>
                  <p>T-5</p>
                </Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3520494, -46.5207648]}>
                <Popup>
                  <a>TALHÃO</a>
                  <p>T-5</p>
                </Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3511486, -46.5209594]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.351593, -46.520888]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350932, -46.52052]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350741, -46.521142]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350335, -46.520706]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350056, -46.520971]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350169, -46.521722]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350413, -46.521957]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.35043, -46.521229]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350776, -46.521923]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.349787, -46.521373]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350635, -46.522985]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.348565, -46.520455]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.348399, -46.519947]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350249, -46.522561]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.349871, -46.524036]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350451, -46.524123]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.349059, -46.52509]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.350032, -46.525617]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.34611111, -46.52861111]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3433254, -46.5258536]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.34361111, -46.52638889]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3431076, -46.5276705]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3426699, -46.5283333]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3427298, -46.5296054]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3427798, -46.5309084]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3428598, -46.5320839]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3423821, -46.5325644]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.34277778, -46.53305556]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3426799, -46.5340272]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3422222, -46.5341238]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.342492, -46.5307272]}>
                <Popup>Prédio H</Popup>
              </Marker>
              <Marker icon={myIcon} position={[-21.3427798, -46.5355019]}>
                <Popup>Prédio H</Popup>
              </Marker>
      
      {/* Adicione mais marcadores aqui conforme necessário */}
    </>
  );
};

export default CafeMarkers;
