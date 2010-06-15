#! /bin/bash

sentence="take the blue cube."

#sentence="Could you take the blue cube?"
#sentence="Can you take my cube?"
#sentence="I want you to show me the black tape."
#sentence="Please take the blue cube."
#sentence="Please take the blue cube."
#sentence="put the grey tape next to the blue cube."
#sentence="put the tape on the table, next to the blue cube."
#sentence="put my tape in the trashbin."
#sentence="Where is the blue cube?"
#sentence="Where are the cubes?"
#sentence="What do you see?"
#sentence="Jido, I need the grey tape!"

echo $sentence | src/dialog/dialog.py -d
