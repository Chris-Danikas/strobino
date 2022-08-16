from tracemalloc import start
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import time
import numpy as np
import mic


if __name__ == '__main__':

    app = pg.mkQApp("Visualizer")
    mw = QtWidgets.QMainWindow()
    win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
    win.resize(1200,800)
    win.setWindowTitle('danikas_studios ***Visualizer***')
    pg.setConfigOptions(antialias=True)

    # mic input plot
    mic_pl = win.addPlot(title="Microphone input")
    mic_curve = mic_pl.plot(pen='w')

    ''' den jerw ti einai auto
    def update():
        global mic_curve, mic_data
        mic_curve.setData()
    timer = QtCore.QTimer()
    #timer.timeout.connect(update)
    timer.start(50)
    '''
    x = np.linspace(0, 100, num=2048)
    mic_pl.setYRange(-6000, 6000, padding=0)
    mic_curve.setData(x, mic.stream(True))
    win.nextRow()


    # frequency domain plot
    spec = win.addPlot(title = "Spectrum analyzer")
    spec_curve = spec.plot(pen='r')
    spec_curve.setData([1,2,3,4], [1,2,3,4])
    win.nextRow()

    # Out signal
    spec = win.addPlot(title = "Spectrum analyzer")
    spec_curve = spec.plot(pen='b')
    spec_curve.setData([1,2,3,4], [0.5,1,1.5,2])
    win.nextRow()

    def doSth(x):
        print('hello')
        hell_but.setText('hell', color='r')

    hell_but = pg.LabelItem('Hello')
    hell_but.mousePressEvent = doSth
    win.addItem(hell_but)

    


    #delete later
    pg.exec()