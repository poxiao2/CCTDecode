# CCTDecode
 Detect and decode the CCT (Circular Coded Target).
The main function is listed as following:

1. Draw CCT images: DrawCCT.py

   which can draw CCT figures to .png format images. the function is CCT_table(12,2500), the args represent the bit number and image size (pixels).
![Image text](https://github.com/poxiao2/image-store/blob/master/cct14.png)
   
2. Decode CCT: CCTDecodeRelease.py

   which can decode CCT from the signal image, or you can use it to decode the CCT images in the same folder.
   the function is code_table,image=CCT_extract1(img,12,0.85), the args represent the input image, bit number and filter arg. and this function returns the code table and image whose CCT is marked.
![Image text](https://github.com/poxiao2/image-store/blob/master/cct6.jpg)
   
3. Decode CCT from video: DecodeCCTFromVideo.py

   which can decode CCT from video directly. The function is CallCamera():
![Image text](https://github.com/poxiao2/image-store/blob/master/20191219223602.png)
