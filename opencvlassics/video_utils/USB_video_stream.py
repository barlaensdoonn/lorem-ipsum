# use threading to increase performance of code using an OPENCV video stream
# adapted from: https://pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
# updated: 2022-04-02

import cv2 as cv
from threading import Thread


class USBVideoStream:
    '''
    read frames from a USB camera device in a dedicated thread.
    other code can poll frames from this thread as needed, which increases overall
    performance as reading from a video stream is now non-blocking.

    @src_index:    believe this is the index of the USB device, either in the system
                   somewhere, or in OPENCV (or both??)
    @thread_name:  name the thread.
    '''

    def __init__(self, src=0, name="USBVideoStream"):
        self.name = name
        self.stopped = False                # change to signal thread to stop
        self.stream = cv.VideoCapture(src)  # initialize the OPENCV video stream
        (self.grabbed, self.frame) = self.stream.read()  # read first frame

    def start(self):
        '''start thread that reads frames off video stream'''
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        '''loop indefinitely, grabbing video frames off the stream, until stop signal received'''
        while self.stopped == False:
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        '''return most recent frame (set in update() method)'''
        return self.frame

    def stop(self):
        '''signal the thread to stop'''
        self.stopped = True
