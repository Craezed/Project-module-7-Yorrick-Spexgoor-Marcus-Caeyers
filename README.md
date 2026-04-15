# Project-module-7-Yorrick-Spexgoor-Marcus-Caeyers

Sign Interpration

This project exists of an AI that interprets signs, and links them to letters. It does this using a CNN framework. It features a game which uses the AI to predict the sign made and uses it to spell out words.

Collect_data: This script is used for collecting data, when run it will display the used camera. When a letter from the available options is pressed, it saves a cropped 320 x 320 pixel image in the corresponding data folder

DataAugment: This script will augment the data with certain values. It makes 5 augmented versions of every image file you put in the datafolder, and put them in the same folder as the original image

Train_ai.py: This will train the AI either through a gridsearch or using certain hyperparameters, it uses the images in the data folder as training data.

Canny test.py: This is a version of the code implemented with the canny edge detection, this was mainly used for testing

Game.py: This is a game that uses the AI prediction as a feature. It prompts the user to spell a word using the gestures, where the AI will recognise these gestures and tell the user which letter it represents
