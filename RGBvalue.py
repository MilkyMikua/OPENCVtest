# This code output the RGB value of the detected area
# everything else same as the main
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

        # Convert the frame to the RGB color space
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Define a range of green color in RGB color space
        lower_green = np.array([0, 100, 0])
        upper_green = np.array([100, 255, 100])

        # Threshold the RGB image to get only green colors
        green_mask = cv2.inRange(rgb_frame, lower_green, upper_green)

        # Find contours of green regions in the image
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image and compute the average RGB value of the green areas
        green_pixels = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                mask = np.zeros_like(green_mask)
                cv2.drawContours(mask, [contour], 0, 255, -1)
                green_pixels.append(rgb_frame[mask == 255])

        # Compute the average RGB value of the green areas
        if len(green_pixels) > 0:
            green_pixels = np.concatenate(green_pixels)
            green_rgb = np.mean(green_pixels, axis=0)
            print("Detected green with RGB value: ", green_rgb)

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


