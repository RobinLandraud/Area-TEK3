import React, { useEffect, useState } from "react";
import Navbar from "components/Navbar";
import { useSelector } from "react-redux";
import api from "services/api";
import Service from "components/Service";
import 'styles/MyPanel.css'
import { useNotification } from "components/NotificationPopUp";

const MyPanel = () => {
  const user = useSelector((state) => state.auth.user);
  const [serviceList, setServiceList] = useState([])
  const [actionList, setActionList] = useState([/*{ "name": "Première action", "enum": "FIRST" }, { "name": "Deuxième action", "enum": "SECOND" }*/])
  const [reactionList, setReactionList] = useState([/*{ "name": "Première réaction", "enum": "FIRST" }, { "name": "Deuxième réaction", "enum": "SECOND" }*/])
  const [currentDelete, setCurrentDelete] = useState(-1)
  const [refreshNeeded, setRefreshNeeded] = useState(false)
  const csrfToken = useSelector((state) => state.auth.csrfToken);
  const addNotification = useNotification();


  const parseAbout = async () => {
    const response = await api.get("about.json", {}, null)
    const serviceAvailable = response.data.server.services
    if (serviceAvailable === undefined)
      return
    serviceAvailable.forEach((service, index) => {
      const transformedActions = service.actions.map(action => {
        if (action.action_data === undefined)
          return action
        const transformedData = action.action_data.reduce((acc, cur) => {
          return { ...acc, [cur.name]: '' };
        }, {});
        return { ...action, action_data: transformedData };
      });
      //acc for accumulator and cur for current
      const transformedReactions = service.reactions.map(reaction => {
        if (reaction.reaction_data === undefined)
          return reaction
        const transformedData = reaction.reaction_data.reduce((acc, cur) => {
          return { ...acc, [cur.name]: '' };
        }, {});
        return { ...reaction, reaction_data: transformedData };
      });
      setActionList(prevActionList => [...prevActionList, ...transformedActions])
      setReactionList(prevReactionList => [...prevReactionList, ...transformedReactions])
    })
  }

  const getService = async () => {
    const servicesResponse = await api.get("services/get/", {}, csrfToken, csrfToken)
    const newServiceList = servicesResponse.data.services.map((service, index) => {
      const action = { name: service.name_action, nickname: service.action, action_data: service.action_data }
      const reaction = { name: service.name_reaction, nickname: service.reaction, reaction_data: service.reaction_data }
      const newService = { ...service, action: action, reaction: reaction }
      return newService
    })
    setServiceList(newServiceList)
  }

  useEffect(() => {
    if ((!user || !user.log))
      return
    const fetchData = async () => {
      try {
        await parseAbout();
        await getService();
      } catch (error) {
        addNotification('Une erreur s\'est produite lors de la récupération de vos donnés', 'error');
      }
    }
    fetchData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [csrfToken, user])

  useEffect(() => {
    if ((!user || !user.log))
      return
    const fetchData = async () => {
      try {
        await getService()
      } catch (error) {
        addNotification('Une erreur s\'est produite lors de la récupération de vos donnés', 'error');
      }
      setRefreshNeeded(false)
    }
    if (refreshNeeded) {
      fetchData()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshNeeded, user, csrfToken])

  useEffect(() => {
    const sendDelete = async () => {
      const serviceToDelete = serviceList.find(item => item.id === currentDelete);
      if (serviceToDelete.new) {
        const newList = serviceList.filter(item => item.id !== currentDelete);
        setServiceList(newList)
        setCurrentDelete(-1)
        setRefreshNeeded(true)
        return
      }
      await api.delete("services/delete/", {}, { id: currentDelete }, csrfToken, csrfToken).then(res => {
        const newList = serviceList.filter(item => item.id !== currentDelete);
        setServiceList(newList)
        setCurrentDelete(-1)
        setRefreshNeeded(true)
      }).catch(err => {
        addNotification('Une erreur s\'est produite lors de l\'envoie de vos donnés', 'error');
      })
    }
    if (currentDelete !== -1) {
      sendDelete()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentDelete, serviceList, csrfToken])

  const addService = () => {
    const newID = serviceList.length > 0 ? serviceList[serviceList.length - 1].id + 1 : 0;
    let newService = { name: "New", action: undefined, reaction: undefined, id: newID, new: true }
    let newServiceList = [...serviceList, newService]
    setServiceList(newServiceList)
  }

  return (

    <div>
      <Navbar />
      {user && user.log &&

        <div className="services-container">
          {serviceList.map((service, index) => {
            if (service === undefined)
              return (<></>);
            return (
              <Service key={index} refresh={setRefreshNeeded} callDelete={setCurrentDelete} service={service} actionList={actionList} reactionList={reactionList}></Service>
            )
          })}
          <div className="add-service" onClick={addService}>
            Ajouter un service
          </div>
        </div>}
      {(!user || !user.log) &&
        <p>Vous devez être connecter pour avoir accès à votre espace</p>
      }
    </div>
  );
}

export default MyPanel;