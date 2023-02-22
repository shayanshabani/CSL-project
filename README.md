# CSL-project

# Face-Recognition-Door-phone

A project on Raspberry Pi that uses OpenCV and face recognition to create a smart door phone system. This system consists of two LEDs, one buzzer, a keypad, and a push button. 

## Features
- Three different modes of operation
- Ability to recognize known faces using OpenCV
- Integration with email to notify when an unknown person is at the door
- Client app for viewing the camera feed and adding known faces

## Modes of Operation
1. Mode 0:
   - If the person in front of the camera is known, the first (green) LED will light up.
   - If the person is unknown, the second (red) LED will light up.
2. Mode 1:
   - The second (red) LED will light up and an email with the picture of the person in front of the camera will be sent to your email.
3. Mode 2:
   - If the person is known, the first (green) LED will light up. 
   - If the person is unknown, the second (red) LED will light up. 
   - An email containing the picture of the person in front of the door will be sent to your Gmail address.

## Components
- Raspberry Pi
- Two LEDs (red and green)
- Buzzer
- Keypad
- Push button
- OpenCV

## Client App
The client app allows you to view the video feed from the camera and add known faces. This allows you to remotely manage the faces that the door phone system can recognize.

## Getting Started
To use this project, you will need to have a Raspberry Pi set up with OpenCV and the necessary components. Once you have everything set up, follow these steps to get started:
1. Clone the repository to your Raspberry Pi
2. Change the ip of the ipwebcam and your Raspberry Pi
3. Run the code
4. Use the client app to manage known faces and view the camera feed

## report of the project in only read mode:
https://latex.sharif.edu/read/rtmfnjhkrxwg
