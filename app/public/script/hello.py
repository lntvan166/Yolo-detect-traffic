import os


path_model = 'public/yolov5/detect.py'
path_image = 'public/img/image.png'
path_result = 'public/yolov5/runs/detect/exp/image.png'

print(os.path.isfile(path_model))
print(os.path.isfile(path_image))