#include <LiquidCrystal.h> /* LCD kullanimi icin kutuphane dahil edilmelidir */
/*voltran lcd 
 * sarı +5V
 * yeşil 24
 * koyu grimsi 25
 * bantlı mavi 31
 * beyaz 32
 * mor toprak
 * bantlı yeşil 23
 * mavi 22
 * 
 * 
 * 
 Devre şeması;
lcd 1,5 torpak
lcd 2 +5V
lcd 3 den torpaga direnç
lcd 4 12. pin
lcd 6--> 11.pin//31
lcd 14.pin-->ardu 2.pin//32
lcd 13-->3.pin //23
lcd 12-->4.pin//24
lcd 11-->5.pin//25
 
 - LCD'nin RS pini -> Arduino'nun 12. pini
 - LCD'nin Enable (E) pini -> Arduino'nun 11. pini
 - LCD'nin D4 pini -> Arduino'nun 5. pini
 - LCD'nin D5 pini -> Arduino'nun 4. pini
 - LCD'nin D6 pini -> Arduino'nun 3. pini
 - LCD'nin D7 pini -> Arduino'nun 2. pini
 
 - LCD'nin R/W pini -> toprağa
 - LCD'nin R0 pini -> potansiyometre çıkışına
 - LCD VDD -> Arduino 5 Voltuna
 - LCD VSS -> toprağa
*/

//mega için fotosu telde.
LiquidCrystal lcd(32,31 , 25, 24, 23, 22); /* LCDnin baglandigi Arduino pinleri */

//sensor ile deneme yapılmalı

//calculations
//tire radius ~ 13.5 inches
//cevre = pi*2*r =~85 inches
//max speed of 35mph =~ 616inches/second
//max rps =~7.25

#define reed A0//pin connected to read switch
#define koksic A1
#define batsic A2
//storage variables
int reedVal;
int koksicval;
int batsicval;
long timer;// time between one full rotation (in ms)
float mph;
float radius = 18;// tire radius (in inches)
float cevre;
float hiz;

int maxReedCounter = 100;//min time (in ms) of one rotation (for debouncing)
int reedCounter=0;


void setup(){
  lcd.begin(20, 4); /* Kullandigimiz LCDnin sutun ve satir sayisini belirtmeliyiz */
  //reedCounter = maxReedCounter;
  cevre = 2*3.14*radius;
  pinMode(reed, INPUT);
  pinMode(koksic,INPUT);
  pinMode(batsic,INPUT);
  
  
  // TIMER SETUP- the timer interrupt allows
  //precise timed measurements of the reed switch
  //for more info about configuration of arduino 
  //timers see http://arduino.cc/playground/Code/Timer1
  cli();//stop interrupts

  //set timer1 interrupt at 1kHz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;
  // set timer count for 1khz increments
  
    //OCR1A = 15624;
OCR1A = 666;// = (1/1000) / ((1/(16*10^6))*8) - 1
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS11 bit for 8 prescaler
  TCCR1B |= (1 << CS11); //saat hızında çalışacak 16/8=2MHz  
  //  TCCR1B |= (1 << CS12) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A); // timer1 kesmesi aktif
  
  sei();//tüm kesmeler aktif
  //END TIMER SETUP
  
  Serial.begin(9600);
}


ISR(TIMER1_COMPA_vect) {//Interrupt at freq of 1kHz to measure reed switch
  reedVal = digitalRead(reed);//get val of A0
  if (reedVal){//if reed switch is closed
    if (reedCounter == 0){//min time between pulses has passed
      
      mph = (56.8*float(cevre))/float(timer);//calculate miles per hour
      timer = 0;//reset timer
      reedCounter = maxReedCounter;//reset reedCounter
    }
   /* else{
      if (reedCounter > 0){//don't let reedCounter go negative
        reedCounter -= 1;//decrement reedCounter
      }
    }
    */
  }
  else{//if reed switch is open
    if (reedCounter > 0){//don't let reedCounter go negative
      reedCounter -= 1;//decrement reedCounter
    }
  }
  
  if (timer > 2000){
    mph = 0;//if no new pulses from reed switch- tire is still, set mph to 0
  }
  else{
    timer += 1;//increment timer
  } 
  
}


void loop(){
  koksicval=(analogRead(koksic)*500)/1023;
  batsicval=(analogRead(batsic)*500)/1023;
  

  //print mph once a second
hiz=mph*1.6;//kmh a geçiş
  Serial.print(",");
 Serial.print("55");
 Serial.print(",");
 Serial.print("98");
 Serial.print(",");
 Serial.println(hiz);
 
 delay(500);

  lcd.setCursor(0,0);
  lcd.print("HIZ:");
  lcd.setCursor(5,0);
  lcd.print(hiz);
  lcd.setCursor(0,1);
  lcd.print("KOKPIT SIC:");
  lcd.setCursor(12,1);
  lcd.print(koksicval);
  lcd.setCursor(0,2);
  lcd.print("BATARYA SIC:");
  lcd.setCursor(13,2);
  lcd.print(batsicval);

  
}


void displayMPH(){

 float hiz=mph*1.6;
  Serial.println(hiz);
}


