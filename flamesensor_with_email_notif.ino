const int flameSensor = A0; // Connect IR sensor to Analog Pin A0
const int buzzerPin = 9;    // Buzzer on Pin 9
int threshold = 200;        // Adjust this based on your sensor sensitivity

void setup() {
  pinMode(flameSensor, INPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600); // Communication with Python
}

void loop() {
  int sensorValue = analogRead(flameSensor);

  // IR sensors usually return a LOW value when fire is detected
  if (sensorValue < threshold) { 
    Serial.println("FIRE_DETECTED"); // Signal for Python
    playSiren(); 
  }
  delay(100);
}

void playSiren() {
  for (int i = 0; i < 2; i++) {
    for (int freq = 600; freq <= 1200; freq += 10) { tone(buzzerPin, freq); delay(2); }
    for (int freq = 1200; freq >= 600; freq -= 10) { tone(buzzerPin, freq); delay(2); }
  }
  noTone(buzzerPin);
}