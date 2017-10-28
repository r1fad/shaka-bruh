import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)

import Leap
import time
from PIL import Image
import urllib, cStringIO
from random import randint
import os
import psutil
os.system("sudo service leapd restart")

f = open("memez.txt","r")
memez = f.readlines()


class SampleListener(Leap.Listener):
    frame_count = 0
    currentUrl = ''
    sent = False
    def on_connect(self, controller):
        print "Connected"

        #enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_frame(self, controller):
        frame = controller.frame()

        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                if not SampleListener.sent:
                    print SampleListener.currentUrl
                    SampleListener.sent = True

        shaka_thumb = False
        shaka_pinky = False
        not_fingers = False

        for finger in frame.fingers:
            if finger.type == 4:
                if finger.is_extended == True:
                    shaka_pinky = True

            elif finger.type == 0:
                if finger.is_extended == True:
                    shaka_thumb = True
            elif finger.is_extended == True:
                not_fingers = True

        if shaka_thumb and shaka_pinky and not not_fingers:
            SampleListener.frame_count += 1

        if SampleListener.frame_count == 60:
            print 'get a meme'
            SampleListener.sent = False

            for proc in psutil.process_iter():
                if proc.name() == "display":
                    proc.kill()

            URL = memez[randint(0,len(memez))]
            SampleListener.currentUrl = URL
            file1 = cStringIO.StringIO(urllib.urlopen(URL).read())
            img = Image.open(file1)
            basewidth = 1500
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            img.show()
            time.sleep(0.5)
            SampleListener.frame_count = 0



def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

     # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
