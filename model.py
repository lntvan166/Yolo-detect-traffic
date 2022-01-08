import torch
import sys
sys.path.append('yolov5')
import cv2
import numpy as np
from PIL import Image


from models.common import *
from models.experimental import *
from utils.autoanchor import check_anchor_order
from utils.general import LOGGER, check_version, check_yaml, make_divisible, print_args
from utils.plots import feature_visualization
from utils.torch_utils import fuse_conv_and_bn, initialize_weights, model_info, scale_img, select_device, time_sync

def _create(name, pretrained=True, channels=3, classes=80, autoshape=True, verbose=True, device=None):
    """Creates a specified YOLOv5 model

    Arguments:
        name (str): name of model, i.e. 'yolov5s'
        pretrained (bool): load pretrained weights into the model
        channels (int): number of input channels
        classes (int): number of model classes
        autoshape (bool): apply YOLOv5 .autoshape() wrapper to model
        verbose (bool): print all information to screen
        device (str, torch.device, None): device to use for model parameters

    Returns:
        YOLOv5 pytorch model
    """
    from pathlib import Path
    from pathlib import Path

    from models.common import AutoShape, DetectMultiBackend
    from models.yolo import Model
    from utils.downloads import attempt_download
    from utils.general import check_requirements, intersect_dicts, set_logging
    from utils.torch_utils import select_device


    check_requirements(exclude=('tensorboard', 'thop', 'opencv-python'))
    set_logging(verbose=verbose)

    name = Path(name)
    path = name.with_suffix('.pt') if name.suffix == '' else name  # checkpoint path
    try:
        device = select_device(('0' if torch.cuda.is_available() else 'cpu') if device is None else device)

        if pretrained and channels == 3 and classes == 80:
            model = DetectMultiBackend(path, device=device)  # download/load FP32 model
            # model = models.experimental.attempt_load(path, map_location=device)  # download/load FP32 model
        else:
            cfg = list((Path(__file__).parent / 'models').rglob(f'{path.stem}.yaml'))[0]  # model.yaml path
            model = Model(cfg, channels, classes)  # create model
            if pretrained:
                ckpt = torch.load(attempt_load(path), map_location=device)  # load
                csd = ckpt['model'].float().state_dict()  # checkpoint state_dict as FP32
                csd = intersect_dicts(csd, model.state_dict(), exclude=['anchors'])  # intersect
                model.load_state_dict(csd, strict=False)  # load
                if len(ckpt['model'].names) == classes:
                    model.names = ckpt['model'].names  # set class names attribute
        if autoshape:
            model = AutoShape(model)  # for file/URI/PIL/cv2/np inputs and NMS
        return model.to(device)

    except Exception as e:
        help_url = 'https://github.com/ultralytics/yolov5/issues/36'
        s = 'Cache may be out of date, try `force_reload=True`. See %s for help.' % help_url
        raise Exception(s) from e

# class Model(torch.nn.Module):
#     def __init__(self, cfg='yolov5s.yaml', ch=3, nc=None, anchors=None):  # model, input channels, number of classes
#         super().__init__()
#         if isinstance(cfg, dict):
#             self.yaml = cfg  # model dict
#         else:  # is *.yaml
#             import yaml  # for torch hub
#             self.yaml_file = Path(cfg).name
#             with open(cfg, encoding='ascii', errors='ignore') as f:
#                 self.yaml = yaml.safe_load(f)  # model dict

#         # Define model
#         ch = self.yaml['ch'] = self.yaml.get('ch', ch)  # input channels
#         if nc and nc != self.yaml['nc']:
#             # LOGGER.info(f"Overriding model.yaml nc={self.yaml['nc']} with nc={nc}")
#             self.yaml['nc'] = nc  # override yaml value
#         if anchors:
#             # LOGGER.info(f'Overriding model.yaml anchors with anchors={anchors}')
#             self.yaml['anchors'] = round(anchors)  # override yaml value
#         self.model, self.save = parse_model(deepcopy(self.yaml), ch=[ch])  # model, savelist
#         self.names = [str(i) for i in range(self.yaml['nc'])]  # default names
#         self.inplace = self.yaml.get('inplace', True)

#         # Build strides, anchors
#         m = self.model[-1]  # Detect()
#         if isinstance(m, Detect):
#             s = 256  # 2x min stride
#             m.inplace = self.inplace
#             m.stride = torch.tensor([s / x.shape[-2] for x in self.forward(torch.zeros(1, ch, s, s))])  # forward
#             m.anchors /= m.stride.view(-1, 1, 1)
#             check_anchor_order(m)
#             self.stride = m.stride
#             self._initialize_biases()  # only run once

#         # Init weights, biases
#         initialize_weights(self)
#         self.info()
#         # LOGGER.info('')

#     def forward(self, x, augment=False, profile=False, visualize=False):
#         if augment:
#             return self._forward_augment(x)  # augmented inference, None
#         return self._forward_once(x, profile, visualize)  # single-scale inference, train

import socket
import time
import threading


def checkPortIsOpen(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    isOpen = False

    if result_of_check == 0:
        isOpen = True
    else:
        isOpen = False

    a_socket.close()

    return isOpen


def interruptListen(s):
    while True:
        print('check port 3000')
        time.sleep(10)
        if checkPortIsOpen(3000):
            continue
        else:
            print('app not work')
            s.close()
            break

def predict():
    imgs = ['image.png']  # numpy

    results = model(imgs, size=640)  # batched inference
    results.print()
    results.save(save_dir='app/public/result')


def runServer(s):
    try:
        while True:
            print('listen')
            conn, addr = s.accept()
            if conn:
                print('Connected by', addr)
                data = conn.recv(1024).decode()
                print('received {!r}'.format(data))
                if not data:
                    break
                if data == 'Close':
                    print('end')
                    break
                predict()

                reply = 'Success'
                conn.send(reply.encode())


    finally:
        s.close()


if __name__ == '__main__':
    model = _create(name='best.pt', pretrained=True, channels=3, classes=80, autoshape=True, verbose=True)  # pretrained

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 1234  # Port to listen on (non-privileged ports are > 1023)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s:
        s.bind((HOST, PORT))
        s.listen()
        threadCheckPort = threading.Thread(target=interruptListen, args=(s,))
        threadServer = threading.Thread(target=runServer, args=(s,))
        threadCheckPort.start()
        threadServer.start()
    # model = custom(path='path/to/model.pt')  # custom

    # Verify inference
    # from pathlib import Path

    # import cv2
    # import numpy as np
    # from PIL import Image

    # imgs = ['yolov5/data/images/zidane.jpg',
    #         'traffic-sign.png',  # filename
    #         Path('yolov5/data/images/zidane.jpg'),  # Path
    #         'https://ultralytics.com/images/zidane.jpg',  # URI
    #         np.zeros((320, 640, 3))]  # numpy

    # results = model(imgs, size=320)  # batched inference
    # results.print()
    # results.save()
