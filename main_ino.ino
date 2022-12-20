#include <SerialTransfer.h>
#include <ArduPID.h>

#define mla 6
#define mlb 7
#define spd 5

ArduPID myController;

double aux = 0.0;

double p=1;
double i=0;
double d=0;

String userDataUpdate = "";

double setpoint=180; //angulo
double input;
double output;
double speedMot;

int controle = 0;

void getUserData(){

  String P;
  String I;
  String D;

  String findDelimiter;
  String Setpoint;
  String VelMot;
  String Input;
  String activation;
  int delimiterInt = 0;

  //userDataUpdate = ("1-0-1-320-255-144.0902769208223-1.0+");

  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();
  
  P = userDataUpdate.substring(0,delimiterInt);
  userDataUpdate.remove(0,delimiterInt+1);
  
  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();

  I = userDataUpdate.substring(0,delimiterInt); 
  userDataUpdate.remove(0,delimiterInt+1);

  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();

  D = userDataUpdate.substring(0,delimiterInt);
  userDataUpdate.remove(0,delimiterInt+1);

  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();

  Setpoint = userDataUpdate.substring(0,delimiterInt);
  userDataUpdate.remove(0,delimiterInt+1); 

  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();
  
  VelMot = userDataUpdate.substring(0,delimiterInt);
  userDataUpdate.remove(0,delimiterInt+1);

  findDelimiter = userDataUpdate.indexOf("-");
  delimiterInt = findDelimiter.toInt();

  Input = userDataUpdate.substring(0,delimiterInt);
  userDataUpdate.remove(0,delimiterInt+1);

  activation = userDataUpdate;
  
  p = P.toDouble();
  i = I.toDouble();
  d = D.toDouble();

  setpoint = Setpoint.toDouble();
  speedMot= VelMot.toDouble();
  input= Input.toDouble();
  aux = activation.toDouble();

}


void setup(){

    Serial.begin(115200);
    
    pinMode(mla,OUTPUT);
    pinMode(mlb,OUTPUT);
    pinMode(spd,OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    myController.begin(&input, &output, &setpoint, p, i, d);
    myController.setOutputLimits(-255, 255);   
    myController.start();

}

void loop(){

    if(Serial.available()){

        char c = Serial.read();
        Serial.println(userDataUpdate);
        Serial.println(c);
        if(c == '+'){

            getUserData();
            Serial.println(p);
            Serial.println(i);
            Serial.println(d);
            userDataUpdate = "";

            if(p == 1.0){

                digitalWrite(LED_BUILTIN, HIGH);

                }
                
            else{

                digitalWrite(LED_BUILTIN,LOW);

                }


            if(aux != 1.0){

                myController.stop();
                controle = 0;

                }

            if(aux == 1.0 & controle == 0){

                myController.start();
                controle = 1;

                }

            myController.compute();
                
            myController.debug(&Serial, "myController", PRINT_INPUT | PRINT_OUTPUT | PRINT_SETPOINT | PRINT_P);

            

            if(output > 0){//lado de giro observar sinal do OUTPUT

                digitalWrite(mla,0); 
                digitalWrite(mlb,1);

                analogWrite(spd,output);//vel do motor proporcional ao erro(output)
                Serial.println(output);
                }

                else{

                    digitalWrite(mla,1); 
                    digitalWrite(mlb,0);

                    output = -1*output;

                    analogWrite(spd,output);//vel do motor proporcional ao erro(output)
                    Serial.println(output);
                }
            userDataUpdate = "";

        }
        else{

            userDataUpdate += c;

        }

 
        //mover motor 1 ver lado de rotação e operar de forma binária o motor
  }
        //enviar valores P I e D para o python e escrever o gráfico
}
