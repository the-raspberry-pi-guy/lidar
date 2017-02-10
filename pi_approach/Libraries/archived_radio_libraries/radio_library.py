# Radio Communication Abstraction Library

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev

class radio_comms(object):
        """ An all-powerful radio communication class using NRF24"""

        pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
        radio = NRF24(GPIO, spidev.SpiDev())

        def __init__(self):
                radio_comms.radio.begin(0, 17)
                time.sleep(1)
                radio_comms.radio.setRetries(15,15)
                radio_comms.radio.setPayloadSize(32)
                radio_comms.radio.setChannel(0x60)
                radio_comms.radio.setDataRate(NRF24.BR_2MBPS)
                radio_comms.radio.setPALevel(NRF24.PA_MIN)
                radio_comms.radio.setAutoAck(True)
                radio_comms.radio.enableDynamicPayloads()
                radio_comms.radio.enableAckPayload()
                radio_comms.radio.openWritingPipe(radio_comms.pipes[1])
                radio_comms.radio.openReadingPipe(1, radio_comms.pipes[0])
                radio_comms.radio.printDetails()

        def send_data(self,data):
                radio_comms.radio.write(data)
                print("Sent: ", data)

        def recv_data(self):
                radio_comms.radio.startListening()
                data_pipe = [0]
                while not radio_comms.radio.available(data_pipe):
                        time.sleep(0.01)
                recv_buffer = []
                radio_comms.radio.read(recv_buffer, radio_comms.radio.getDynamicPayloadSize())
                radio_comms.radio.stopListening()
                return recv_buffer
