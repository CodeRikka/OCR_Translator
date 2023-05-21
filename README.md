## OCR_Translator

### UPDATE
```
2023.5.19 11:19     added spellchecker (pyenchant methods)
2023.5.21 18:56     added llama_spellcheck ([vanilla-llama](https://github.com/galatolofederico/vanilla-llama))
```
### Introduction

This project uses [EasyOCR](https://github.com/JaidedAI/EasyOCR), [Page-Dewarp](https://github.com/lmmx/page-dewarp), [Vanilla-llama](https://github.com/galatolofederico/vanilla-llama) and Baidu Translator for implementation, aiming to learn the encapsulation and deployment of APIs on servers

#### Examples

![examples.png](https://s2.loli.net/2023/05/19/9ohKxbZRy2d8icf.png)

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
Step4. Download Golang related packages
```
go get github.com/gin-gonic/gin
```
Step5. Modify the `filePath` and `outputPath` in the `main.go` to an absolute address(optional)


#### Install Vanilla-llama (Optional)

See [Vanilla-llama](https://github.com/galatolofederico/vanilla-llama) for tutorial


### Run locally

#### Usage
```
usage: python export.py [-r0 ROOT_0] [-r1 ROOT_1] [-o OUTPUT_PATH]
                        [-tl THRESH_LINE] [-tb THRESH_BOX]
                        [-e EXTRA_SIZE] [-f FONT_SIZE]
                        [--uid UID] [--bkey BKEY]
                        [-g GPU{True, False}] [-rs RESIZE{True, False}]
                        [-d DEWARP{True, False}]
                        [-m MODEL{0,1,2}] # updated on 23.05.18

positional arguments: [-r0 ROOT_0] [-r1 ROOT_1] [-o OUTPUT_PATH]

use Page-Dewarp: python export.py [arguments] -d True

select ML model: [-m MODEL{0,1,2}] # using ML methods
                 0: Default
                 1: KMeans
                 2: AgglomerativeClustering
                 **These methods are still being tested**
                 **See export.py for further information**
```

### Enable Server

#### 1. Enable single threading on the local server
```
python single_thread.py
```
#### 2. Enable multithreading on the local server
```
python multi_thread.py
```

### Apply

make sure you are using the correct port

#### 1. Send a request to the server using code
```
python posts/py_POST.py
```

#### 2. Send a request to the server using cmd
```
curl -X POST https://example.com:25000/export -d root0=your/path/to/root0 -d root1=your/path/to/root1 ...
```