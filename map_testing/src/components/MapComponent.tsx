import { useEffect, useRef } from "react";
import "ol/ol.css";
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat } from "ol/proj";

interface Props {
  longitude: number;
  latitude: number;
  zooming: number;
}

const MapComponent = ({ longitude, latitude, zooming }: Props) => {
  const mapRef = useRef<Map | null>(null);
  const targetRef = useRef<HTMLDivElement | null>(null);

  /*The first useEffect hook is used to initialize the map when the component mounts. 
  It checks if the targetRef has a current value (referring to the target DOM element). 
  If it exists, a new Map instance is created, with a single TileLayer using OpenStreetMap as the source. 
  The target element is set to the current value of targetRef. A View is also created, with the center and zoom level configured based on the props. 
  The view is set for the map instance, and the map reference is stored in mapRef. 
  Finally, a cleanup function is returned to reset the map target when the component unmounts. */

  useEffect(() => {
    if (targetRef.current) {
      const map = new Map({
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
        ],
        target: targetRef.current,
      });

      const view = new View({
        center: fromLonLat([longitude, latitude]),
        zoom: zooming,
      });

      map.setView(view);
      mapRef.current = map;

      return () => {
        if (mapRef.current && targetRef.current) {
          mapRef.current.setTarget(targetRef.current);
        }
      };
    }
  }, []);

  /*The second useEffect hook is used to update the map when the latitude, longitude, or zooming props change. 
  It checks if the map reference exists (mapRef.current) and at least one of the props has changed. 
  If so, the view is obtained from the map instance, and its center and zoom level are updated based on the props. 
  This ensures that the map view reflects the new coordinates and zoom level. */

  useEffect(() => {
    if (mapRef.current && (latitude || longitude || zooming)) {
      const view = mapRef.current.getView();
      view.setCenter(fromLonLat([longitude, latitude]));
      view.setZoom(zooming);
    }
  }, [latitude, longitude]);

  return (
    <>
      <h1>Resulting Map</h1>
      <div
        ref={targetRef}
        className="map-container"
        style={{
          width: "50%",
          height: "400px",
        }}
      ></div>
    </>
  );
};

export default MapComponent;
