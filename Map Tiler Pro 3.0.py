# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 22:01:53 2016

@author: sandeep
"""
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

#import tkFileDialog

from urllib.request import Request, urlopen, build_opener
from urllib.error import URLError, HTTPError


import time
#import poly2 as kkk
import os
import threading
from threading import Thread
import HoverInfo as k1
root=Tk()
I_ovwrt=0
b=[66,6,102,42]
zoom=25
zmin=0
zmax=4
pad=0
url=""
layers=[]
out_dir=""
running="" #switch to start the exection
b_str=""
tiles_ok=0
running=1
high_interrupt=1 # works reverse
excep_intrpt=1


    
def Tile_fetcher(bbox_val,i_add):
    global url
    global tiles_ok
    global excep_intrpt
    fetch_url=url+bbox_val
    #print(fetch_url)
    a=build_opener()
    try:
        response=a.open(fetch_url)
    except URLError:
        excep_intrpt=0
    except:
        excep_intrpt=0
    try:
        img_data=response.read()
    except:
        img_data='........'
     
    if((ord(img_data[0])==0xff) or (ord(img_data[0])==0x89)): # I'm saving the tiles whose first character is 0xFF and skipping all other tiles
        tiles_ok=tiles_ok+1
        #print(tiles_ok)
        try:
            with open(i_add,'wb') as output:
                output.write(img_data)
        except:
            pass

        
            
def Tile_fetch_controller():
    def callback2():
        global running
        global zmin
        global zmax
        global pad
        global url
        global layers
        global out_dir
        global excep_intrpt
        tcur=0
        #zmax=zmax+3
        fb=open("bboxfile.bhu1","r")
        bb=fb.readlines()
        fb.close()
        #print(zmax+2,zmin),
        th_count=0
        total_tiles=0
        pb_feed.delete('1.0',END)
        pb_feed.insert(END,">>The process of tile production has beeen started . . . .")
        for z in range(zmin+1,zmax+1):
            a=bb[z].split(',')
            a=[float(k) for k in a[:-1]]
            #print(a),
            zv=(180.0)/(2**(z-1))
            #print(zv),
            dx=a[2]-a[0]
            dy=a[3]-a[1]
            pa=[0,0,0,0]
            pa[0]=a[0]-(pad*zv)
            pa[1]=a[1]-(pad*zv)
            pa[2]=a[2]+(pad*zv)
            pa[3]=a[3]+(pad*zv)
            #print(pa),
            Tnum_x=int((pa[0]+180)/zv)                              
            Tnum_y=int((pa[1]+90)/zv)
            #print("Tnum_x,Tnum_y=",Tnum_x,Tnum_y),
            xdiv=int(dx/zv)+2*pad
            ydiv=int(dy/zv)+2*pad
            #print("Number of Tiles in zoom level %d = %d" %(z-1,xdiv*ydiv))
            total_tiles+=xdiv*ydiv
        #print("Total tiles =",total_tiles)
        for z in range(zmin+1,zmax+1):
            if(running and excep_intrpt):
                a=bb[z].split(',')
                a=[float(k) for k in a[:-1]]
                #print(a),
                zv=(180.0)/(2**(z-1))
                #print(zv),
                dx=a[2]-a[0]
                dy=a[3]-a[1]
                pa=[0,0,0,0]
                pa[0]=a[0]-(pad*zv)
                pa[1]=a[1]-(pad*zv)
                pa[2]=a[2]+(pad*zv)
                pa[3]=a[3]+(pad*zv)
                #print(pa),
                Tnum_x=int((pa[0]+180)/zv)                              
                Tnum_y=int((pa[1]+90)/zv)
                #print("Tnum_x,Tnum_y=",Tnum_x,Tnum_y),
                xdiv=int(dx/zv)+2*pad
                ydiv=int(dy/zv)+2*pad
                #print("Number of Tiles in zoom level %d = %d" %(z-1,xdiv*ydiv))
                #total_tiles+=xdiv*ydiv
                #--------------- copied from bboxer
                
                st=time.time()
                for x in range(xdiv):
                    xmin=pa[0]+(zv*x)
                    Tnum_tmp_y=Tnum_y
                    for y in range(ydiv):
                        if(running):
                            ymin=pa[1]+(zv*y)
                            xmax=xmin+zv
                            ymax=ymin+zv
                            #print(Tnum_x,Tnum_tmp_y)
                            bbox=("%f,%f,%f,%f" % (xmin,ymin,xmax,ymax))
                            add=("%s/%.2d/" % (out_dir,z-1)) #changed i to z
                            if (Tnum_x<0):
                                x_p=Tnum_x+1000
                                x_pth=("-01/999/%d/" % (x_p))
                            else:
                                x_p=Tnum_x
                                x_pth=("000/000/%.3d/" % (x_p))
                            if (Tnum_tmp_y<0):
                                y_p=Tnum_tmp_y+1000
                                y_pth=("-01/999")
                            else:
                                y_p=Tnum_tmp_y
                                y_pth=("000/000")
                                
                            fol_add=add+x_pth+y_pth
                            if(Tnum_tmp_y<0):
                                img_ext=("/%d.jpeg" % y_p)
                            else:
                                img_ext=("/%.3d.jpeg" % y_p)
                                                            
                            img_add=add+x_pth+y_pth+img_ext
                            #print(img_add)
                            Tnum_tmp_y+=1
                            tcur=tcur+1
                            if not os.path.exists(fol_add):
                                os.makedirs(fol_add)
                            if not I_ovwrt:    
                                if os.path.exists(img_add):
                                    continue
                                
                            t=Thread(target=Tile_fetcher,args=(bbox,img_add))
                            
                            th_count=th_count+1
                            try:
                                t.start()
                            except:
                                #print("working......"),
                                #print(th_count)
                                time.sleep(5)
                                pb["value"]=(1.*tcur/total_tiles)*100-2
                        else:
                            try:
                                time.sleep(2)
                                t.join()
                            except:
                                pass
                            
                            break
                    if(running and excep_intrpt):
                        Tnum_x=Tnum_x+1
                    else:
                        break
                if(running and excep_intrpt):
                    pb["value"]=(1.*tcur/total_tiles)*100-2
                    pb.update()
                else:
                    break
        if(running and excep_intrpt):
            try:
                t.join()
            except:
                pass
                #print("All the tiles exists in the directory")

            
            global tiles_ok    
           
            if(th_count-tiles_ok==0):
                pb_feed.delete('1.0',END)
                pb_feed.insert(END,">> The task has been completed sucessfully !")
                B_strt.configure(state='disabled',bg='gray')
                B_stop.configure(state='disabled',bg='gray')
                B_validate.configure(state='normal',bg='#269900')
                
            else:
                time.sleep(1)
                msg=("The server hasn't served few tiles. Click on 'Start' to re-request.")
                pb_feed.delete('1.0',END)
                pb_feed.insert(END,msg)
                B_strt.configure(state='normal',bg='#269900')
                B_stop.configure(state='disabled',bg='gray')
                B_validate.configure(state='normal',bg='#269900')
            pb["value"]=100
            tiles_ok=0
            th_count=0
            
        else:
            time.sleep(2)
            B_strt.configure(state='normal',bg='#269900')
            B_validate.configure(state='normal',bg='#269900')
            B_stop.configure(state='disabled',bg='gray')
        if(not excep_intrpt):
            if(running):
                #print("Exception")
                start()
            else:
                stop()

    j=Thread(target=callback2)
    j.start()

def bbox_producer():
    global b
    global zoom
    global B
    #b=[66,6,102,42]
    #B=[-180,-90,180,90] #standard values, don't change
    #B=[0,-90,180,90] 
    res=0 # temporary variable to store values
    bounds=[]
    for j in range(2):
        n_plus=B[j]
        bounds.append(n_plus)
        Bx=360.0
        for i in range(zoom):
            Bx=float(Bx/2)
            res=Bx+n_plus   
            while(res<=b[j]):
                res=res+Bx
            n_plus=(res-Bx)
            bounds.append(n_plus)
    for j in range(2,4):
        n_plus=B[j]
        bounds.append(n_plus)
        Bx=360.0
        for i in range(zoom):
            Bx=Bx/2
            res=n_plus-Bx   
            while(res>=b[j]):
                res=res-Bx
            n_plus=(res+Bx)
            bounds.append(n_plus)
    f=open("bboxfile.bhu1","w")
    for j in range(zoom+1):
        c=j
        for i in range(4):
            f.write(str(bounds[c]))
            f.write(",")
            #print(bounds[c]),
            c=c+zoom+1
        #print("")
        f.write("\n")
    f.close()
    bounds=[]
    Tile_fetch_controller()


def fopen():
    out=filedialog.askdirectory()
    dirname=str(out)
    O_file.delete('1.0',END)
    O_file.insert(END,dirname)

def start():
    global tiles_ok
    global running
    global excep_intrpt
    running=1
    excep_intrpt=1
    time.sleep(0.03)
    tiles_ok=0
    B_stop.configure(state='normal',bg='#269900')
    B_validate.configure(state='disabled',bg='gray')
    B_strt.configure(state='disabled',bg='gray')
    tstrt=Thread(target=bbox_producer)
    tstrt.start()
    tstrt.join()
    
def intrpt_handler():
    global high_interrupt
    if (high_interrupt):
        time.sleep(5)
        start()
    
def interrupt():
    global running
    running=0
    #print(">> Interruption <<")
    pb_feed.delete('1.0',END)
    pb_feed.insert(END,">>Internet Connection Lost. Trying to reconnect in 5 seconds....")
    tint=Thread(target=intrpt_handler)
    tint.start()
    
def stop():
    global high_interrupt
    global running
    running=0
    high_interrupt=0
    #print(">> stop signal received")
    pb_feed.delete('1.0',END)
    pb_feed.insert(END,">>Tile production has been stopped")
    
    #B_validate.configure(state='normal',bg='#269900')
    #B_strt.configure(state='normal',bg='#269900')

def validate(): 
        pb["value"]=0
        pb.update()
        global b
        global zoom
        global pad
        global zmin
        global zmax
        global url
        global layers
        global out_dir
        global B
        global b_str
        B_validate.config(state='disabled')
        B_strt.config(state='disabled')
        B_stop.config(state='disabled')
        notification.delete('1.0',END)
        notification.destroy
        pb_feed.delete('1.0',END)
        pb_feed.insert(END,">> Please wait while we verify the given input fields . . . . . . . ")
        #d=O_file.get("1.0", "end-1c")
        url=str(I_url.get("1.0", "end-1c"))
        layers=str(I_lay.get("1.0", "end-1c"))
        out_dir=str(O_file.get("1.0", "end-1c"))
        b=str(I_bbox.get("1.0", "end-1c"))
        zm=str(I_zoom.get("1.0", "end-1c"))
        pad=int(I_pad.get("1.0", "end-1c"))
        err_msg=""
        B=str(I_B_bbox.get("1.0", "end-1c"))
        """
        
        """
        if((layers[-1] == ',') or (layers[-1] == ' ')):
            layers=layers[:-1]
        b_str=b
        b=b.split(',')
        try:
            b=[float(k) for k in b]
        except ValueError:
            I_bbox.delete('1.0','end')
            I_bbox.insert("1.0","66,6,102,42")
            err_msg="enter four floating/integer numbers for BBox of the AOI"
        if(len(b)!=4):
            err_msg="Enter four floating/integer numbers for BBox the AOI"
            
        B=B.split(',')
        try:
            B=[float(k) for k in B]
        except ValueError:
            I_B_bbox.delete('1.0','end')
            I_B_bbox.insert("1.0","-180,-90,180,90")
            err_msg="enter four floating/integer numbers for BBox of the Base"
        if(len(B)!=4):
            err_msg="Enter four floating/integer numbers for BBox of the Base"
        zm=zm.split(',')
        try:
            zm=[int(k) for k in zm]
            
        except ValueError:
            I_zoom.delete('1.0','end')
            I_zoom.insert('1.0',"0,5")
            err_msg="enter natural numbers only for Zoom Levels"
                
        zmin=zm[0]
        zmax=zm[1]
        zoom=zmax
        if (out_dir==""):
            err_msg="Specify the output location"
        else:
            if(not os.path.exists(out_dir)):
                err_msg="Specify the correct output location"
            
        if(err_msg==""):
            url_checker()
        else:
            pb_feed.delete('1.0',END)
            pb_feed.insert(END,err_msg)
            B_validate.config(state='normal')
            #print(url,layers,out_dir,b,zm,pad)
    
def url_checker(): 
  def subcall():
    def callback4(): 
        global b
        global zoom
        global pad
        global zmin
        global zmax
        global url
        global layers
        global out_dir
        global B
        global b_str
        pb_feed.delete('1.0',END)
        pb_feed.insert(END,">> Please wait while we verify the URL . . . . . . . . . . . . . . .")
        xmldata=None
        img_data=None
        err_msg=''
        notif_msg=''
        laylist=layers.split(',')

        if("?" in url):
            if(".map" in url):
                url=url+"&"
        else:
            url=url+"?"
        url_getc=url+"SERVICE=WMS&REQUEST=GETCAPABILITIES"



        try:
            xmldata=urlopen(url_getc)
        except URLError as err:
            err_msg= " >> " + str(err.reason) + " - open the below url in any browser to know more."
            notif_msg=url_getc
        if(xmldata is not None):
            xml=xmldata.read()
            for ll in laylist:
                if(ll in xml):
                    pass
                else:
                    err_msg="Invalid Layers - open the below url in any browser to know the valid layers"
                    notif_msg=url_getc
                    
        if(err_msg == ''):
            url=url+"LAYERS="+layers+"&STYLES=&SERVICE=WMS&WIDTH=256&FORMAT=image/jpeg&REQUEST=GetMap&HEIGHT=256&SRS=EPSG:4326&VERSION=1.1.1&BBOX="                   
            try:           
                img_data=urllib2.urlopen(url+b_str)
            except urllib2.URLError as err:
                err_msg= "There is an error. Open the below url in any browser for more details and try again"
                notif_msg=url+b_str
            if(img_data is not None):
                imgd=img_data.read()
                if((ord(imgd[0])==0xff) or (ord(imgd[0])==0x89)):
                    pass
                else:
                    err_msg="BBOX of AOI is not matching. Open below url in any browser for more details "
                    notif_msg=url+b_str
                
        if(err_msg == ''):
            B_validate.config(state='normal',bg='#269900')
            B_strt.configure(state='normal',bg='#269900')
            notification.config(bg="white",state='disabled')
            pb_feed.delete('1.0',END)
            pb_feed.insert(END,">>The inputs have been validated successfully. Click on Start button.")
        else:
            notification.configure(state='normal')
            notification.config(bg="#ff6666",fg="white")
            notification.delete('1.0',END)
            notification.insert(END,notif_msg)
            notification.configure(state='disabled')
            pb_feed.delete('1.0',END)
            pb_feed.insert(END,err_msg[0:95])
            B_validate.config(state='normal',bg='#269900')
        xml=''
        imgd=''

    thu=Thread(target=callback4)
    thu.start()
    thu.join()
 
  thu2=Thread(target=subcall)
  thu2.start()

  

frame=Frame(root)
root.resizable(0,0)
frame.pack()

root.title("Bhuvan Tiler Pro")
try:
    root.iconbitmap('bhuvan.ico')
except:
    pass

fz=open("repository.bhu1","rb")
a=fz.read()
f1=open("logo.gif","wb")
f1.write(a[:18094][::-1])
f1.close()
f2=open("fol_icon.gif","wb")
f2.write(a[1004:][::-1])
f2.close()


logo=PhotoImage(file="logo.gif")
txd=Label(frame,image=logo,borderwidth=8)
txd.grid(row=0,column=0)

L_url=Label(frame,text="WMS Link - ( Enter the URL of a WMS server)")
L_url.grid(row=1,column=0,sticky=NW)
I_url=Text(frame,width=70,height=2,borderwidth=5,padx=15)
I_url.insert(END,"http://example.com/bhuvan/india/wms/?")
I_url.grid(row=2,column=0,sticky=NW)

lay=Label(frame,text="Layers - ( Layer1, layer2, layer3, .  . n )") 
lay.grid(row=3,column=0,sticky=NW)
I_lay=Text(frame,width=70,height=3,borderwidth=5,padx=15,fg="black")
I_lay.insert(END,"Layer1,Layer2,...LayerN") 
I_lay.grid(row=4,column=0,sticky=NW)

bbox=Label(frame,text="BBOX of the AOI - (xmin,ymin,xmax,ymax)")
bbox.grid(row=5,column=0,sticky=W)
I_bbox=Text(frame,width=70,height=1,borderwidth=5,padx=15)
I_bbox.insert(END,"66,6,102,42") #66,6,102,42
I_bbox.grid(row=6,column=0,sticky=NW)

B_bbox=Label(frame,text="BBOX of the Base- (xmin,ymin,xmax,ymax)")
B_bbox.grid(row=7,column=0,sticky=W)
I_B_bbox=Text(frame,width=70,height=1,borderwidth=5,padx=15)
I_B_bbox.insert(END,"-180,-90,180,90")
I_B_bbox.grid(row=8,column=0,sticky=W)

out=Label(frame,text="Output Location")
out.grid(row=9,column=0,sticky=NW)
O_file=Text(frame,width=65,height=1,borderwidth=5,padx=15,pady=5)
O_file.grid(row=10,column=0,sticky=NW)

fol_img=PhotoImage(file="fol_icon.gif")
O_btn=Button(frame,image=fol_img,command=fopen)
#O_btn=Button(frame,padx=1,borderwidth=4,image=fol_img,fg="black",command=fopen,height=28,width=30)
O_btn.grid(row=10,column=0,sticky=NE)


frame1=Frame(root)
frame1.pack(side=TOP)

zoom=Label(frame1,text="          Zoom Levels-(from,to):")
zoom.pack(side=LEFT)

I_zoom=Text(frame1,width=10,height=1,borderwidth=5)
I_zoom.insert(END,"0,5")
I_zoom.pack(side=LEFT,expand=True,padx=20)

pd=Label(frame1,text="          Padding:    ")
pd.pack(side=LEFT)
I_pad=Text(frame1,width=10,height=1,borderwidth=5,fg="blue")
I_pad.insert(END,"0")
I_pad.pack(side=LEFT,padx=20)

frame5=Frame(root)
frame5.pack(side=TOP)
Line=Label(frame5, text="   ")
Line.grid(row=0,column=0,sticky=W)

frame3=Frame(root)
frame3.pack(side=TOP)
B_validate=Button(frame3,command=validate,text="Validate")
B_validate.grid(row=1,column=0,sticky=E)
B_strt=Button(frame3,command=start,text="Start",state='disabled') #command=start,
B_strt.grid(row=1,column=3,sticky=E)
B_stop=Button(frame3,text="Stop",state='disabled',command=stop)
B_stop.grid(row=1,column=5,sticky=E)


frame4=Frame(root)
frame4.pack(side=TOP)
pb_feed=Text(frame4,width=70,height=1,borderwidth=5,bg="#426b7d",fg='white')
pb_feed.grid(row=0,column=0)
pb_feed.insert(END,">>Enter the given inputs and click on validate to validate the inputs")


pb = Progressbar(frame4, orient="horizontal", length=470,mode="determinate")
pb.grid(row=1,column=0)

notification=Text(frame4,width=70,height=1,borderwidth=5)
notification.grid(row=3,column=0)

hhelp=Label(frame4,width=5,text="Tips",borderwidth=5)
hhelp.grid(row=1,column=0,sticky=E)
k1.HoverInfo(hhelp,"1. Double click on the text to select the whole text from an input field. \n2. Click on validate button after changing any of the input fields.\n3. 'Ctrl + C' to copy the text from an input fields")


#pb.start()

root.mainloop()
#root.withdraw()
