# This code use Lab color Space instead of RGB. The core ideas same as the main
import cv2
import numpy as np

# Create a VideoCapture object to access the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
else:
    # Loop through the video frames
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            print("Error: Could not read frame from camera")
            break

        # Convert the frame to the Lab color space
        lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        # Define a range of green color in Lab color space
        lower_green = np.array([0, -128, -128])
        upper_green = np.array([100, 127, 127])

        # Threshold the Lab image to get only green colors
        green_mask = cv2.inRange(lab_frame, lower_green, upper_green)

        # Find contours of green regions in the image
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Flag to indicate whether green is present in the current frame
        green_detected = False

        # Draw contours on the original image and set the flag to True if a green contour is found
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                green_detected = True
        '''if len(green_pixels) > 0:
            green_pixels = np.concatenate(green_pixels)
            green_rgb = np.mean(green_pixels, axis=0)
            print("Detected green with RGB value: ", green_rgb)'''

        # Print 1 if green is detected in the current frame
        if green_detected:
            print("1")
        else:
            print("0")

        # Display the frame
        cv2.imshow('Camera', frame)

        # Wait for 1 millisecond and check if the 'q' key was pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Save the last frame as an image file
    cv2.imwrite('last_frame.jpg', frame)

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
