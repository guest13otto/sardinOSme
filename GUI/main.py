import pygame
import cv2
from Module_Base import Module
from plot import Plot


def nothing(x):
    pass


def main():
    pygame.init()
    pygame.display.set_caption("ControlGUI(姐姐牛逼")
    screen = pygame.display.set_mode((1080, 720))
    running = True
    clock = pygame.time.Clock()

    plot = Plot(screen, 1080, 720)

    cv2.namedWindow('Track Bars')
    cv2.createTrackbar('strafe', 'Track Bars', 0, 100, nothing)
    cv2.createTrackbar('drive', 'Track Bars', 0, 100, nothing)
    cv2.createTrackbar('yaw', 'Track Bars', 0, 100, nothing)
    cv2.createTrackbar('tilt', 'Track Bars', 0, 100, nothing)
    cv2.createTrackbar('updown1', 'Track Bars', 0, 100, nothing)
    cv2.createTrackbar('updown2', 'Track Bars', 0, 100, nothing)

    while running:
        strafe = (cv2.getTrackbarPos('strafe', 'Track Bars') - 50) / 50
        drive = (cv2.getTrackbarPos('drive', 'Track Bars') - 50) / 50
        yaw = (cv2.getTrackbarPos('yaw', 'Track Bars') - 50) / 50
        tilt = (cv2.getTrackbarPos('tilt', 'Track Bars') - 50) / 50
        updown1 = (cv2.getTrackbarPos('updown1', 'Track Bars') - 50) / 50
        updown2 = (cv2.getTrackbarPos('updown2', 'Track Bars') - 50) / 50

        plot.update(strafe, drive, yaw, tilt, updown1, updown2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)


if __name__ == "__main__":
    main()
