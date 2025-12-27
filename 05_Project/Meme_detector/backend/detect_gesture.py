import sys
import cv2
import json
import numpy as np

# Try importing mediapipe with error handling
try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_face_mesh = mp.solutions.face_mesh
except AttributeError:
    # If solutions module doesn't exist, try alternative import
    print(json.dumps({'success': False, 'error': 'MediaPipe version incompatible. Please install: pip install mediapipe>=0.10.0'}))
    sys.exit(1)
except ImportError as e:
    print(json.dumps({'success': False, 'error': f'MediaPipe not installed: {str(e)}'}))
    sys.exit(1)

# --- Gesture Logic ---
def is_thumb_up(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    if thumb_tip.y >= thumb_ip.y:
        return False
        
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            return False
            
    return True

def is_pointing(hand_landmarks):
    index_tip = hand_landmarks.landmark[8]
    index_pip = hand_landmarks.landmark[6]
    
    if index_tip.y >= index_pip.y:
        return False
        
    check_fingers = [(12, 10), (16, 14), (20, 18)]
    
    for tip, pip in check_fingers:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            return False
            
    return True

def is_touching_head(hand_landmarks, face_landmarks):
    if not face_landmarks:
        return False
        
    forehead = face_landmarks.landmark[10]
    middle_tip = hand_landmarks.landmark[12]
    
    if middle_tip.y <= forehead.y + 0.05:
        return True
        
    return False

def detect_gesture(image_path):
    """
    Detect gesture from image file
    Returns: dict with gesture, confidence, and meme filename
    """
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        return {
            'success': False,
            'error': 'Could not read image'
        }
    
    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Initialize detectors
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands, \
         mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5) as face_mesh:
        
        # Process image
        results_hands = hands.process(image_rgb)
        results_face = face_mesh.process(image_rgb)
        
        # Get face landmarks
        face_lms = None
        if results_face.multi_face_landmarks:
            face_lms = results_face.multi_face_landmarks[0]
        
        # Check for gestures
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                # Check gestures in priority order
                if is_touching_head(hand_landmarks, face_lms):
                    return {
                        'success': True,
                        'gesture': 'touching_head',
                        'confidence': 0.92,
                        'meme': 'reaction_head.jpg'
                    }
                elif is_thumb_up(hand_landmarks):
                    return {
                        'success': True,
                        'gesture': 'thumbs_up',
                        'confidence': 0.95,
                        'meme': 'reaction_thumb.jpg'
                    }
                elif is_pointing(hand_landmarks):
                    return {
                        'success': True,
                        'gesture': 'pointing',
                        'confidence': 0.90,
                        'meme': 'reaction_point.jpg'
                    }
        
        # No gesture detected
        return {
            'success': True,
            'gesture': 'none',
            'confidence': 0.0,
            'meme': None
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'No image path provided'}))
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = detect_gesture(image_path)
    print(json.dumps(result))
