import cv2
import dlib
import numpy as np
from imutils import face_utils
from scipy.ndimage import zoom
from scipy.spatial import distance
from tensorflow.keras.saving import load_model

global shape_x
global shape_y


def show_webcam():
    shape_x = 48
    shape_y = 48

    def eye_aspect_ratio(eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def detect_face(frame):

        # Cascade classifier pre-trained model
        cascPath = r'D:\projectworkspace\moodechoinsight\MoodEchoInsight\base\services\face_landmarks.dat'
        faceCascade = cv2.CascadeClassifier(cascPath)

        # BGR -> Gray conversion
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Cascade MultiScale classifier
        detected_faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,
                                                      minNeighbors=6,
                                                      minSize=(
                                                          shape_x, shape_y),
                                                      flags=cv2.CASCADE_SCALE_IMAGE)
        coord = []

        for x, y, w, h in detected_faces:
            if w > 100:
                sub_img = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)
                coord.append([x, y, w, h])

        return gray, detected_faces, coord

    def extract_face_features(faces, offset_coefficients=(0.075, 0.05)):
        gray = faces[0]
        detected_face = faces[1]

        new_face = []

        for det in detected_face:
            x, y, w, h = det

            horizontal_offset = np.int(np.floor(offset_coefficients[0] * w))
            vertical_offset = np.int(np.floor(offset_coefficients[1] * h))

            extracted_face = gray[y + vertical_offset:y + h,
                             x + horizontal_offset:x - horizontal_offset + w]

            new_extracted_face = zoom(extracted_face,
                                      (shape_x / extracted_face.shape[0],
                                       shape_y / extracted_face.shape[1]))

            new_extracted_face = new_extracted_face.astype(np.float32)

            new_extracted_face /= float(new_extracted_face.max())

            new_face.append(new_extracted_face)

        return new_face

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (jStart, jEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

    (eblStart, eblEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
    (ebrStart, ebrEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

    model = load_model(
        r'D:\projectworkspace\moodechoinsight\MoodEchoInsight\base\services\video.h5')
    face_detect = dlib.get_frontal_face_detector()
    predictor_landmarks = dlib.shape_predictor(
        r"D:\projectworkspace\moodechoinsight\MoodEchoInsight\base\services\face_landmarks.dat")

    video_capture = cv2.VideoCapture(0)

    # list of each sentiment

    angry_list = []
    fear_list = []
    sad_list = []
    disgust_list = []
    surprise_list = []
    neutral_list = []
    happy_list = []

    angry_average = 0.0
    fear_average = 0.0
    sad_average = 0.0
    disgust_average = 0.0
    surprise_average = 0
    neutral_average = 0.0
    happy_average = 0.0

    while True:

        ret, frame = video_capture.read()
        if ret:
            face_index = 0

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = face_detect(gray, 1)

            for (i, rect) in enumerate(rects):

                shape = predictor_landmarks(gray, rect)
                shape = face_utils.shape_to_np(shape)

                (x, y, w, h) = face_utils.rect_to_bb(rect)
                face = gray[y:y + h, x:x + w]

                try:

                    face = zoom(face, (
                        shape_x / face.shape[0], shape_y / face.shape[1]))

                except:
                    break

                face = face.astype(np.float32)

                face /= float(face.max())
                face = np.reshape(face.flatten(), (1, 48, 48, 1))

                prediction = model.predict(face)
                prediction_result = np.argmax(prediction)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

                # for (j, k) in shape:
                #     cv2.circle(frame, (j, k), 1, (0, 0, 255), -1)

                # Create list for each sentiment type
                # Store values in their list
                # Find the mean value & store detection_table column float NULL

                angry_list.append(round(prediction[0][0], 2))
                sad_list.append(round(prediction[0][4], 2))
                neutral_list.append(round(prediction[0][6], 2))
                surprise_list.append(round(prediction[0][5], 2))
                disgust_list.append(round(prediction[0][1], 2))
                fear_list.append(round(prediction[0][2], 2))
                happy_list.append(round(prediction[0][3], 2))

                print("Angry={}".format(str(round(prediction[0][0], 2))))
                print("Sad={}".format(str(round(prediction[0][4], 2))))
                print("Neutral={}".format(str(round(prediction[0][6], 2))))
                print("Surprise={}".format(str(round(prediction[0][5], 2))))
                print("Disgust={}".format(str(round(prediction[0][1], 2))))
                print("Fear={}".format(str(round(prediction[0][2], 2))))
                print("Happy={}".format(str(round(prediction[0][3], 2))))

                cv2.putText(frame, "----------------", (40, 100 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 0)
                cv2.putText(frame, "Emotional report : Face #" + str(i + 1),
                            (40, 120 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                cv2.putText(frame,
                            "Angry : " + str(round(prediction[0][0], 3)),
                            (40, 140 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                cv2.putText(frame,
                            "Disgust : " + str(round(prediction[0][1], 3)),
                            (40, 160 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
                cv2.putText(frame, "Fear : " + str(round(prediction[0][2], 3)),
                            (40, 180 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                cv2.putText(frame,
                            "Happy : " + str(round(prediction[0][3], 3)),
                            (40, 200 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                cv2.putText(frame, "Sad : " + str(round(prediction[0][4], 3)),
                            (40, 220 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                cv2.putText(frame,
                            "Surprise : " + str(round(prediction[0][5], 3)),
                            (40, 240 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
                cv2.putText(frame,
                            "Neutral : " + str(round(prediction[0][6], 3)),
                            (40, 260 + 180 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)

                if prediction_result == 0:
                    cv2.putText(frame, "Angry", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Angry")
                elif prediction_result == 1:
                    cv2.putText(frame, "Disgust", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Disgust")
                elif prediction_result == 2:
                    cv2.putText(frame, "Fear", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Fear")
                elif prediction_result == 3:
                    cv2.putText(frame, "Happy", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Happy")
                elif prediction_result == 4:
                    cv2.putText(frame, "Sad", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Sad")
                elif prediction_result == 5:
                    cv2.putText(frame, "Surprise", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Surprise")
                else:
                    cv2.putText(frame, "Neutral", (x + w - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Neutral")

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]

                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0

                # leftEyeHull = cv2.convexHull(leftEye)
                # rightEyeHull = cv2.convexHull(rightEye)
                # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # nose = shape[nStart:nEnd]
                # noseHull = cv2.convexHull(nose)
                # cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)

                # mouth = shape[mStart:mEnd]
                # mouthHull = cv2.convexHull(mouth)
                # cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

                # jaw = shape[jStart:jEnd]
                # jawHull = cv2.convexHull(jaw)
                # cv2.drawContours(frame, [jawHull], -1, (0, 255, 0), 1)

                # ebr = shape[ebrStart:ebrEnd]
                # ebrHull = cv2.convexHull(ebr)
                # cv2.drawContours(frame, [ebrHull], -1, (0, 255, 0), 1)
                # ebl = shape[eblStart:eblEnd]
                # eblHull = cv2.convexHull(ebl)
                # cv2.drawContours(frame, [eblHull], -1, (0, 255, 0), 1)

            cv2.putText(frame, 'Number of Faces : ' + str(len(rects)),
                        (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, 155, 1)
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


    # return angry_list, sad_list, happy_list,disgust_list, surprise_list, neutral_list,fear_list

    def calculate_emotion_averages(angry_list, sad_list, happy_list,
                                   disgust_list, surprise_list, neutral_list,
                                   fear_list):
        # 1
        if angry_list:
            angry_average = round(sum(angry_list) / len(angry_list), 2)

        print("angry_average>>>>>>>>>>>>>>>>>", angry_average)
        # 2
        if sad_list:
            sad_average = round(sum(sad_list) / len(sad_list), 2)

        print("sad_average>>>>>>>>>>>>>>>>>", sad_average)
        # 3
        if happy_list:
            happy_average = round(sum(happy_list) / len(happy_list), 2)

        print("happy_average>>>>>>>>>>>>>>>>", happy_average)
        # 4
        if disgust_list:
            disgust_average = round(sum(disgust_list) / len(disgust_list), 2)

        print("disgust_average>>>>>>>>>", disgust_average)
        # 5
        if surprise_list:
            surprise_average = round(sum(surprise_list) / len(surprise_list),
                                     2)

        print("surprise_average>>>>>>>>>>>>>>", surprise_average)
        # 6
        if neutral_list:
            neutral_average = round(sum(neutral_list) / len(neutral_list), 2)

        print("neutral_average>>>>>>>>>>>>>", neutral_average)
        # 7
        if fear_list:
            fear_average = round(sum(fear_list) / len(fear_list), 2)

        print("fear_average>>>>>>>>>>>>>>", fear_average)


        avg = {"angry": angry_average,
               "sad": sad_average,
               "happy": happy_average,
               "disgust": disgust_average,
               "surprise": surprise_average,
               "neutral": neutral_average,
               "fear": fear_average
               }

        print(avg)
        return avg

    video_capture.release()
    cv2.destroyAllWindows()
    return calculate_emotion_averages(angry_list, sad_list, happy_list,
                                   disgust_list, surprise_list, neutral_list,
                                   fear_list)

    # When everything is done, release the capture