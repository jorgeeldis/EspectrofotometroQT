#include <math.h>

/*
 * Macro Definitions
 */
#define SPEC_ST A1     //A1
#define SPEC_CLK A2    //A2
#define SPEC_VIDEO A0  //A0

#define SPEC_CHANNELS 288  // New Spec Channel
uint16_t data[SPEC_CHANNELS];
uint16_t wavelength[SPEC_CHANNELS];

void setup() {

  //Set desired pins to OUTPUT
  pinMode(SPEC_CLK, OUTPUT);
  pinMode(SPEC_ST, OUTPUT);

  digitalWrite(SPEC_CLK, HIGH);  // Set SPEC_CLK High
  digitalWrite(SPEC_ST, LOW);    // Set SPEC_ST Low

  Serial.begin(9600);  // Baud Rate set to 115200
}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */
void readSpectrometer() {

  int delayTime = 1;  // delay time

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);

  //Sample for a period of time
  for (int i = 0; i < 15; i++) {

    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime);
  }

  //Set SPEC_ST to low
  digitalWrite(SPEC_ST, LOW);

  //Sample for a period of time
  for (int i = 0; i < 85; i++) {

    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime);
  }

  //One more clock pulse before the actual read
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);

  //Read from SPEC_VIDEO
  for (int i = 0; i < SPEC_CHANNELS; i++) {

    data[i] = abs(analogRead(SPEC_VIDEO) - 1024);
    wavelength[i] = 3.059651344 * pow(10, 2) + 2.716298429 * i - 1.284751120 * pow(10, -3) * pow(i, 2) - 6.672071166 * pow(10, -6) * pow(i, 3) + 5.557539172 * pow(10, -9) * pow(i, 4) + 1.015634508 * pow(10, -11) * pow(i, 5);
    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime);
  }

  //Set SPEC_ST to high
  digitalWrite(SPEC_ST, HIGH);

  //Sample for a small amount of time
  for (int i = 0; i < 7; i++) {

    digitalWrite(SPEC_CLK, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW);
    delayMicroseconds(delayTime);
  }

  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
}

/*
 * The function below prints out data to the terminal or 
 * processing plot
 */
void printData() {

  for (int i = 0; i < SPEC_CHANNELS; i++) {

    Serial.print(wavelength[i]);
    Serial.print(",");
    Serial.println(data[i]);
  }
}

void loop() {

  readSpectrometer();
  printData();
  delay(10);
  
}
