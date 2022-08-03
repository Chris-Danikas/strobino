from asyncore import write
import PySimpleGUI as sg
import pyaudio
import numpy as np
# TO-DOOOOOO:
# apla vazw to chunk 1024
# vgazw olo to visualization
# grafw ton algorithmo gia na vriskei ta bpms
# diavazw perissotera gia to pyaudio k ta fft
from arduino import write_read
from arduino import beat
import threading 

def create_thread():
	return threading.Thread(target=beat, args=('5',))


""" RealTime Audio Basic FFT plot """
# VARS CONSTS:
_VARS = {'window': False,
         'stream': False,
         'audioData': np.array([])}

# pysimpleGUI INIT:
AppFont = 'Any 16'
sg.theme('Black')
CanvasSizeWH = 500

layout = [[sg.Graph(canvas_size=(CanvasSizeWH, CanvasSizeWH),
                    graph_bottom_left=(-16, -16),
                    graph_top_right=(116, 116),
                    background_color='#B9B9B9',
                    key='graph')],
          [sg.ProgressBar(4000, orientation='h',
                          size=(20, 20), key='-PROG-')],
          [sg.Button('Listen', font=AppFont),
           sg.Button('Stop', font=AppFont, disabled=True),
           sg.Button('Exit', font=AppFont)]]
_VARS['window'] = sg.Window('Mic to basic fft plot + Max Level',
                            layout, finalize=True)

graph = _VARS['window']['graph']

# INIT vars:
CHUNK = 128  # Samples: 1024,  512, 256, 128
RATE = 2000  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen
TIMEOUT = 10  # In ms for the event loop
GAIN = 10
pAud = pyaudio.PyAudio()

beaf1 = 0

# FUNCTIONS:


def drawAxis():
    graph.DrawLine((0, 50), (100, 50))  # x Axis
    graph.DrawLine((0, 0), (0, 100))  # y Axis

    graph.DrawLine((0, 0), (100, 0))


def drawTicks():

    divisionsX = 10
    multi = int(RATE/divisionsX)
    offsetX = int(100/divisionsX)

    divisionsY = 10
    offsetY = int(100/divisionsY)

    for x in range(0, divisionsX+1):
        # print('x:', x)
        graph.DrawLine((x*offsetX, -3), (x*offsetX, 3))
        graph.DrawText(x*multi/1000, (x*offsetX, -10), color='black')

    for y in range(0, divisionsY+1):
        graph.DrawLine((-3, y*offsetY), (3, y*offsetY))


def drawAxesLabels():
    graph.DrawText('kHz', (50, 10), color='black')
    graph.DrawText('Norm Scaled AUDIO', (-5, 50), color='black', angle=90)


def drawPlot():
    # Divide horizontal axis space by data points :
    barStep = 100/CHUNK
    x_scaled = ((_VARS['audioData']/100)*GAIN)+50

    for i, x in enumerate(x_scaled):
        graph.draw_rectangle(top_left=(i*barStep, x),
                             bottom_right=(i*barStep+barStep, 50),
                             fill_color='#B6B6B6')


mV = 0
preV = 0
beaf1 = 0
dum = 0
counter = 0
avgV = 0
vCounter = 0
beatard = False

def drawFFT():
    global mV
    global avgV
    global beaf1
    global dum
    global preV
    global counter
    global vCounter
    global beatard

    barStep = 100/(CHUNK/2)  # Needed to fit the data into the plot.
    fft_data = np.fft.rfft(_VARS['audioData'])  # The proper fft calculation
    fft_data = np.absolute(fft_data)  # Get rid of negatives
    fft_data = fft_data/10000  # ghetto scaling

    for i, x in enumerate(fft_data):
        
        graph.draw_rectangle(top_left=(i*barStep, x),
                             bottom_right=(i*barStep+barStep, 50),
                             fill_color='black')
        
        if mV < x:
            beaf1 = i
            mV = x
            counter += 1
            vCounter += x
            avgV = vCounter/counter
            print(i)

        if i == beaf1 and x - preV > 30 and x > (avgV - 50):
            dum += 1
            print('beat-' + str(i) + '-' + str(dum))
            t = create_thread()
            t.start()
            


        if i == beaf1:
            preV = x
            # print(int(x))


# PYAUDIO STREAM :


def stop():
    if _VARS['stream']:
        _VARS['stream'].stop_stream()
        _VARS['stream'].close()
        _VARS['window']['-PROG-'].update(0)
        _VARS['window'].FindElement('Stop').Update(disabled=True)
        _VARS['window'].FindElement('Listen').Update(disabled=False)


def callback(in_data, frame_count, time_info, status):
    _VARS['audioData'] = np.frombuffer(in_data, dtype=np.int16)
    return (in_data, pyaudio.paContinue)


def listen():
    _VARS['window'].FindElement('Stop').Update(disabled=False)
    _VARS['window'].FindElement('Listen').Update(disabled=True)
    _VARS['stream'] = pAud.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK,
                                stream_callback=callback)
    _VARS['stream'].start_stream()


def updateUI():
    # Uodate volumne meter
    _VARS['window']['-PROG-'].update(np.amax(_VARS['audioData']))
    # Redraw plot
    graph.erase()
    drawAxis()
    drawTicks()
    drawAxesLabels()
    drawFFT()


# INIT:
drawAxis()
drawTicks()
drawAxesLabels()


# MAIN LOOP
while True:
    event, values = _VARS['window'].read(timeout=TIMEOUT)
    if event == sg.WIN_CLOSED or event == 'Exit':
        stop()
        pAud.terminate()
        break
    if event == 'Listen':
        listen()
    if event == 'Stop':
        stop()
    elif _VARS['audioData'].size != 0:
        updateUI()


_VARS['window'].close()
