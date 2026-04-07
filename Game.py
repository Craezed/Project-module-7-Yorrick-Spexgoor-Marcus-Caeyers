import pygame

def main():
    size = (640, 320)  # Set the screen size
    pygame.init()  # Initialize the pygame library
    screen = pygame.display.set_mode(size)  # Initialize the pygame screen
    clock = pygame.time.Clock()  # Initialize a pygame timer


    while True:

        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the screen is closed, quit the program
                pygame.quit()

        screen.fill(0)  # Fill the whole screen with the color black

        pygame.draw.rect(screen, 999999, ([50, 50], [50, 50]))

        pygame.display.flip()  # Update the screen

        clock.tick(60)  # Limits frame rate to 60 FPS




# Run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()