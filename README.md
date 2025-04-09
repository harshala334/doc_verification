 activate virtual environment
 pip install -r requirements.txt
 python extract_text.py
 python detect_aadhaar.py

export PYTHONPATH=$PYTHONPATH:/Users/apple/Downloads/doc_verification/models:/Users/apple/Downloads/doc_verification/models/research:/Users/apple/Downloads/doc_verification/models/research/slim


 # print("\n🔍 Step 1: Detecting Aadhaar visual features...")
    # output_img, _, _, _ = detect_features(img_path)
    # cv2.imshow("Detected Aadhaar Features", output_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    conda install -c conda-forge opencv
