import subprocess

def process(image_path):
    cmd = ["page-dewarp","-x","0","-y","0",image_path]
    subprocess.run(cmd)
    
    import os
    image_name = os.path.basename(image_path)
    image_name_without_extension = os.path.splitext(image_name)[0]
    new_image_name = image_name_without_extension + '_thresh.png'
    return new_image_name