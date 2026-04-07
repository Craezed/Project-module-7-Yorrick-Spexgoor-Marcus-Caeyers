import pygame
import pygame.camera

def main():

    size = (1080, 720)  # Set the screen size
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
    rect = pygame.Rect([0, 0], [200, 200])
    rect.center = (size[0] // 2, size[1] // 2)

    img = pygame.Surface(size) # To store camera frames

    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the screen is closed, quit the program
                pygame.quit()

        # Capture image from camera
        try:
            cam.get_image(img)
        except Exception as e:
            print(f"Error capturing image: {e}")
            break

        screen.blit(img, (0, 0))
        pygame.draw.rect(screen, 999999, rect, 10)

        pygame.display.flip() # Update Screen

        clock.tick(60)  # Limits frame rate to 60 FPS




# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()