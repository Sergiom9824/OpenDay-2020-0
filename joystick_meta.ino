// Analog Pins connected to the joystick outputs
int Eje_X = 1;
int Eje_Y = 2;
int Pr = 4;
int Pl = 5;
void setup() {
 
  //Initialize serial communication at 9600 bps
  Serial.begin(9600);
  pinMode(Pr, INPUT);
  pinMode(Pl, INPUT);
 
  }
 
void loop() {
 
  //Assign the analog values received to variables
  int DX = analogRead(Eje_X);
  int DY = analogRead(Eje_Y);

  //Lee valor del pulsador
  int Pulsador_rigth = digitalRead(Pr);
  int Pulsador_left = digitalRead(Pl);
  
  
  //Concatenate the variables in a String
  String Lectura = String(DX) + "/" + String(DY) + "/" + String(Pulsador_left) + "/" + String(Pulsador_rigth);

  //Prints the String to the serial port
  Serial.println(Lectura);
  
}
