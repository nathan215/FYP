import { useEffect, useRef } from "react";
import "ol/ol.css";
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat } from "ol/proj";

interface Props {
  mapWidth: string;
  mapHeight: string;
  longitude: number;
  latitude: number;
  zooming: number;
}

const MapComponent = ({
  mapWidth,
  mapHeight,
  longitude,
  latitude,
  zooming,
}: Props) => {
  const mapRef = useRef<Map | null>(null);
  const targetRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (targetRef.current) {
      const map = new Map({
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
        ],
        view: new View({
          center: fromLonLat([longitude, latitude]),
          zoom: zooming,
        }),
      });

      map.setTarget(targetRef.current);
      mapRef.current = map;

      return () => {
        if (targetRef.current && mapRef.current) {
          mapRef.current.setTarget(null as any);
          mapRef.current = null;
        }
      };
    }
  }, [latitude, longitude, zooming]);

  return (
    <>
      <div
        ref={targetRef}
        className="map-container"
        style={{
          width: mapWidth,
          height: mapHeight,
        }}
      ></div>
    </>
  );
};

export default MapComponent;
