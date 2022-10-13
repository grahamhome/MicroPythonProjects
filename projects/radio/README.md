### Radio Communication

#### Status: Not Working, WIP

#### Overview
The goal of this project is to find and learn to use a MicroPython library 
for the NRF24L01+ FM radio modules I have.
I want to be able to send and receive arbitrary data between Pi Pico units. 
I plan to write a component class to simplify the use of my chosen library.

#### Updates
9/15/22:
I only have one Pico that can interface with my radios right now. 
The other one mysteriously does not. 
I am waiting for another Pico to arrive before I can continue with this project.

10/12/22:
I now have 2 Picos connected to radios and successfully interfacing with them.
However, the radios are only intermittently able to exchange messages. After 
researching this problem online I have found a couple of hacks to improve connectivity 
a very small amount by attaching a 10uF capacitor between the VCC and GND pins of the 
NRF24L01+ radio board, and by placing my finger on the radio antenna trace to raise 
its capacitance. Based on these experiments I am hypothesizing that the USB power supply I
am using to power the Pico is not stable enough for the NRF24L01+ radios, or perhaps they 
are simply of poor quality. I have purchased a new set of NRF24L01+ boards which have 
a 3.3V regulator included in each board. I hope that the combination of the power regulator 
and what appears to be a higher-quality board will help me to finally get my test code
running successfully so that I may proceed to build projects with the NRF24L01+. 