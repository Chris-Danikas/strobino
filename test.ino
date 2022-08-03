int x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop() {
  while (Serial.available() == 0){
    
  }
  int x = Serial.readString().toInt();
  digitalWrite(x/10, x%10);
}
