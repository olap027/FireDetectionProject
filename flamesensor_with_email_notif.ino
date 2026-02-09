#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

const int buzzerPin = 9;     
const int relayPin  = 7;     
const int threshold = 50;    

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Force OFF immediately
  
  Serial.begin(9600);
  mlx.begin();
  pinMode(buzzerPin, OUTPUT);

  // Tell Python we are ready
  Serial.println("SYSTEM_READY");
}

void loop() {
  float objTemp = mlx.readObjectTempC();

  if (objTemp >= threshold) {
    digitalWrite(relayPin, HIGH);  
    
    // Format: "ALERT:52.45"
    Serial.print("ALERT:"); 
    Serial.println(objTemp);
    
    playWailSiren();               
  } else {
    noTone(buzzerPin);
    digitalWrite(relayPin, LOW);   
    
    // Send normal data for Python logs
    Serial.print("NORMAL:");
    Serial.println(objTemp);
    
    delay(1000); 
  }
}

void playWailSiren() {
  for (int freq = 600; freq <= 1300; freq += 20) {
    tone(buzzerPin, freq);
    delay(5);
  }
  for (int freq = 1300; freq >= 600; freq -= 20) {
    tone(buzzerPin, freq);
    delay(5);
  }
}