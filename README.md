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
   ``` c
   <1> cd root_path 
   <2> python DrawCCT.py --bit_n=9 --size=400 --color=black      
   ```
![Image text](https://github.com/poxiao2/image-store/blob/master/CCT/cct12_1.png)
   
2. Detect and decode CCT: CCTDecodeRelease.py <br>
   which can decode CCT from the signal image, or you can use it to decode the CCT images in the same folder. <br>
   usage: <br>  
   ``` c
   <1> cd root_path    
   <2> python CCTDecodeRelease.py --filename=cct12_6.png 
                                  --bit_n=12                                        
                                  --threshold=0.7   // for single image   
                                  --color=black     // select the color of CCT mark (white over black / black over white)                                     
       python CCTDecodeRelease.py --batch=True 
                                  --bit_n=8                              
                                  --save_folder=./result/                                    
                                  --threshold=0.93  // for images in same folder
                                  --color=black 
     ```                                   
![Image text](https://github.com/poxiao2/image-store/blob/master/CCT/cct12.png)

Actually, there are some args are default value which can be ignored if you follow my data construction. The whole args are listed as follows: <br>
``` c
   batch=False,                // batch processing 
   bit_n=12,                   // the bit number of CCT image 
   filename=None,              // image name 
   save_folder='./result/',    // the folder for saving the processed images 
   src_folder='./data/',       // the folder which contains the source images 
   threshold=0.8               // the threshold for CCT detecion, which is between 0 and 1. 
   color=white                 // the color of CCT mark (white over black / black over white)
```
So, you can change these args as you whish. But remember to write it correctly and don't foget the '--' before each arg. <br>

3. Decode CCT from video: DecodeCCTFromVideo.py <br>
   usage: <br>
   ``` c
   <1> cd root_path 
   <2> python DetectCCTFromVideo.py --bit_n=12 --threshold=0.7 --color=white
   ```                                 
![Image text](https://github.com/poxiao2/image-store/blob/master/CCT/CCT.gif)
