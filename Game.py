import random

import cv2
import pygame
import pygame.camera
import os
from keras.models import load_model
import numpy as np

size = (2560/4, 1440/4)
frame_size = (256, 256)
model = load_model("model.keras")
words = ["stern", "noses", "laces" ,"roast", "stall", "cents", "rolls", "tries", "clean", "lines", "trail"]
word = ""
font = None

def main():
    pygame.init()  # Initialize the pygame library
    pygame.camera.init()
    screen = pygame.display.set_mode(size)  # Initialize the camera screen
    clock = pygame.time.Clock()  # Initialize a pygame
    font = pygame.font.Font(None, 48)
    predicted_letter = ""

    # Set Camera
    camlist = pygame.camera.list_cameras()
    if not camlist:
        print("No camera found")
        pygame.quit()

    cam = pygame.camera.Camera(camlist[0], size)
    cam.start()

    img = pygame.Surface(size) # To store camera frames

    # Set word and place to put it
    word = pick_new_word()

    text_surface = font.render(word, True, 0)
    text_rect = text_surface.get_rect(center=(50, 50))

    # Create frame
    frame = pygame.Rect([0, 0], frame_size)
    frame.center = (size[0] // 2, size[1] // 2)

    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the screen is closed, quit the program
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                Key_Check(img, frame, event.key, predicted_letter)

        # Capture image from camera
        try:
            cam.get_image(img)
        except Exception as e:
            print(f"Error capturing image: {e}")
            break

        # Display Image
        img = pygame.transform.flip(img, True, False)

        screen.blit(img, (0, 0))

        pygame.draw.rect(screen, 0, frame, 10)

        pygame.draw.rect(screen, (255, 255, 255), text_rect)
        screen.blit(text_surface, text_rect)

        predicted_letter_text = font.render(predicted_letter, True, 0)
        predicted_letter_rect = text_surface.get_rect(center=(size[0] // 4, size[1] // 2))
        pygame.draw.rect(screen, (255, 255, 255), predicted_letter_rect)
        screen.blit(predicted_letter_text, predicted_letter_rect)
        print(predicted_letter)
        pygame.display.flip() # Update Screen

        clock.tick(60)  # Limits frame rate to 60 FPS

def Key_Check(img, frame, key, predicted_letter):
    label_key = ['a', 'c', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't']

    if key == pygame.K_SPACE:
        cropped_image = img.subsurface(frame)

        # Extract pixel data from pygame surface
        img_array = pygame.surfarray.pixels3d(cropped_image) # Array: (width, height, 3)
        img_array = np.transpose(img_array, (1, 0, 2)) # Match training data

        img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

        # Get predicted label
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_letter = label_key[predicted_index]

        for letter in word:
            if letter == predicted_letter:
                pass



def pick_new_word():
    word = random.choice(words)
    print(word)
    return word

# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()