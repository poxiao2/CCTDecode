CCTDecode 
=============== 

 Detect and decode the CCT (Circular Coded Target). <br>

Requirements: 
---------------- 

<1> python 3.7 (I don't know whether other python version would work correctly, you can have a try.) <br>
<2> opencv-python <br>
<3> pillow <br>
<4> numpy <br>
<5> matplotlib <br>
<6> progress <br>
<7> ... (maybe others, you can follow the error infomation to 'pip install xxx' them.) <br>
 
The main function is listed as following:
-----------------------------------------

1. Draw CCT images: DrawCCT.py <br>
   usage: <br>
   ``` python
   <1> cd root_path <br>
   <2> python DrawCCT.py --bit_n=9 --size=400   <br>    
   ```
![Image text](https://github.com/poxiao2/image-store/blob/master/cct14.png)
   
2. Detect and decode CCT: CCTDecodeRelease.py <br>
   which can decode CCT from the signal image, or you can use it to decode the CCT images in the same folder. <br>
   usage: <br>  
   ``` python
   <1> cd root_path <br>   
   <2> python CCTDecodeRelease.py --filename=cct12_6.png <br>
                                  --bit_n=12 <br>                                       
                                  --threshold=0.7   #for single image <br>                                        
       python CCTDecodeRelease.py --bach=True <br>
                                  --bit_n=8 <br>                              
                                  --save_folder=./result/ <br>                                      
                                  --threshold=0.93   #for images in same folder <br>
     ```                                   
![Image text](https://github.com/poxiao2/image-store/blob/master/cct12.jpg)

(Actually, there are some args are default value which can be ignored if you follow my data construction. The whole args are listed as follows: <br>
   bach=False, # bach processing <br>
   bit_n=12,   # the bit number of CCT image <br>
   filename=None,  # image name <br>
   save_folder='./result/',  # the folder for saving the processed images <br>
   src_folder='./data/',  # the folder which contains the source images <br>
   threshold=0.8   # the threshold for CCT detecion, which is between 0 and 1. <br>
So, you can change this args as you whish. But remember to write it correctly.) <br>

3. Decode CCT from video: DecodeCCTFromVideo.py <br>
   usage: <br>
   ``` python
   <1> cd root_path <br>
   <2> python DetectCCTFromVideo.py --bit_n=12 --threshold=0.7 <br>      
   ```                                 
![Image text](https://github.com/poxiao2/image-store/blob/master/20191219223602.png)
