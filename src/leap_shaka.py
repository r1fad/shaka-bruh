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
import json, requests
from slackclient import SlackClient

os.system("sudo service leapd restart")

f = open("dankmemes.txt","r")
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

        # for gesture in frame.gestures():
        #     if gesture.type is Leap.Gesture.TYPE_SWIPE:
        #         swipe = Leap.SwipeGesture(gesture)
        #         if not SampleListener.sent:
        #             SampleListener.sent = True
        #             url = 'https://hooks.slack.com/services/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'
        #             d = {}
        #             d["text"] = 'Here\'s one from Rifad: ' + SampleListener.currentUrl
        #             #payload = json.loads('{"text":"' + SampleListener.currentUrl +' "}')
        #             headers = {'Content-type': 'application/json'}
        #             r = requests.post(url, data=json.dumps(d), headers=headers)
        #             print 'meme shared to Slack successfully!'

        shaka_thumb = False
        shaka_pinky = False
        #not_fingers = False
        shaka_index = False
        shaka_middle = False
        shaka_ring = False
        for finger in frame.fingers:
            if finger.type == 4:
                if finger.is_extended == True:
                    shaka_pinky = True
            elif finger.type == 0:
                if finger.is_extended == True:
                    shaka_thumb = True
            elif finger.type == 1:
                if finger.is_extended == True:
                    shaka_index = True
            elif finger.type == 2:
                if finger.is_extended == True:
                    shaka_middle = True
            elif finger.type == 3:
                if finger.is_extended == True:
                    shaka_ring = True

        if shaka_thumb and shaka_pinky and not shaka_ring and not shaka_middle and not shaka_index:
            SampleListener.frame_count += 1
        elif shaka_index and shaka_middle and not shaka_ring and not shaka_thumb and not shaka_pinky:
            if not SampleListener.sent:
                SampleListener.sent = True
                url = 'https://hooks.slack.com/services/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'
                d = {}
                d["text"] = 'Here\'s one from Rifad: ' + SampleListener.currentUrl
                #payload = json.loads('{"text":"' + SampleListener.currentUrl +' "}')
                headers = {'Content-type': 'application/json'}
                r = requests.post(url, data=json.dumps(d), headers=headers)
                print 'meme shared to Slack successfully!'

        if SampleListener.frame_count == 30:
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
