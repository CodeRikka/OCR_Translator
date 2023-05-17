## OCR_Translator

### Introduction

This project uses [EasyOCR](https://github.com/JaidedAI/EasyOCR), [Page-Dewarp](https://github.com/lmmx/page-dewarp), and Baidu Translator for implementation, aiming to learn the encapsulation and deployment of APIs on servers

### Installation

#### Installing on the host machine
Step1. Install OCR_Translator
```
git clone https://github.com/CodeRikka/OCR_Translator.git
cd OCR_Translator
pip install -r requirements.txt
```
Step2. Verify Page-Dewarp
```
page-dewarp -x 0 -y 0 pics/example6.jpg
```
Step3. GPU acceleration

If you wish to use GPU acceleration, please install the GPU version of torch and related packages. Check the [Pytorch official website](https://pytorch.org/) for tutorials.
```
pip uninstall torch torchvision torchaudio
# Modify the cuda version to your own version
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```
### Run locally

#### Usage
```
usage: python export.py [-r0 ROOT_0] [-r1 ROOT_1] [-o OUTPUT_PATH]
                        [-tl THRESH_LINE] [-tb THRESH_BOX]
                        [-e EXTRA_SIZE] [-f FONT_SIZE]
                        [--uid UID] [--bkey BKEY]
                        [-g GPU{True, False}] [-rs RESIZE{True, False}]
                        [-d DEWARP{True, False}]
positional arguments: [-r0 ROOT_0] [-r1 ROOT_1] [-o OUTPUT_PATH]
use Page-Dewarp: python export.py [arguments] -d True
```

### Enable Server

#### 1. Enable single threading on the local server
```
python main.py
```
#### 2. Enable multithreading on the local server
```
python multi_main.py
```

### Apply

make sure you are using the correct port

#### 1. Send a request to the server using code
```
python POST.py
```

#### 2. Send a request to the server using cmd
```
curl -X POST https://example.com:25000/export -d root0=your/path/to/root0 -d root1=your/path/to/root1 ...
```