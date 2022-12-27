# Nested parallel filters 2

def filter1_init(img_src,img_dst,imgfilter,glb_lock):
    global image_src1
    global image_dst1
    global image_filter1
    global global_lock1
    
    image_src1=img_src
    image_dst1=img_dst
    image_filter1=imgfilter
    global_lock1=glb_lock
    
    #if you whish to handle image_dst1 as NumPy matrix, you should have to create a new global NumPy Matrix, and assign
    #the image_dst1 shared array to the matrix buffer


def filter1(row):
    #here the shared image is stored in image_src1,so:
    row = image_src1[row,:,:]
    return #you wish to return something?


def filter2_init(img_src,img_dst,imgfilter,glb_lock):
    global image_src2
    global image_dst2
    global image_filter2
    global global_lock2
    
    image_src1=img_src
    image_dst1=img_dst
    image_filter2=imgfilter
    global_lock2=glb_lock
    #if you whish to handle image_dst1 as NumPy matrix, you should have to create a new global NumPy Matrix, and assign
    #the image_dst1 shared array to the matrix buffer


def filter2(row):
    #here the shared image is stored in image_src1,so:
    row = image_src2[row,:,:]
    return #you wish to return something?

