from flask import Flask,url_for,request,Response
import numpy as np
import cv2
from PIL import Image
app=Flask(__name__)

@app.route('/')
def start():
    return "hello world!"
@app.route('/upload',methods=['GET','POST'])
def upload():
    origin=request.files['origin']
    origin=Image.open(origin)

    #origin.save("tmp.png")
    template=request.files['template']
    template = Image.open(template)
    origin=cv2.cvtColor(np.asarray(origin),cv2.COLOR_RGB2BGR)
   # origin=np.asarray(origin)
    template = cv2.cvtColor(np.asarray(template), cv2.COLOR_RGB2BGR)

    print(template.shape)
    method=int(request.form['method'])
    methods=[cv2.TM_SQDIFF_NORMED,cv2.TM_CCORR_NORMED,cv2.TM_CCOEFF_NORMED]
    th,tw=template.shape[:2]
    result=cv2.matchTemplate(origin,template,methods[method])
    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(result)
    if method==0:
        tl=min_loc
    else:
        tl=max_loc
    br=(tl[0]+tw,tl[1]+th)
    print(tl)
    print(br)
    cv2.rectangle(origin,tl,br,(0,0,255),2)
    cv2.imwrite("./template.png",template)
    cv2.imwrite("./origin.png",origin)

    return str(tl[0])+"|"+str(tl[1])+"|"+str(br[0])+"|"+str(br[1])

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)