# use threading to increase performance of code using an OPENCV video stream
# adapted from: https://pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
# updated: 2022-04-02

from threading import Thread


class FastStream:
    '''
    base class for USB and PiCamera threaded video streams.

    read frames from a video stream in a dedicated thread, which an external
    process can poll as needed. this is more efficient as it decouples
    blocking I/O calls from the main process.

    have seen large impacts when using the RasPi camera module.
    in some cases it's boosted a program from 7-15 FPS to ~realtime (20-30 FPS).
    '''

    def __init__(self, *args, **kwargs):
        self.name = type(self).__name__  # name of the instance's class
        self.frame = None                # placeholder for most recent frame read off the stream
        self.streaming = True            # call self.stop() to change this and shutdown the stream

    def start(self):
        '''start thread that reads frames off video stream'''
        t = Thread(target=self._update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def read(self):
        '''
        return the most recent frame grabbed off the stream to another process.
        self.frame should be set by the child class in an update() method.
        '''
        return self.frame

    def stop(self):
        '''call this to stop the thread and shutdown the stream'''
        self.streaming = False
        self.stream.release()


class USBVideoStream(FastStream):
    '''
    read frames from a USB camera device in a dedicated thread.
    other code can poll frames from the stream as needed.

    @src_index:    believe this is the index of the USB device, either in the system
                   somewhere, or in OPENCV (or both??)
    @thread_name:  optionally pass in a string to name the video stream's thread.
                   necessary if using more than one instance of this class.
    '''

    import cv2 as cv  # import OPENCV

    def __init__(self, src_index=0, thread_name=None, *args, **kwargs):
        FastStream.__init__(self, *args, **kwargs)
        self.thread_name = thread_name if thread_name is not None else self.name
        self.stream = self.cv.VideoCapture(src_index)  # initialize an OPENCV video stream
        (self.grabbed, self.frame) = self.stream.read()  # read first frame

    def _update(self):
        '''grab video frames off the stream until stop signal received'''
        while self.streaming == True:
            (self.grabbed, self.frame) = self.stream.read()
        self.stream.release()

    def show(self):
        self.cv.imshow("Frame", self.read()[1])


class PicamVideoStream(FastStream):
    pass


if __name__ == '__main__':
    usbstream = USBVideoStream().start()

    print('warming up...')
    import time
    time.sleep(2)

    print('displaying feed from video stream')
    print('USE ^C TO STOP')
    try:
        usbstream.show()
    except Exception as e:
        print(e)
        print('shutting down')
        usbstream.stop()
