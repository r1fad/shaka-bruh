import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)
import Leap
import time

class SampleListener(Leap.Listener):
    frame_count = 0
    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):

        frame = controller.frame()
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
