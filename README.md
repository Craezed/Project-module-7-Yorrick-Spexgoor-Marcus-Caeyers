# Project-module-7-Yorrick-Spexgoor-Marcus-Caeyers

Sign Interpration

This project exists of an AI that interprets signs, and links them to letters. It does this using a CNN framework. It features a game which uses the AI to predict the sign made and uses it to spell out words.

Canny test.py: This is a version of the code implemented with the canny edge detection, this was mainly used for testing

Collect_data: This script is used for collecting data, when ran it will display the used camera and when the letter is pressed the image taken will be saved under a folder of that letter.

DataAugment: This script will augment the data with the values shown in Datagen on line 9. It makes 5 augmented versions of every image file you put in the datafolder

Game.py: This is the game that uses the AI prediction as a feature

Train_ai.py: This will train the AI either through a gridsearch or with using the given hyperparameters.
