import os
import cv2

path = r"/home/wyc/0927/test_envir1/Bpredict/"
filelist = os.listdir(path)
filelist.sort()
fps = 10

size = (640, 480)
video = cv2.VideoWriter("/home/wyc/0927/test_envir1/base_pre.avi",
                        cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
# video = cv2.VideoWriter("/home/wyc/0927/envir_1/envir_1/04_1216.avi",
#                         cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
#1632716206.660048
#1632716208732028.png
for item in filelist:
    picname = path + item
    img = cv2.imread(picname)
    # ptest = item[:-10] + "."+item[10:13]
    # cv2.putText(img, ptest, org=(20, 50), fontFace=cv2.FONT_HERSHEY_DUPLEX,
    #             fontScale=2.0,color=(0,0,255))
    video.write(img)

video.release()
cv2.destroyAllWindows()