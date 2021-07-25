import cv2

#Capture a few samples of images of a person's face from the liv camera frame and assihgn IDs to the captured images.
def generate_dataset():
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    Id = 1
    sampleNum = 0

    while (True):
        # capture image
        ret, img = cam.read()
        # convert the image into grayscale because the viola-jones algorithm will segregate the image through the brightness of a pixel from black to gray and white.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # increment the sample number by one each time it detects a face
            sampleNum = sampleNum + 1
            # saving the captured face in the dataSet folder and x,y is the top left coordinate of the face rectangle and h,w is the height and weight of the image in terms of pixels
            cv2.imwrite("dataSet/User." + str(Id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            # live frame from camera to show up
            cv2.imshow('frame', img)

        # wait for 100 milliseconds to capture 20 images or quit the operation using "q"
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is more than 20
        elif sampleNum > 20:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Collected Samples Successfully.")
generate_dataset()
