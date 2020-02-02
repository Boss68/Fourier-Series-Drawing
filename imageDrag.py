import pygame,os

WINDOW=pygame.display.set_mode((800,600))
availExt=['.jpg','.jpeg','.png','.gif','.bmp','.pcx','.tga','.tif','.lbm','.pbm','.pgm','.ppm','.xpm']
image=None
running=True
while running:
    if image!=None:
        WINDOW.blit(pygame.transform.scale(image,(800,600)),(0,0))
    pygame.display.update()
    WINDOW.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.DROPFILE:
            if os.path.splitext(event.file)[1] in availExt:
                print('valid image')
                image=pygame.image.load(event.file)
            else:
                print('invalid image')
        if event.type == pygame.QUIT:
            pygame.quit()
            running=False