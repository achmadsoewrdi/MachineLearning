import cv2
import mediapipe as mp
import numpy as np
import os
import time

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# --- Load Assets ---
ASSETS_DIR = "assets"
REACTION_THUMB = os.path.join(ASSETS_DIR, "reaction_thumb.jpg")
REACTION_POINT = os.path.join(ASSETS_DIR, "reaction_point.jpg")
REACTION_HEAD = os.path.join(ASSETS_DIR, "reaction_head.jpg")

# Preload images
img_thumb = cv2.imread(REACTION_THUMB)
img_point = cv2.imread(REACTION_POINT)
img_head = cv2.imread(REACTION_HEAD)

# Initial warning if images are missing (will check again in loop if needed or just handle None)
if img_thumb is None: print(f"Warning: Could not load {REACTION_THUMB}")
if img_point is None: print(f"Warning: Could not load {REACTION_POINT}")
if img_head is None: print(f"Warning: Could not load {REACTION_HEAD}")

# --- Gesture Logic ---
def is_thumb_up(hand_landmarks):
    # Thumb: 4 (Tip), 3 (IP)
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    # Thumb tip should be higher (smaller y) than IP for typical thumbs up
    # Note: Orientation matters. Assuming hand is upright.
    if thumb_tip.y >= thumb_ip.y:
        return False
        
    # Check if other fingers are closed (Tip below PIP)
    # 8 (Index), 12 (Middle), 16 (Ring), 20 (Pinky)
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    for tip, pip in zip(finger_tips, finger_pips):
        # If any finger tip is HIGHER (smaller y) than PIP, it's open
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            return False
            
    return True

def is_pointing(hand_landmarks):
    # Index open, others closed
    index_tip = hand_landmarks.landmark[8]
    index_pip = hand_landmarks.landmark[6]
    
    # Index should be up (Tip higher/smaller y than PIP)
    if index_tip.y >= index_pip.y:
        return False
        
    # Other fingers closed (Middle, Ring, Pinky)
    check_fingers = [(12, 10), (16, 14), (20, 18)]
    
    for tip, pip in check_fingers:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            return False
            
    return True

def is_touching_head(hand_landmarks, face_landmarks):
    if not face_landmarks:
        return False
        
    # Face landmark 10 is forehead
    forehead = face_landmarks.landmark[10]
    
    # Check middle finger tip (12) or index (8) relative to forehead
    # Using middle finger as a proxy for the hand
    middle_tip = hand_landmarks.landmark[12]
    
    # Condition: Hand Y <= Forehead Y (Hand is above or at forehead level)
    # Using a slightly relaxed threshold
    if middle_tip.y <= forehead.y + 0.05: # +0.05 allows it to be slightly below the exact point
        return True
        
    return False

# --- Main Loop ---
def main():
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened
    if not cap.isOpened():
        print("Error: Camera not found or could not be opened.")
        return

    # Initialize Detectors
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands, \
         mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        
        last_reaction_time = 0
        current_reaction_img = None
        REACTION_DURATION = 2.0 # Seconds to keep showing the meme
        
        print("Starting Gesture Meme Detector...")
        print("Press 'Esc' to exit.")

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip the image horizontally for a later selfie-view display
            # But process RGB after flip so left/right logic is intuitive? 
            # Standard webcam view is mirrored. MediaPipe expects RGB.
            # Let's flip first for user convenience
            image = cv2.flip(image, 1)

            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            results_hands = hands.process(image_rgb)
            results_face = face_mesh.process(image_rgb)

            image.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            detected_gesture = None
            
            # Draw Face
            face_lms = None
            if results_face.multi_face_landmarks:
                face_lms = results_face.multi_face_landmarks[0]
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_lms,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

            # Check Hands
            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    
                    # Check gestures
                    # Priority: Head > Thumb > Pointing (Arbitrary, but handling multihand can be complex)
                    # We'll just take the last detected one in loop
                    
                    if is_touching_head(hand_landmarks, face_lms):
                        detected_gesture = "Touching Head"
                        if img_head is not None:
                            current_reaction_img = img_head
                        last_reaction_time = time.time()
                    elif is_thumb_up(hand_landmarks):
                        detected_gesture = "Thumb Up"
                        if img_thumb is not None:
                            current_reaction_img = img_thumb
                        last_reaction_time = time.time()
                    elif is_pointing(hand_landmarks):
                        detected_gesture = "Pointing"
                        if img_point is not None:
                            current_reaction_img = img_point
                        last_reaction_time = time.time()

            # Handle Reaction Display
            if current_reaction_img is not None:
                if time.time() - last_reaction_time < REACTION_DURATION:
                    cv2.imshow('Meme Reaction', current_reaction_img)
                    
                    # Overlay text
                    if detected_gesture:
                         cv2.putText(image, f"Gesture: {detected_gesture}", (10, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    try:
                        cv2.destroyWindow('Meme Reaction')
                    except:
                        pass
                    current_reaction_img = None
            
            # Show main window
            cv2.imshow('MediaPipe Hand & Face', image)
            
            if cv2.waitKey(5) & 0xFF == 27:
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
