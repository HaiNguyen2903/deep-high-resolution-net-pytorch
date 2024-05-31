# Tutorial for Training, Testing and Inference

<details><summary><h3>Setup Conda Environment and buid neccesary libs</h3></summary>

```bash
conda create -n {env_name} python=3.6
pip install -r requirements.txt
```
```bash
cd lib
make
```
For more information, see the **Author's Quickstart README section**
</details>

<details><summary><h3>Create data for Training and Inference</h3></summary>
The easiest way to add a custom dataset is to format it to COCO format, which should has the following format:

```bash
root
  |
  |__detection_files.json (optional)
  |
  |__annotations
  |     |__{prefix}_train.json
  |     |__{prefix}_val.json
  |
  |__images
        |__train
        |    |__000000.jpg
        |    |__000001.jpg
        |    |__...
        |__val
             |__000000.jpg
             |__000001.jpg
             |__...
```

Where the annotation files contain some neccessary information:

```bash
{
    "categories": [
        {
            "supercategory": "person",
            "id": 1,
            "name": "person",
            "keypoints": ["nose", "head", ...], # list name (label) of 2D keypoint
            "skeleton": [[16,14], [14,12], ...], # list of keypoints pair that link together (e.x: keypoint 16 links with keypoints 14, ...)
            "images": [
              {
                "has_no_densepose": true,   # obj has dense pose or not
                "is_labeled": true,         # obj is label or not
                "file_name": "000000.jpg",  # file name
                "nframes": 900,             # number of frame in video
                "frame_id": 0,              # frame id
                "id": 0,                    # image id 
                "width": 608,               # image width
                "height": 1080              # image height
              },
              ...
            ],
            "annotations": [
              {
                "keypoints": [x1, y1, 1, x2, y2, 1, ...], # list with length 3 x num_keypoints, where 1 or 0 stand for kpt is invisble or not
                "track_id": 1,                            # obj id in the video
                "image_id": 0,                            # iamge id, same as in the *image* attribute
                "bbox": [x, y, w, h],                     # bbox coord in (top, left, width, height) format
                "scores": [],                             # left blank list
                "id": 0,                                  # assign the same value as image_id
                "iscrowd": false,                         # is image crowd or not
                "num_keypoints": 17,                      # number of keypoints
                "area": float(area)                       # bbox area
              },
              ...
            ]
        }
    ],
```

The ```detection_file.json``` is used in case we want to use result of a detection model instead of bbox ground truths. It should has the following format:

```bash
[
  {
    "image_id": 0,
    "bbox": [x, y, w, h], # bbox coord where x y is the top left corner coord
    "score": 0.x,         # detection confidence score
    "category_id": 1      # category of the obj class 
  }, 
  ...
]
```
</details>

<details><summary><h3>Setup config file and dataset</h3></summary>

Define a config file for training and inference in ```experiments/coco/hrnet``` or any where you like. Copy the existed .yaml file and change some neccesary attribute:
```bash
DATASET:
  DATASET: # name of the dataset class (define in lib/dataset/)
  ROOT: # path to root of the dataset
  TEST_SET: # name of the test json file
  TRAIN_SET: # name of the train json file
  
MODEL:
  PRETRAINED: # path to pretrained weight (use for training)

TRAIN:
  BATCH_SIZE_PER_GPU: # training batch size
  END_EPOCH: # number of train epochs (BEGIN_EPOCH = 0 as default)
  
TEST:
  COCO_BBOX_FILE: # path to detection json file (in case using detection instead of bbox ground truth)
  USE_GT_BBOX: # whether to use the bbox ground truth or not
```
Create a dataset class in ```lib/dataset/custom_dataset.py```. The dataset class should be the same as the ```COCODataset``` class in ```lib/dataset/coco.py```. However, there are some functions need to be customized:
 
```bash
def _get_ann_file_keypoint(self):
  '''
  change suitable prefix and path to your annotation file (annotations/train.json and annotations/test.json)
  '''
```
Note that it can have error in the ```_load_coco_keypoint_annotation_kernal``` function, since it cannot determine image paths in the json file to use ```self.coco.getAnnIds``` API. 

Debug this API if neccessary.

</details>

<details><summary><h3>Train, Test and Inference</h3></summary>

Train script:
```bash
python tool/train.py --cfg {path to cfg yaml file}
```
For default, the model is evaluated and saved best after every epoch.

Test script:
```bash
python tool/test.py --cfg {path to cfg yaml file} TEST.MODEL_FILE {path to test model weight}
```

Inference script:
```bash
python demo/inference.py --cfg {path to cfg yaml file} TEST.MODEL_FILE {path to test model weight} --videoFile {path to video file}
```

</details>
