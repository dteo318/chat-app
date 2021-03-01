# Real-time Chat App

## Description
A real-time chat messaging app built with Django as the backend and real-time functionality implemented using the Channels Django library.

## Features

### Checking who's in the current room

To check who is in the current room, click the "Users" dropdown in the top right corner of the screen. The user's name will be bolded while other members will not. If users leave the room, there will be a message by "ADMIN" in the chat indicating who has left.

### Added a room key

A simple password or room key can be added by clicking the "Users" dropdown in the top right corner of the screen, entering the room key into the input box and clicking set. From then on, when users want to join the room, they will need to enter the room key into the password field. 

The room key can be set by anyone in the room and everyone is able to view the current room key by clicking the "Users" dropdown. When a room member changes the room key, it will be reflected on all room members' room key input field.

### Saving messages

Messages are typically not saved and users who join the room after messages have been sent will not see the previously sent messages. 

However, clicking on messages will put a grey highlight over the message and save it. This means that new users will see these saved messages in their chat box upon joining the room, and even after all members have left the chat room, these messages will remain and be shown upon rejoining the chat.

Messages can be unsaved by clicking on them again. The grey highlight will be removed and the message will disappear once the user leaves the chat room.

### Is typing...

At the bottom of the chat box, a grey "is typing..." indicator will appear when other room users are typing. 

## Usage

### Opening the chat room app

1. Install Docker from https://www.docker.com/get-docker
2. Create a virtual environment on your system
3. Install dependencies by running `pip install -r requirements.txt` in your shell
4. Run `docker run -p 6379:6379 -d redis:5` in your shell
5. `cd chat-project` to enter the folder with the manage.py
6. Run `python manage.py runserver` and go to http://127.0.0.1:8000/ in your web browser

### Entering a chat room

1. Enter a username and room
2. If the room has a password, enter a password
3. Press `enter` and you will be redirected to a chat room
4. You can simulate additional users by opening a new tab, going to http://127.0.0.1:8000/ and entering the same room but with a different username
