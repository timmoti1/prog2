# SCRUMTODOL

The acronym stands for **super cool really useful mini TODO list.**

## Installation

Fist of all install flask if not already done. The server runs in debug mode so it can be started by typing ```python3 app.py``` in the console.
The app should now be running. there should be an address and port in the console, which upon opening displays the web app.

## Capabilities and Usage

The app is capable of saving tasks and working through them in a SCRUM style manner.
That being said there are four categories:

1. Backlog: Used as a "todo bucket". Everything that has to be done goes into there.
1. Active: Houses all todo items that you're currently working on.
1. Done: Houses all items you successfully completed.
1. Archive: When your done "bucket" gets quite full you can archive items.

Features:

- Add items
- Move items from one bucket to the next one
- Modify items
- Delete items
- Set due dates and get a reminder badge on the item if it is
  - overdue (red badge)
  - due tomorrow (yellow badge)
  - due today (yellow badge)

Limitations:

- There is no way to move items in a backwards fashion.

## Project Idea

