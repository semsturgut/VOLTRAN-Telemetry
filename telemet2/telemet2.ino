
//calculations
//tire radius ~ 13.5 inches
//cevre = pi*2*r =~85 inches
//max speed of 35mph =~ 616inches/second
//max rps =~7.25

#define reed A0
#define koksic A1
#define batsic A2
//storage variables
int reedVal;
int koksicval;
int batsicval;
long timer;// time between one full rotation (in ms)
float mph;
float radius = 12;// tire radius (in inches)
float cevre;
float hiz;

int solsinyal=LOW;
int sagsinyal=LOW;
int dortlu=LOW;

int led =13;
const int sol = 3;   
const int sag = 4;
const int dortlum = 5;

int maxReedCounter = 100;//min time (in ms) of one rotation (for debouncing)
int reedCounter=0;

void setup(){

pinMode(sol,INPUT);
pinMode(sag,INPUT);
pinMode(dortlum,INPUT);
pinMode(led,OUTPUT);
pinMode(10,OUTPUT);
pinMode(11,OUTPUT);

  
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
  
solsinyal=digitalRead(sol);
sagsinyal=digitalRead(sag);
dortlu=digitalRead(dortlum);



  if(solsinyal==HIGH){
    digitalWrite(led,HIGH);
    
    digitalWrite(10,HIGH);
    delay(700);
   // Serial.println(sol);
    digitalWrite(10,LOW);
    digitalWrite(led,LOW);
    delay(700);
  }
  if(sagsinyal==HIGH){
    digitalWrite(11,HIGH);
    delay(700);
    digitalWrite(11,LOW);
    delay(700);
  }

  if(dortlu==HIGH){
   dortluler();
  }

  //print mph once a second
hiz=mph*1.6;//kmh a geçiş

 Serial.print(" ,");
 Serial.print(hiz);
 Serial.print(",");
 Serial.print(koksicval);
 Serial.print(",");
 Serial.print(batsicval);
 Serial.println(",");
 
 
  
}



void dortluler(){
  digitalWrite(10,HIGH);
   digitalWrite(11,HIGH);
   delay(700);
   digitalWrite(10,LOW);
   digitalWrite(11,LOW);
   delay(700);
}
/*
void displayMPH(){

 float hiz=mph*1.6;
  Serial.println(hiz);
}





/*/*/*//
 * /*
 * /
 * */
 /*
  * *
  * /
  * 
  */

*/
