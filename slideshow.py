#importing the necessary libraries
import pygame
import os
import time

#initialize pygame
pygame.init()

#constants
screen_width = 800
screen_height = 600
image_display_height = 500 #space for images
caption_bar_height = 100 #space for captions
bg_colour = (0, 0, 0) #black colour
text_colour = (255, 255, 255) #white
font = pygame.font.Font(None, 36) #default font size 36
slide_duration = 3

#setup display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Slideshow")

#load music
music_folder = "music"
music_files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
if music_files:
    pygame.mixer.music.load(os.path.join(music_folder, music_files[0]))
    pygame.mixer.music.play(-1) #loop forever

#load images and captions
images_folder = "images"
caption_file = "captions.txt"

#read captions
captions = {}
if os.path.exists(caption_file):
    with open(caption_file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("|")
            if len(parts)==2:
                captions[parts[0]] = parts[1]

#load image
image_files = [f for f in os.listdir(images_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
image_files.sort() #sort image files alphabetically

# Check if there are any valid images in the folder
if len(image_files) == 0:
    print(f"Error: No valid image files found in the folder '{images_folder}'.")
    pygame.quit()
    exit(1)

#function to display image and caption
def show_slide(image_path, caption):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screen_width, image_display_height))

    # Clear the screen and display the image
    screen.fill(bg_colour)
    screen.blit(image, (0, 0))

    # Draw caption bar
    pygame.draw.rect(screen, (50, 50, 50), (0, image_display_height, screen_width, caption_bar_height))

    # Render the specific caption text
    caption_text = font.render(caption, True, text_colour)
    text_rect = caption_text.get_rect(center=(screen_width // 2, image_display_height + (caption_bar_height // 2)))
    screen.blit(caption_text, text_rect)
    pygame.display.flip()


#main loop
running = True
index = 0
while running:
     if index >= len(image_files):
         index = 0
     image_name = image_files[index]
     image_path = os.path.join(images_folder, image_name)
     caption = captions.get(image_name, "A special moment ❤") # default caption if not found
     show_slide(image_path, caption)
     time.sleep(slide_duration) #wait before showing next slide
     index += 1
     # start_time = time.time()
     # while time.time() - start_time < slide_duration:
     #     for event in pygame.event.get():
     #         if event.type == pygame.QUIT:
     #             running = False
     #         elif event.type == pygame.KEYDOWN:
     #             if event.key == pygame.K_RIGHT:
     #                 index = (index + 1) % len(image_files)
     #                 break
     #             elif event.key == pygame.K_LEFT:
     #                 index = (index - 1) % len(image_files)
     #                 break
     #             elif event.key == pygame.K_ESCAPE:
     #                 running = False
     #                 index = (index - 1) % len(image_files)

     #event handling(exit on close button)
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False

pygame.quit()
