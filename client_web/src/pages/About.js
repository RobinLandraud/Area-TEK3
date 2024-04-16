import React, { useEffect, useState } from "react";
import Navbar from "components/Navbar";
import api from "services/api";
import 'styles/About.css'

const InfoBlock = (props) => {
  const [color, setColor] = useState(getRandomColor());

  function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
  }

  const handleClick = () => {
    setColor(getRandomColor());
  }

  const divStyle = {
    border: `4px solid ${color}`,
    padding: '20px' // Optional styling
  };

  return (
    <div style={divStyle} className="info-container" onClick={handleClick}>
      {props.name !== undefined && <h3>{props.name}</h3>}
      {typeof props.value === 'object' && props.value !== null && !Array.isArray(props.value) && Object.entries(props.value).map(([key, value]) => (
        <InfoBlock name={key} value={value}/>
      ))}
      {typeof props.value === 'object' && Array.isArray(props.value) &&
        props.value.map((item) => {
          return (
            <>
              <InfoBlock value={item}/>
            </>
          )
        })
      }
      {typeof props.value === 'string' && <p>{props.value}</p>}
      {typeof props.value === 'number' && <p>{props.value}</p>}
      {typeof props.value === 'boolean' && <p>{props.value ? "True": "False"}</p>}
      {typeof props.value === 'undefined' && <p>Type de valeur inconnue</p>}
    </div>
  )
}

const About = () => {
  const [about, setAbout] = useState({})

  useEffect(() => {
    const fetchData = async () => {
      const response = await api.get("about.json", {}, null)
      setAbout(response.data)
    }
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
  <div>
    <Navbar />
    <div className="about-container">
      <InfoBlock name="About" value={about}/>
    </div>
  </div>
  );
}

export default About;