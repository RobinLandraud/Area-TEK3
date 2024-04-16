import React, { useEffect, useState } from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import { Button } from 'react-bootstrap';
import { FaTimes } from 'react-icons/fa';
import { useSelector } from "react-redux";
import api from "services/api";
import 'styles/Service.css'
import { useNotification } from "./NotificationPopUp";

const ServiceDropDown = (props) => {
    return (
        <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                {props.title}
            </Dropdown.Toggle>
            <Dropdown.Menu>
                {props.list.map((item, index) => {
                    return (
                        <Dropdown.Item id={index} key={index} eventKey={index} onClick={props.onItemClick}>{item.name}</Dropdown.Item>
                    )
                })}
            </Dropdown.Menu>
        </Dropdown>

    )
}

const Service = (props) => {
    const [selectedAction, setselectedAction] = useState(props.service.action)
    const [selectedReaction, setselectedReaction] = useState(props.service.reaction)
    const [previusAction, setPreviusAction] = useState(props.service.action)
    const [previusReaction, setPreviusReaction] = useState(props.service.reaction)
    const [previusName, setPreviusName] = useState(props.service.name)
    const [name, setName] = useState(props.service.name || '')
    const [isNew, setIsNew] = useState(props.service.new)
    const [isUpdate, setIsUpdate] = useState(false)
    const csrfToken = useSelector((state) => state.auth.csrfToken);
    const [actionData, setActionData] = useState(props.service.action && props.service.action.action_data !== undefined ? props.service.action.action_data : {})
    const [reactionData, setReactionData] = useState(props.service.reaction && props.service.reaction.reaction_data !== undefined ? props.service.reaction.reaction_data : {})
    const addNotification = useNotification();

    useEffect(() => {
        if (selectedAction !== previusAction || selectedReaction !== previusReaction || name !== previusName)
            setIsUpdate(true)
        else
            setIsUpdate(false)
    }, [selectedAction, selectedReaction, previusAction, previusReaction, name, previusName])

    const handleActionClick = (event) => {
        let newSelectedAction = props.actionList[event.target.id]
        setselectedAction(newSelectedAction)
        setActionData(newSelectedAction.action_data !== undefined ? newSelectedAction.action_data : {})
    }

    const handleReactionClick = (event) => {
        let newSelectedReaction = props.reactionList[event.target.id]
        setselectedReaction(newSelectedReaction)
        setReactionData(newSelectedReaction.reaction_data !== undefined ? newSelectedReaction.reaction_data : {})
    }

    const createService = () => {
        const actionNickName = selectedAction !== undefined ? selectedAction.nickname : "AOTH";
        const reactionNickName = selectedReaction !== undefined ? selectedReaction.nickname : "ROTH";
        api.post("services/add/", {}, { action: actionNickName, reaction: reactionNickName, name: name, reaction_data: reactionData, action_data: actionData }, csrfToken, csrfToken).then(res => {
            setIsNew(false)
            props.refresh(true)
            setPreviusAction(selectedAction)
            setPreviusReaction(selectedReaction)
            setPreviusName(name)
            setIsUpdate(false)
            addNotification('Service crée avec succès');
            return true
        }).catch(error => {
            setIsNew(true)
            addNotification('Une erreur s\'est produite lors de l\'enregistrement de vos données', 'error');
            return false
        })
        //send create request to back

    }

    const updateService = () => {
        //send update request to back
        const actionNickName = selectedAction !== undefined ? selectedAction.nickname : "AOTH";
        const reactionNickName = selectedReaction !== undefined ? selectedReaction.nickname : "ROTH";
        api.put("services/update/", {}, { id: props.service.id, action: actionNickName, reaction: reactionNickName, name: name, reaction_data: reactionData, action_data: actionData }, csrfToken, csrfToken).then(res => {
            props.refresh(true)
            setPreviusAction(selectedAction)
            setPreviusReaction(selectedReaction)
            setPreviusName(name)
            setIsUpdate(false)
            addNotification('Service modifié avec succès');
            return true
        }).catch(error => {
            addNotification('Une erreur s\'est produite lors de l\'enregistrement de vos données', 'error');
            console.log(error)
            return false
        })
    }

    const handleDelete = () => {
        props.callDelete(props.service.id)
    }

    const handleSave = () => {
        if (isNew)
            createService()
        else
            updateService()
    }

    const handleNameChange = (event) => {
        if (event.target.value.length <= 15 || event.target.value.length < name.length)
            setName(event.target.value)
    }

    const handleReactionChange = (key, value) => {
        setReactionData({ ...reactionData, [key]: value });
        setIsUpdate(true)
    }

    const handleActionChange = (key, value) => {
        setActionData({ ...actionData, [key]: value });
        setIsUpdate(true)
    }

    return (
        <div className="service-container">
            <h2>
                <input
                    className="input-name-field"
                    type="text"
                    value={name}
                    onChange={handleNameChange}
                />
            </h2>

            <div className="action-container">
                <ServiceDropDown title={selectedAction !== undefined ? selectedAction.name : "Choisir une action"} list={props.actionList} onItemClick={handleActionClick} />
                {Object.entries(actionData).map(([key, value]) => (
                    <div key={key}>
                        <label>
                            {key}:
                            <input
                                type="text"
                                value={value}
                                onChange={(e) => handleActionChange(key, e.target.value)}
                            />
                        </label>
                    </div>
                ))}
            </div>
            <div className="reaction-conatiner">
                <ServiceDropDown title={selectedReaction !== undefined ? selectedReaction.name : "Choisir une réaction"} list={props.reactionList} onItemClick={handleReactionClick} />
                {Object.entries(reactionData).map(([key, value]) => (
                    <div key={key}>
                        <label>
                            {key}:
                            <input
                                type="text"
                                value={value}
                                onChange={(e) => handleReactionChange(key, e.target.value)}
                            />
                        </label>
                    </div>
                ))}
            </div>
            {isUpdate && <Button variant="success" onClick={handleSave}>Save</Button>}
            <Button variant="danger" onClick={handleDelete}>
                <FaTimes />
            </Button>
        </div>
    )
}

export default Service