#import tensorflow as tf
import numpy as np
#import tensorflow_hub as hub
import cv2
import sys
import os
import shutil
import requests
import json
from tqdm import tqdm
import time

def make_predictions(inpath, outpath):
    MODEL_URL = "http://10.0.20.200:8501/v1/models/faster_rcnn_inception_v2:predict"

    try:
        shutil.rmtree(outpath)
    except:
        pass
    os.makedirs(outpath)
    
    files = os.listdir(inpath)
    
    i = -1
    tt = 0

    for f in tqdm(files):
        i = i+1
        img = cv2.imread(os.path.join(inpath, f))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (200, 200))
        np_input_data = np.expand_dims(img_resized, axis=0)
        input_data = {"instances": np_input_data.tolist()}

        t0 = time.time()
        try:
            print("sending request to detection-serving...")
            res = requests.post(MODEL_URL, json=input_data) 
        except requests.exceptions.RequestException:
            print("ERROR: Request error, did you start Tensorflow Serving?")
            sys.exit()
        except Exception as e:
            raise e

        td = time.time()-t0
        print("Amount of seconds to predict frame is..", td)
        tt = tt+td

        if (res.status_code == 400):
            print("Error:", res.text)
            pass
        else:
            t0 = time.time()
            detector_output = res.json()["predictions"][0]
            print("Amount of seconds to get JSON:", time.time()-t0)

            img = cv2.imread(os.path.join(inpath, f))
            height, width, _ = img.shape
            bbs = detector_output['detection_boxes']
            scores = detector_output['detection_scores']
            classes = detector_output['detection_classes']
            for i in range(len(bbs)):
                score = scores[i]
                if score < 0.25:
                    continue
                label = str(classes[i])
                bb = bbs[i]
                start_point = (int(bb[1]*width) , int(bb[2]*height))
                end_point = (int(bb[3]*width), int(bb[0]*height))
                cv2.rectangle(img, start_point, end_point, (0,255,0), 2)
                cv2.rectangle(img, start_point, (end_point[0], start_point[1]-20), (255,0,0), -1)
                cv2.putText(img, label, start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imwrite(os.path.join(outpath, f), img)

    print("total time took to process all the frame is:", tt)