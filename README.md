🎮 Gesture-Controlled Platformer Game
A Python + Pygame + MediaPipe Project Powered by Hand Tracking AI

This project is a 2D platformer game where the player is controlled entirely through hand gestures captured from a webcam.
Move left, move right, and jump — all without touching the keyboard!

Built using:
✔ Pygame for game engine
✔ MediaPipe Hands for gesture recognition
✔ OpenCV for webcam input
✔ Tkinter for Game Over / Win screens

🚀 Features
🎮 Core Gameplay

Player animation frames for smooth movement
Physics system: gravity, jumping, falling
Moving enemies with patrol AI
Level generated from a 2D grid map
Collision with tiles, platforms, and enemies


🏁 Win/Lose States

Game Over screen using Tkinter
You Win screen when reaching the exit
Automatic restart support

🛠️ Tech Stack
Component      	                                  Technology
Game Engine	                                      Pygame
Gesture Detection	                                MediaPipe Hands
Webcam Input	                                    OpenCV
UI Popups	                                        Tkinter
Language	                                        Python

🕹 Controls (Gesture Based)
Gesture	                                          Action
Hand moves Left	                                  Player moves left
Hand moves Right	                                Player moves right
Index finger up	                                  Jump

These gestures are detected using MediaPipe’s hand landmark positions.

🎯 Future Improvements

Add keyboard fallback controls
Add coins + scoring system
Create more levels
Add background music + sound effects
Add main menu + pause menu
Add player health and multiple lives
Export to Windows .exe format


Thank you for reading 🦾


