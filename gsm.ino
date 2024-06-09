#include <SoftwareSerial.h>

SoftwareSerial GSM(10, 11);

String number = "+639483572088";

const String notifyMessages[] = {
    "Feather Care System: Status is Online"
    "Feather Care System: Chicken with High Temperature Detected!", 
};

void setup() {
    Serial.begin(9600);
    GSM.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();
        switch (command) {
        case 's':
            notify(0);
            break;
        case 'n':
            notify(1);
            break;
        }
    }
}

void notify(int pos) {
    String message = notifyMessages[pos];
    GSM.println("AT+CMGF1");
    delay(200);
    GSM.println("AT+CMGS=\"" + number + "\"");
    delay(200);
    GSM.println(message);
    delay(200);
    GSM.println((char)26);
    delay(200);
}