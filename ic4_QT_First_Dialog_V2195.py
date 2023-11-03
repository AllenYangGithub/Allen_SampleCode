import sys
from PyQt5.QtGui import QPixmap, QImage      
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5 import QtCore
import numpy as np
import cv2
import os
import time
import threading
import ic4 as ic4

class Listener(ic4.QueueSinkListener):

    def __init__(self,device_delivered,device_transmission_error,device_underrun,sink_delivered,sink_ignored,sink_underrun,grabber):

        #self.fdisplay = ic4.FloatingDisplay()  # fdisplay will creat another dialog to display
        self.device_delivered = device_delivered
        self.device_transmission_error= device_transmission_error
        self.device_underrun= device_underrun
        self.sink_delivered= sink_delivered
        self.sink_ignored= sink_ignored
        self.sink_underrun= sink_underrun
        self.grabber = grabber= grabber
        pass

    def sink_connected(self, sink: ic4.QueueSink, image_type: ic4.ImageType, min_buffers_required: int) -> bool:
        sink.alloc_and_queue_buffers(5)

        return True

    def sink_disconnected(self, sink: ic4.QueueSink):
        return

    def frames_queued(self, sink: ic4.QueueSink):
        try:
            f = sink.pop_output_buffer()
            image = QImage(f.pointer,f.image_type.width,f.image_type.height,QImage.Format_Grayscale8 )
            image.save("123.jpg")
            print("Device Number: "+str(f.meta_data.device_frame_number)+ "/ Driver NUmber: "+str(f.meta_data.device_frame_number))
            self.device_delivered.setText( str(self.grabber.stream_statistics.device_delivered))
            self.device_transmission_error.setText( str(self.grabber.stream_statistics.device_transmission_error))
            self.device_underrun.setText( str(self.grabber.stream_statistics.device_underrun))
            self.sink_delivered.setText( str(self.grabber.stream_statistics.sink_delivered))
            self.sink_ignored.setText( str(self.grabber.stream_statistics.sink_ignored))
            self.sink_underrun.setText( str(self.grabber.stream_statistics.sink_underrun))
            #self.fdisplay.display_buffer(f) # fdisplay will creat another dialog to display

        except ic4.IC4Exception:
                return
        return



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IC4 First Dialog By QT Display")
        self.setGeometry(100, 100, 800, 500)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # 左邊的 Label
        videowindow = QLabel("這是一個 640x480 的 Label")
        videowindow.setStyleSheet("background-color: darkblue;")
        videowindow.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout.addWidget(videowindow)

        # 右邊的按鈕區域
        button_widget = QWidget()
        layout.addWidget(button_widget)

        button_layout = QVBoxLayout(button_widget)
        button_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        self.btn_Device = QPushButton("Device")
        self.btn_Properties = QPushButton("Properties")
        self.btn_Live = QPushButton("Live Start")


        self.btn_Device.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_Properties.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_Live.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_device_delivered =  QLabel("Device Deliverd")
        self.device_delivered =  QLabel("0")
        self.device_delivered.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_device_transmission_error =  QLabel("Device Transmission erro")
        self.device_transmission_error =  QLabel("0")
        self.device_transmission_error.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_device_underrun =  QLabel("Device Underrun")
        self.device_underrun =  QLabel("0")
        self.device_underrun.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_sink_delivered =  QLabel("Sink Deliverd")
        self.sink_delivered =  QLabel("0")
        self.sink_delivered.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_sink_ignored =  QLabel("Sink ignored")
        self.sink_ignored =  QLabel("0")
        self.sink_ignored.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.TXT_sink_underrun =  QLabel("Sink underrun")
        self.sink_underrun =  QLabel("0")
        self.sink_underrun.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout.addWidget(self.btn_Device)
        button_layout.addWidget(self.btn_Properties)
        button_layout.addWidget(self.btn_Live)
        button_layout.addWidget(self.TXT_device_delivered)
        button_layout.addWidget(self.device_delivered)
        button_layout.addWidget(self.TXT_device_transmission_error)
        button_layout.addWidget(self.device_transmission_error)
        button_layout.addWidget(self.TXT_device_underrun)
        button_layout.addWidget(self.device_underrun)
        button_layout.addWidget(self.TXT_sink_delivered)
        button_layout.addWidget(self.sink_delivered)
        button_layout.addWidget(self.TXT_sink_ignored)
        button_layout.addWidget(self.sink_ignored)
        button_layout.addWidget(self.TXT_sink_underrun)
        button_layout.addWidget(self.sink_underrun)


        self.btn_Device.clicked.connect(self.on_Device_clicked)
        self.btn_Properties.clicked.connect(self.on_Properties_clicked)
        self.btn_Live.clicked.connect(self.on_Live_clicked)

        self.grabber = ic4.Grabber()
        self.edisplay = ic4.EmbeddedDisplay(videowindow.winId())
        self.edisplay.set_render_position(ic4.DisplayRenderPosition.STRETCH_CENTER)

    def Line1RisingEdgeNotifcation(self,property : ic4.Property)->None :
        self.Event_Line1_Rising_Edge_Timestamp.setText( str(self.eventLine1RisingEdgeTimestamp.value))
        print("Rising Edge")
        return None
    
    def Line1FallingEdgeNotifcation(self,property : ic4.Property)->None :
        self.Event_Line1_Falling_Edge_Timestamp.setText( str(self.eventLine1FallingEdgeTimestamp.value))    
        print("Falling Edge")
        return None

    def on_Device_clicked(self):
        # for di in.devices():
        #     if di.model_name == "DFK 33GX183":
        #         grabber.device_open(di)
        #         break
        #grabber.device_property_map.set_value(ic4.PropId.PIXEL_FORMAT,ic4.PixelFormat.BayerRG8)

        ic4.Dialogs.grabber_select_device(self.grabber,1)
        self.listen = Listener(self.device_delivered,
                               self.device_transmission_error,
                               self.device_underrun,
                               self.sink_delivered,
                               self.sink_ignored,
                               self.sink_underrun,
                               self.grabber)
        
        self.sink = ic4.QueueSink(self.listen)

 
    def on_Properties_clicked(self):
        ic4.Dialogs.grabber_device_properties(self.grabber,1)

    def on_Live_clicked(self):


        if  self.grabber.is_acquisition_active:    
            self.grabber.stream_stop()
            self.btn_Live.setText("Live Start")
        else:
            
            self.btn_Live.setText("Live Stop")
            self.grabber.stream_setup(self.sink,self.edisplay)

if __name__ == "__main__":
    ic4.Library.init()
    
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
