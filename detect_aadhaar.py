import os
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util, visualization_utils as vis_util

# Load Model and Label Map
MODEL_DIR = "models/inference_graph"
LABEL_PATH = "label_map.pbtxt"

def load_model():
    PATH_TO_CKPT = os.path.join(MODEL_DIR, "frozen_inference_graph.pb")

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    return detection_graph

# Detect Aadhaar Features
def detect_features(img_path):
    detection_graph = load_model()
    category_index = label_map_util.create_category_index_from_labelmap(LABEL_PATH, use_display_name=True)

    with detection_graph.as_default():
        with tf.compat.v1.Session(graph=detection_graph) as sess:
            image = cv2.imread(img_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_expanded = np.expand_dims(image_rgb, axis=0)

            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_expanded})

            vis_util.visualize_boxes_and_labels_on_image_array(
                image,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=3,
                min_score_thresh=0.5)

            return image, boxes, scores, classes

# Run and visualize
if __name__ == "__main__":
    img_path = "data/sample_aadhaar.jpg"
    output_img, _, _, _ = detect_features(img_path)

    cv2.imshow("Detected Aadhaar Features", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

