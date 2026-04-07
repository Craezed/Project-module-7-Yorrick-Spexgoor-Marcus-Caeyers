import cv2
import pygame
import pygame.camera
import os

size = (2560/2, 1440/2)
frame_size = (256, 256)

last_time_pressed = 0

def main():

    pygame.init()  # Initialize the pygame library
    pygame.camera.init()
    screen = pygame.display.set_mode(size)  # Initialize the pygame screen
    clock = pygame.time.Clock()  # Initialize a pygame timer

    camlist = pygame.camera.list_cameras()
    if not camlist:
        print("No camera found")
        pygame.quit()

    cam = pygame.camera.Camera(camlist[0], size)
    cam.start()

    # Create frame
    rect = pygame.Rect([0, 0], frame_size)
    rect.center = (size[0] / 2, size[1] / 2)

    img = pygame.Surface(size) # To store camera frames

    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the screen is closed, quit the program
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                Key_Check(img, rect, screen, pygame.key.name(event.key))

        # Capture image from camera
        try:
            cam.get_image(img)
        except Exception as e:
            print(f"Error capturing image: {e}")
            break

        # Display Image
        img = pygame.transform.flip(img, True, False)
        screen.blit(img, (0, 0))
        pygame.draw.rect(screen, 0, rect, 10)

        pygame.display.flip() # Update Screen

        clock.tick(60)  # Limits frame rate to 60 FPS

def Key_Check(img, frame, screen, key):
    possible_keys = ['a', 'k', 't', 'e', 'r']

    print(key)

    if key in possible_keys:
        cropped_image = img.subsurface(frame)
        screen.blit(cropped_image, (0,0))

        if not os.path.isfile(f"{key}"):
            os.makedirs(f"{key}")

        files = os.listdir(f"{key}")
        i = len(files)
        pygame.image.save(cropped_image, f"{key}/test{i}.png")





# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()