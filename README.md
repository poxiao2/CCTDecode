# CCTDecode
 Detect and decode the CCT (Circular Coded Target).

# Requirements:

<1> python 3.7 (I don't know whether other python version would work correctly, you can have a try.)

<2> opencv-python

<3> pillow

<4> numpy

<5> matplotlib

<6> progress

<7> ... (maybe others, you can follow the error infomation to 'pip install xxx' them.)
 
# The main function is listed as following:

1. Draw CCT images: DrawCCT.py

   usage: <1> cd root_path
   
          <2> python DrawCCT.py --bit_n=9 
          
                                --size=400   
                                
![Image text](https://github.com/poxiao2/image-store/blob/master/cct14.png)
   
2. Detect and decode CCT: CCTDecodeRelease.py

   which can decode CCT from the signal image, or you can use it to decode the CCT images in the same folder.
   
   usage: <1> cd root_path
   
          <2>python CCTDecodeRelease.py --filename=cct12_6.png 
          
                                        --bit_n=12 
                                        
                                        --threshold=0.7   #for single image
                                        
             python CCTDecodeRelease.py --bach=True 
             
                                        --bit_n=8 
                                        
                                        --save_folder=./result/ 
                                        
                                        --threshold=0.93   #for images in same folder
                                        
![Image text](https://github.com/poxiao2/image-store/blob/master/cct12.jpg)

(Actually, there are some args are default value which can be ignored if you follow my data construction. The whole args are listed as follows:

   bach=False, # bach processing
   
   bit_n=12,   # the bit number of CCT image
   
   filename=None,  # image name
   
   save_folder='./result/',  # the folder for saving the processed images
   
   src_folder='./data/',  # the folder which contains the source images
   
   threshold=0.8   # the threshold for CCT detecion, which is between 0 and 1.
   
So, you can change this args as you whish. But remember to write it correctly.)

3. Decode CCT from video: DecodeCCTFromVideo.py

   usage: <1>cd root_path
   
          <2>python DetectCCTFromVideo.py --bit_n=12 
          
                                          --threshold=0.7      
                                          
![Image text](https://github.com/poxiao2/image-store/blob/master/20191219223602.png)
