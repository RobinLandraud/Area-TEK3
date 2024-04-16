# Area : DEV - Application Development

## **Main goal**

The goal of this project is to create a web and mobile application that implements shortcuts to other services.<br />
The user will be able to create link his accounts with the services we have implemented and create shortcuts to use them.<br />
He would be able to catch the fact that he received an email and add a reaction for this event.<br />
For example, the user will be able to save the attached files of an email in his Tumblr account each time he receive one.<br />

## **How to compile ?**

Run this command on your terminal:
```
docker-compose build
```

## **How to launch ?**

Run this command on your terminal:
```
docker-compose up
```
(This command will automatically launch the server and the client web application)<br />

## **Services and Actions/Reactions implemented**

### **Tumblr**

**Action**: 

**Reaction**: 

### **Gmail**

**Action**: Detect when an email has been received

**Reaction**: Send an email

### **Github**

**Action**: 

**Reaction**: Create an issue

**Reaction**: Create a pull request


### **Reddit**

**Action**: Detect subreddit modification

**Action**: Detect when a certain subreddit followed got a new subscriber

**Reaction**: Compose and send an private message to someone

**Reaction**: Créer un post dans un subreddit

### **Spotify**

**Action**: Detect when a user playlist is updated

**Action**: Detect when a user create a new playlist

**Reaction**: Create a new playlist and add selected song to it

**Reaction**: Create a new playlist and add song of the day to it

**Reaction**: Follow the given artist/user

**Reaction**: Save album from an artist or user

**Reaction**: Add a music to the player track queue

**Reaction**: Subscribe to a podcast(show)


### **Weather**

**Action**: Detect when the weather is going to be rainy

**Action**: Detect when a certain temperature has been reached

## **Technologies used**

**Backend**

Framework: Django<br />
Language: Python

**Frontend**

Framework: React<br />
Language: Javascript

**Database**

mysql

**Mobile**

Framework: React Native<br />
Language: Javascript

**APIs**

- Tumblr API<br />
- Gmail API<br />
- Github API<br />
- Reddit API<br />
- Spotify API<br />
- Weather API<br />

## PDF of the subject

[Subject - Area](https://intra.epitech.eu/module/2022/B-DEV-500/BDX-5-2/acti-554251/project/file/B-DEV-500_AREA.pdf)


## Authors

- Valentin Eyraud
- Louis Leblond
- Nicolas Lavigne
- Rémi Huguet
- Robin Landraud
