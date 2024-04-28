import type { MetaFunction } from "@remix-run/node";
import { YMaps, Map, Clusterer, Circle } from '@pbe/react-yandex-maps';
import { axios } from '../middleware';
import { useEffect, useState } from 'react';
import { Modal } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";


export const meta: MetaFunction = () => {
  return [
    { title: "PureWater - следите за качеством воды по всему миру" },
    { name: "description", content: "Контролируйте уровень загрязнения воды" },
  ];
};


function getGraphPoints(device_id) {
  axios.get('/graph_data?device_id=1&type=0&interval=5%20minutes', {
    params: {
      device_id: 1,
      type: 0,
      interval: '5 minutes'
    }
  })
  .then((res) => {
    return res.data
  })
}


function Index() {
  const [devicesData, setDevicesData] = useState([])
  const [opened, { open, close }] = useDisclosure(false);
  const [currentDevice, setCurrentDevice] = useState(null)
  const [graphPoint, setGraphPoint] = useState([])

  useEffect(() => {
    axios.get('/all').then((resp) => {
      setDevicesData(resp.data)
      setCurrentDevice(resp.data[0])
      open()
    })
  }, [])

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        title="Информация по датчику"
        centered
      >
        {currentDevice &&
          <div>
            <div>Датчик {currentDevice.name}</div>
            <div>Текущий показатель: {Math.round(currentDevice.last_value * 100) / 100} PH</div>
            <div>
              
            </div>
          </div>
        }
      </Modal>
      <YMaps>
        <Map
          width="100vw"
          height="100vh"
          state={{
            center: [54.74306, 55.96779],
            zoom: 9,
            controls: ["zoomControl"]
          }}
          modules={["control.ZoomControl"]}
        >
          <Clusterer
            options={{
              preset: "islands#invertedVioletClusterIcons",
              groupByCoordinates: false,
            }}
          >
            {devicesData.map((deviceData, index) => (
              <Circle
                key={index}
                geometry={[[deviceData.latitude, deviceData.longitude], 500]}
                options={{
                  fillColor: deviceData.danger_type == null ? "0000FF" : deviceData.danger_type == 0 ? "00FF00" : deviceData.danger_type == 1 ? "FFFF00" : "FF0000",
                  fillOpacity: 0.5
                }}
              />
            ))}
          </Clusterer>
        </Map>
      </YMaps>
    </>
  )
}

export default Index