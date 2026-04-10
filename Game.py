import random
import pygame
import pygame.camera
from keras.models import load_model
import numpy as np

pygame.init()  # Initialize the pygame library

size = (1600/2, 1200/2)
frame_size = (320, 320)
model = load_model("model.keras")
words = ["stern", "noses", "laces" ,"roast", "stall", "cents", "rolls", "tries", "clean", "lines", "trail"]
font = pygame.font.Font(None, int(size[1]/5))

# Create frame
focus_frame = pygame.Rect([0, 0], frame_size)
focus_frame.center = (size[0] // 2, size[1] // 2)

def main():
    screen = pygame.display.set_mode(size)  # Initialize the camera screen
    clock = pygame.time.Clock()  # Initialize a pygame

    cam = camera_setup()
    img = pygame.Surface(size) # To store camera frames

    current_word = pick_new_word() # Set word
    matching_symbols = [None, None, None, None, None]
    pred_letter = None
    pred_symbol = None

    while True:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the screen is closed, quit the program
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pred_letter, pred_symbol = predict_frame(img, focus_frame)

                    # Check if word contains guessed letter
                    for i in range(len(current_word)):
                        if pred_letter == current_word[i]:
                            matching_symbols[i] = pred_symbol

                if event.key == pygame.K_q:
                    pygame.quit()

        if all(elem is not None for elem in matching_symbols):
            current_word = pick_new_word()  # Set word
            matching_symbols = [None, None, None, None, None]
            pred_letter = None
            pred_symbol = None

        # Capture image from camera
        try:
            cam.get_image(img)
        except Exception:
            pass

        display(screen, img, current_word, pred_letter, pred_symbol, matching_symbols)

        clock.tick(60)  # Limits frame rate to 60 FPS

def predict_frame(img, frame):
    label_key = ['a', 'c', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't']

    cropped_image = img.subsurface(frame)

    # Extract pixel data from pygame surface
    #img_array = np.array(cropped_image)
    #img_array = pygame.surfarray.pixels3d(cropped_image) # Array: (width, height, 3)
    #img_array = np.transpose(img_array, (1, 0, 2)) # Match training data
    #img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
    # Get surface and convert to NumPy
    cropped_surface = img.subsurface(frame)
    img_array = pygame.surfarray.array3d(cropped_surface)

    # Match training data
    img_array = img_array.transpose([1, 0, 2])
    input_picture = np.expand_dims(img_array, axis=0) / 255.0

    # Get predicted label
    prediction = model.predict(input_picture)
    predicted_index = np.argmax(prediction)
    pred_letter = label_key[predicted_index]

    prediction_symbol = pygame.image.load(f"pictures/{pred_letter}.png")

    print(prediction)

    return pred_letter, prediction_symbol

def display(screen, img, word, pred_letter, pred_symbol, matching_symbols):
    # Display Camera Image
    # img = pygame.transform.flip(img, True, False)
    screen.blit(img, (0, 0))

    # Display focus frame
    pygame.draw.rect(screen, 0, focus_frame, 10)

    # Display side bars
    pygame.draw.rect(screen, (250, 237, 205), ((0, 0), (size[0]/5, size[1])))
    pygame.draw.rect(screen, (250, 237, 205), ((size[0]/5*4, 0), (size[0]/5, size[1])))

    # Display word to spell
    if word is not None:
        for i in range(len(word)):
            # Place letter based on index and center
            letter = word[i].capitalize()
            letter_surface = font.render(letter, True, 0)
            letter_rect = letter_surface.get_rect(center=(size[0]/10, (size[1]/(len(word)+1)) * (i+1)))
            screen.blit(letter_surface, letter_rect)

    # Display word spelled in symbols
    for i in range(len(matching_symbols)):
        # Place symbol based on index and center
        sym_img = matching_symbols[i]
        if sym_img is not None:
            img_rect = sym_img.get_rect(center=(size[0]/10*9, (size[1]/(len(matching_symbols)+1)) * (i+1))) # Get center of letter
            screen.blit(sym_img, img_rect)

    # Display current prediction (letter + symbol)
    if pred_letter is not None:
        pred_letter_text = font.render(pred_letter.capitalize(), True, 0)
        pred_letter_rect = pred_letter_text.get_rect(center=(size[0] / 2, size[1] / 4)) # Get center of letter
        pygame.draw.rect(screen, (255, 255, 255), pred_letter_rect)
        screen.blit(pred_letter_text, pred_letter_rect)

    if pred_symbol is not None:
        img_rect = pred_symbol.get_rect(center=(size[0] / 2, size[1] / 4 * 3))  # Get center of letter
        screen.blit(pred_symbol, img_rect)


    pygame.display.flip()  # Update Screen

def pick_new_word():
    word = random.choice(words)
    print(word)
    return word

def camera_setup():
    # Setup Camera
    pygame.camera.init()
    camlist = pygame.camera.list_cameras()
    if not camlist:
        print("No camera found")
        pygame.quit()

    cam = pygame.camera.Camera(camlist[1], size)
    cam.start()

    return cam

# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()