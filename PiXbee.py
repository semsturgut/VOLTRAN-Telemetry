import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5)

temp1 = 25
coctemp = 35
cur = 90
volt = 12
speed = 60

if ser.isOpen:
    while True:
        speed = speed + 1
        ser.writelines('#' + ',' + str(temp1) + ',' +
                       str(coctemp) + ',' +
                       str(cur) + ',' + str(volt) + ',' +
                       str(speed) + ',' + '?')

        print('#' + ',' + str(temp1) + ',' +
              str(coctemp) + ',' +
              str(cur) + ',' + str(volt) + ',' +
              str(speed) + ',' + '?')

#            def wait():
#                cnt = 0
#                while True:
#                    lcd.clear()
#                    lcd.set_cursor(1, cnt)
#                    lcd.message('Waiting for update')
#                    print 'Waiting for update'
#                    cnt = cnt + 1
#                    if cnt > 3:
#                        cnt = 0
#                    time.sleep(.5)
