import Adafruit_CharLCD as LCD
from time import gmtime, strftime, sleep
import serial
from math import pi
import os

# Sems Turgut 01.08.2016 13:37

# GPIO Pinleri belirleniyor.
lcd_rs = 18
lcd_en = 23
lcd_d4 = 12
lcd_d5 = 16
lcd_d6 = 20
lcd_d7 = 21
lcd_bl = 4
lcd_cols = 20
lcd_rows = 4

# BMS degiskenleri belirleniyor.
htemp_bms = ''
atemp_bms = ''
cur_bms = ''
hvolt_bms = ''
batper_bms = ''

# Arduino dan gelen degiskenler belirleniyor.
speed_eng = ''
battemp_eng = ''
cotemp_eng = ''

# LCD ozellikleri belirleniyor.
lcd = LCD.Adafruit_CharLCD(
    lcd_rs, lcd_en, lcd_d4,
    lcd_d5, lcd_d6, lcd_d7,
    lcd_cols, lcd_rows, lcd_bl)

# USB Portlar acik mi diye test ediliyor


def portCheck():
    sleep(0.5)
    if os.path.exists('/dev/ttyUSB2'):
        print 'USB ports are OK.'
        lcd.clear()
        lcd.set_cursor(0, 1)
        lcd.message("Butun USB'ler tamam.")
        lcd.set_cursor(0, 2)
        lcd.message('>----Basliyoruz----<')
        sleep(1)
    else:
        print 'Please check USB ports.'
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.message('1-BMS:')
        if os.path.exists('/dev/ttyUSB0'):
            lcd.set_cursor(6, 0)
            lcd.message(' OK')

        lcd.set_cursor(0, 1)
        lcd.message('2-Arduino:')
        if os.path.exists('/dev/ttyUSB1'):
            lcd.set_cursor(10, 1)
            lcd.message(' OK')

        lcd.set_cursor(0, 2)
        lcd.message('3-Xbee:')
        if os.path.exists('/dev/ttyUSB2'):
            lcd.set_cursor(7, 2)
            lcd.message(' OK')
            sleep(0.5)

        lcd.set_cursor(0, 3)
        lcd.message('Lutfen sirayla takin')
        portCheck()

    ser_bms = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

    ser_eng = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)

    ser_xbee = serial.Serial(
        port='/dev/ttyUSB2',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)
    lcd.clear()
    main(ser_bms, ser_eng, ser_xbee)


# Ana fonksiyon.
def main(ser_bms, ser_eng, ser_xbee):
    print 'Successfully connected to:' + ser_bms.portstr
    print 'Successfully connected to:' + ser_eng.portstr
    print 'Successfully connected to:' + ser_xbee.portstr
    while True:
        sleep(.3)
        print strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime())
        log = []
        line = []
        # BMS den gelen veriler parse ediliyor.
        if ser_bms.isOpen():
            while True:
                try:
                    line = ser_bms.readline().split(',')
                    if ':' not in line[0]:
                        if line[0] == 'BT3':
                            htemp_bms = str(
                                (int(line[3], 16) + (-100)) * 1)
                            atemp_bms = str(
                                (int(line[4], 16) + (-100)) * 1)
                        if line[0] == 'CV1':
                            hvolt_bms = str(
                                int(line[1], 16) * 1 / 100)
                            cur_bms = str(
                                int(line[2], 16) * 1 / 10
                            )
                        if line[0] == 'BC1':
                            batper_bms = str(
                                int(line[3], 16) / 100)
                            line = []
                            break
                    else:
                        if line[2] == 'BT3':
                            htemp_bms = str(
                                (int(line[3], 16) + (-100)) * 1)
                            atemp_bms = str(
                                (int(line[4], 16) + (-100)) * 1)
                        if line[2] == 'CV1':
                            hvolt_bms = str(
                                int(line[3], 16) * 1 / 100)
                            cur_bms = str(int(line[4], 16) / 10)
                        if line[2] == 'BC1':
                            batper_bms = str(
                                int(line[5], 16) / 100)
                            line = []
                            break
                except (IndexError, ValueError) as e:
                    print e
                    htemp_bms = '0'
                    atemp_bms = '0'
                    cur_bms = '0'
                    hvolt_bms = '0'
                    batper_bms = '0'

        else:
            print 'USB0|BMS:Handling data problem. Please check connections.'

            # Arduino dan gelen veriler parse ediliyor.
        if ser_eng.isOpen():
            try:
                line = []
                line = ser_eng.readline().split(',')

                '''speed_eng = str(
                    int(((int(line[1]) * (21 * pi)) / 60) * 0.09144)
                ) '''

                speed_eng = line[1]
                battemp_eng = line[2]
                cotemp_eng = line[3]
            except (IndexError, ValueError) as e:
                print e
                speed_eng = '0'
                battemp_eng = '0'
                cotemp_eng = '0'

        else:
            print 'USB1|ENG:Handling data problem. Please check connections.'

        # Veriler 20x4 LCD ekrana yazdiriliyor.
        if str(speed_eng) != '':

            lcd.set_cursor(8, 0)
            lcd.message('    ')
            lcd.set_cursor(8, 1)
            lcd.message('    ')
            lcd.set_cursor(8, 2)
            lcd.message('    ')
            lcd.set_cursor(8, 3)
            lcd.message('    ')

            lcd.set_cursor(0, 0)
            lcd.message('Speed  :')
            lcd.set_cursor(8, 0)
            lcd.message(str(speed_eng) + '  KM/H')
            lcd.set_cursor(0, 1)
            lcd.message('CTemp  :')
            lcd.set_cursor(8, 1)
            lcd.message(str(cotemp_eng) + '   C')
            lcd.set_cursor(0, 2)
            lcd.message('BTemp  :')
            lcd.set_cursor(8, 2)
            lcd.message(str(battemp_eng) + '   C')
            lcd.set_cursor(0, 3)
            lcd.message('Battery:')
            lcd.set_cursor(8, 3)
            lcd.message('%' + str(batper_bms))

            # Parse edilen veriler Xbee ile pit'e gonderiliyor.
        if ser_xbee.isOpen():
            if str(speed_eng) != '':
                print('Speed :' + str(speed_eng) + 'KM/H | CTemp :' +
                      str(cotemp_eng) + 'C | BTemp :' +
                      str(battemp_eng) + 'C | Battery:' +
                      str(batper_bms) + '%'
                      )

                print('#' + ',' + str(battemp_eng) + ',' +
                      str(cotemp_eng) + ',' +
                      str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                      str(speed_eng) + ',' +
                      str(batper_bms) + ',' + '?')

                ser_xbee.writelines('#' + ',' + str(battemp_eng) + ',' +
                                    str(cotemp_eng) + ',' +
                                    str(cur_bms) + ',' + str(hvolt_bms) + ',' +
                                    str(speed_eng) + ',' +
                                    str(batper_bms) + ',' + '?')
        else:
            print 'USB2|XBEE:Sending data problem. Please check connections.'

        with open('/home/pi/TELEMETRY_LOG.txt', 'a') as file:
            file.write(
                strftime("Date :%Y-%m-%d Time :%H:%M:%S", gmtime()) + '\n')
            file.write('htemp_bms :' + htemp_bms + 'atemp_bms :' + atemp_bms +
                       'cur_bms :' + cur_bms + 'hvolt_bms :' + hvolt_bms +
                       'batper_bms :' + batper_bms + '\n')
            file.write('speed_eng :' + speed_eng + 'battemp_eng :' +
                       battemp_eng + 'cotemp_eng' + cotemp_eng + '\n')
            file.close()

    # Yeniden baslatilmayi bekleme komutu


def update():
    cnt = 0
    while True:
        lcd.clear()
        lcd.set_cursor(0, cnt)
        lcd.message('Waiting for update')
        print 'Waiting for update'
        cnt = cnt + 1
        if cnt > 3:
            cnt = 0
        sleep(.5)


def splash():
    lcd.clear()
    while True:
        lcd.set_cursor(0, 3)
        lcd.message("USB'leri cikariniz.")
        lcd.set_cursor(0, 0)
        lcd.message('USB0 :')
        if not os.path.exists('/dev/ttyUSB0'):
            lcd.set_cursor(6, 0)
            lcd.message(' OK')

        lcd.set_cursor(0, 1)
        lcd.message('USB1 :')
        if not os.path.exists('/dev/ttyUSB1'):
            lcd.set_cursor(6, 1)
            lcd.message(' OK')

        lcd.set_cursor(0, 2)
        lcd.message('USB2 :')
        if not os.path.exists('/dev/ttyUSB2'):
            lcd.set_cursor(6, 2)
            lcd.message(' OK')

        if not os.path.exists('/dev/ttyUSB0'):
            if not os.path.exists('/dev/ttyUSB1'):
                if not os.path.exists('/dev/ttyUSB2'):
                    sleep(.3)
                    break

        sleep(0.2)

    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.message('<--BULENT ECEVIT-->')
    lcd.set_cursor(0, 1)
    lcd.message('   MUH. FAKULTESI   ')
    lcd.set_cursor(0, 2)
    lcd.message('    ROBOT KULUBU    ')
    lcd.set_cursor(0, 3)
    lcd.message('>-----VOLTRAN-----<')
    sleep(3)

    cnt = 3
    while True:
        lcd.clear()
        lcd.set_cursor(0, cnt)
        lcd.message('<----YUKLENIYOR---->')
        print '<----YUKLENIYOR---->'
        cnt = cnt - 1
        if cnt < 0:
            break
        sleep(.5)


try:
    splash()
    portCheck()
except KeyboardInterrupt:
    print 'Interrupted.'
    update()
