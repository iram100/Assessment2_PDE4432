"""
camera_keepalive.py

A robust webcam tester that:
 - uses DirectShow on Windows (cv2.CAP_DSHOW) for more stable capture
 - auto-reconnects if frames stop arriving
 - logs camera open/close and errors to camera_debug.log
 - shows feed and keeps running until you press 'q'

Usage:
  python camera_keepalive.py

Config at top of file: CAM_INDEX, FRAME_W/H, RECONNECT_DELAY (s), MAX_BAD_FRAMES before reconnect.

Author: original for your project.
"""

import cv2, time, os, sys, logging
from datetime import datetime

# ---------- CONFIG ----------
CAM_INDEX = 0                 # try 0, 1, 2... if your webcam uses another index
FRAME_W = 640
FRAME_H = 480
RECONNECT_DELAY = 2.0         # seconds before attempting to reopen camera when it fails
MAX_BAD_FRAMES = 30           # if this many consecutive bad frames, attempt reconnect
SAVE_DEBUG_EVERY = 0          # set >0 to save a debug frame every N seconds (0 disables)
LOGFILE = "camera_debug.log"
# ----------------------------

# set up logging
logging.basicConfig(filename=LOGFILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def open_camera(index):
    """Open camera; on Windows try DirectShow (CAP_DSHOW) for stability."""
    try:
        if os.name == "nt":
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            logging.warning(f"VideoCapture.open({index}) failed.")
            return None
        # set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
        # small warm-up
        time.sleep(0.2)
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
        logging.info(f"Camera opened index={index} size={actual_w}x{actual_h} fps={fps:.2f}")
        return cap
    except Exception as e:
        logging.exception("Exception opening camera:")
        return None

def close_camera(cap):
    try:
        if cap:
            cap.release()
            logging.info("Camera released.")
    except Exception as e:
        logging.exception("Exception releasing camera:")

def main():
    cap = None
    last_debug_save = 0
    bad_frames = 0
    last_open_attempt = 0
    try:
        while True:
            if cap is None or not cap.isOpened():
                # rate-limit open attempts
                if time.time() - last_open_attempt < RECONNECT_DELAY:
                    time.sleep(0.1)
                    continue
                last_open_attempt = time.time()
                cap = open_camera(CAM_INDEX)
                bad_frames = 0
                if cap is None:
                    logging.error(f"Failed to open camera index {CAM_INDEX}. Retrying in {RECONNECT_DELAY}s")
                    time.sleep(RECONNECT_DELAY)
                    continue

            ret, frame = cap.read()
            if not ret or frame is None:
                bad_frames += 1
                logging.warning(f"Bad frame #{bad_frames} (ret={ret}).")
                if bad_frames >= MAX_BAD_FRAMES:
                    logging.error(f"Too many bad frames ({bad_frames}). Reopening camera after {RECONNECT_DELAY}s.")
                    close_camera(cap)
                    cap = None
                    time.sleep(RECONNECT_DELAY)
                else:
                    # short sleep to give driver time
                    time.sleep(0.05)
                continue

            # good frame
            bad_frames = 0
            # optionally save periodic debug frames
            if SAVE_DEBUG_EVERY > 0 and (time.time() - last_debug_save) > SAVE_DEBUG_EVERY:
                fn = f"debug_frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(fn, frame)
                logging.info(f"Saved debug frame {fn}")
                last_debug_save = time.time()

            # display (mirror for convenience)
            disp = cv2.flip(frame, 1)
            h, w = disp.shape[:2]
            cv2.putText(disp, f"{w}x{h}", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
            cv2.imshow("Camera Keepalive - press 'q' to quit", disp)

            # handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logging.info("Exit requested by user.")
                break

        # end while
    except KeyboardInterrupt:
        logging.info("Interrupted by user (KeyboardInterrupt).")
    except Exception as e:
        logging.exception("Unhandled exception in main loop:")
    finally:
        close_camera(cap)
        cv2.destroyAllWindows()
        logging.info("Exiting.")

if __name__ == "__main__":
    main()
