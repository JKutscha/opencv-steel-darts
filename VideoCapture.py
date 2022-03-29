from threading import Thread
import cv2
import time

DEBUG = False

class VideoStream(Thread):
    def __init__(self, camName:str,camID=0):
        Thread.__init__(self)
        # initialize the video camera stream and read the first frame
        # from the stream
        self.grabbed = False
        self.frame = None
        self.camID = camID
        self.camName = camName
        self.stream = cv2.VideoCapture(self.camID)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def run(self):
        print ("Starting " + self.camName)
        if self.stream.isOpened():
            self.grabbed, self.frame = self.stream.read()
            if DEBUG:
                self.initCamPreview()
            # keep looping infinitely until the thread is stopped
            self.update()

    def update(self):
        while not self.stopped:
            # otherwise, read the next frame from the stream
            self.grabbed, self.frame = self.stream.read()
            if DEBUG:
                if self.grabbed:
                    cv2.imshow(self.camName, self.frame)
                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    self.stop()

    def read(self):
        # return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        if DEBUG:
            cv2.destroyWindow(self.camName)

    def initCamPreview(self):
        cv2.namedWindow(self.camName)

if __name__ == '__main__':
    DEBUG = True
    # test cams
    thread1 = VideoStream("Camera 1", 0)
    thread2 = VideoStream("Camera 2", 2)
    thread1.start()
    thread2.start()