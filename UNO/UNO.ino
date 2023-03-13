#include <SoftwareSerial.h>
SoftwareSerial ArduinoUno(10,9);
int led[]={2,3,4,5,6,7,8};

int number[][7]={
  {0,1,1,0,0,0,0},
  {1,1,0,1,1,0,1},
  {1,1,1,1,0,0,1},
  {0,1,1,0,0,1,1},
  {1,0,1,1,0,1,1},
  {1,0,1,1,1,1,1}
  };
  int count=6;
void display(int n){
    for(int i=0;i<7;i++){
    digitalWrite(led[i],!number[n-1][i]);
    };
    delay(500);
  }
}
void setup(){
	
	Serial.begin(9600);
	ArduinoUno.begin(4800);
   pinMode(led[0],OUTPUT);
 pinMode(led[1],OUTPUT);
 pinMode(led[2],OUTPUT);
 pinMode(led[3],OUTPUT);
 pinMode(led[4],OUTPUT);
 pinMode(led[5],OUTPUT);
 pinMode(led[6],OUTPUT);
}

void loop(){
	
	while(ArduinoUno.available()>0){
	float val = ArduinoUno.parseFloat();
	if(ArduinoUno.read()== '\n'){
	Serial.println(val);
  if(val.indexOf('occupied')>0){
      display(val.substring(val.indexOf('occupied')+1));
    }
	}
}
delay(30);
}
