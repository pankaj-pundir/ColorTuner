# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label 

from kivy.uix.textinput import TextInput 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.boxlayout import BoxLayout
import numpy as np 
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty

LOW_ ,UPPER_ = np.array([0,0,0]),np.array([180,255,255])

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        # self.lower_red = 
        # self.upper_red = np.array([255,255,180])
        Clock.schedule_interval(self.update, 1.0 / fps)


    def processing(self,frame):
        global LOW_,UPPER_

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOW_, UPPER_)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        return res

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, -1)
            buf1 = self.processing(buf1)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class start(BoxLayout):
    slider_val_hue = NumericProperty(0)
    slider_val_saturation = NumericProperty(0)
    slider_val_value = NumericProperty(0)


    slider_val_hue_upper = NumericProperty(180)
    slider_val_saturation_upper = NumericProperty(255)
    slider_val_value_upper = NumericProperty(255)

    def __init__(self, *args, **kwargs):
        super(start, self).__init__(*args, **kwargs)
        # self.hueV = NumericProperty(25)
        # self.saturationV = NumericProperty(25)
        self.label_hue = Label(text=str(self.slider_val_hue))
        self.label_saturation = Label(text=str(self.slider_val_saturation))
        self.label_value = Label(text=str(self.slider_val_value))


        self.label_hue_upper = Label(text=str(self.slider_val_hue_upper))
        self.label_saturation_upper = Label(text=str(self.slider_val_saturation_upper))
        self.label_value_upper = Label(text=str(self.slider_val_value_upper))
        
    def run(self,capture):
        b = BoxLayout(orientation='vertical')
        self.my_camera = KivyCamera(capture=capture, fps=60)

        #-----------------------
        b.add_widget(Label(size_hint = (1, 0.1),text="[b] COLOR TUNER",markup=True,color=(1,0,0,1)))
        #-----------------------

        im = BoxLayout(size_hint = (1,0.7))
        im.add_widget(self.my_camera)
        
        #------------------
        b.add_widget(im)
        #-----------------

        data = BoxLayout(orientation='horizontal',size_hint = (1,0.2))

        left = BoxLayout(orientation='vertical',size_hint = (0.5,1))
        left.add_widget(Label(size_hint = (1, 0.05),text="[b] Lower Limit",markup=True,color=(1,0,0,1)))
        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='Hue'))
        hue = Slider(min=0,max=180,value=0,step = 1)
        hue.fbind('value', self.on_slider_val_hue)
        self.label_hue =  Label(text=str(self.slider_val_hue))
        c.add_widget(hue)
        c.add_widget(self.label_hue)
        left.add_widget(c)


        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='Saturation'))
        saturation = Slider(min=0,max=255,value=0,step = 1)
        saturation.fbind('value', self.on_slider_val_saturation  )
        self.label_saturation =  Label(text=str(self.slider_val_saturation ))
        
        c.add_widget(saturation)
        c.add_widget(self.label_saturation)
        left.add_widget(c)


        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='value'))
        value = Slider(min=0,max=255,value=0,step = 1)
        value.fbind('value', self.on_slider_val_value)
        self.label_value =  Label(text=str(self.slider_val_value))
        
        c.add_widget(value)
        c.add_widget(self.label_value)
        left.add_widget(c)
        
        data.add_widget(left)

        # --------------------------------------------------- 




        right = BoxLayout(orientation='vertical',size_hint = (0.5,1))
        right.add_widget(Label(size_hint = (1, 0.05),text="[b] upper Limit",markup=True,color=(1,0,0,1)))
        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='Hue'))
        hue_upper = Slider(min=0,max=180,value=180,step = 1)
        hue_upper.fbind('value', self.on_slider_val_hue_upper)
        self.label_hue_upper =  Label(text=str(self.slider_val_hue_upper))
        c.add_widget(hue_upper)
        c.add_widget(self.label_hue_upper)

        right.add_widget(c)


        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='Saturation'))
        saturation_upper = Slider(min=0,max=255,value=255,step = 1)
        saturation_upper.fbind('value', self.on_slider_val_saturation_upper  )
        self.label_saturation_upper =  Label(text=str(self.slider_val_saturation_upper ))
        
        c.add_widget(saturation_upper)
        c.add_widget(self.label_saturation_upper)

        right.add_widget(c)


        c = BoxLayout(orientation='horizontal',size_hint = (1,0.1))
        c.add_widget(Label(text='value'))
        value_upper = Slider(min=0,max=255,value=255,step = 1)
        value_upper.fbind('value', self.on_slider_val_value_upper)
        self.label_value_upper =  Label(text=str(self.slider_val_value_upper))
        
        c.add_widget(value_upper)
        c.add_widget(self.label_value_upper)
        
        
        right.add_widget(c)
        
        data.add_widget(right)

        b.add_widget(data)
        return b


    def on_slider_val_hue(self, instance, val):
        self.label_hue.text = str(val)
        global LOW_ , UPPER_
        LOW_ = np.array([int(val),LOW_[1],LOW_[2]])

    def on_slider_val_saturation(self, instance, val):
        self.label_saturation.text = str(val)
        global LOW_ , UPPER_
        LOW_ = np.array([LOW_[0],int(val),LOW_[2]])

    def on_slider_val_value(self, instance, val):
        self.label_value.text = str(val)
        global LOW_ , UPPER_
        LOW_ = np.array([LOW_[0],LOW_[1],int(val)])

    def on_slider_val_hue_upper(self, instance, val):
        self.label_hue_upper.text = str(val)
        global UPPER_
        UPPER_ = np.array([int(val),UPPER_[1],UPPER_[2]])


    def on_slider_val_saturation_upper(self, instance, val):
        self.label_saturation_upper.text = str(val)
        global UPPER_
        UPPER_ = np.array([UPPER_[0],int(val),UPPER_[2]])

    def on_slider_val_value_upper(self, instance, val):
        self.label_value_upper.text = str(val)
        global UPPER_
        UPPER_ = np.array([UPPER_[0],UPPER_[1],int(val)])


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        # self.my_camera = KivyCamera(capture=self.capture, fps=30)
        s = start()
        return s.run(self.capture)


    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()