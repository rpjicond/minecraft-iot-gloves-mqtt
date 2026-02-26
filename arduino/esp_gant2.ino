#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Configuration Wi-Fi
const char* ssid = "SAE304-LDA";
const char* password = "lidian20";

// Configuration MQTT
const char* mqtt_server = "192.168.1.125";
const int mqtt_port = 1883;
const char* mqtt_client_id = "ESP8266_Gant";
const char *mqtt_username = "jouer2"; 
const char *mqtt_password = "craft"; 

  // Déclaration des broches des boutons
  #define BP_INDEX 0
  #define BP_MAJEUR 2
  #define BP_ANNUAIRE 12
  #define BP_AURICULAIRE 14

//Déclaration des topics
#define TOPIC_INDEX "gant2/index"
#define TOPIC_MAJEUR  "gant2/majeur"
#define TOPIC_ANNUAIRE "gant2/annulaire"
#define TOPIC_AURICULAIRE "gant2/auriculaire"

WiFiClient espClient;
PubSubClient client(espClient);

// Variables pour mémoriser l'heure du dernier appui sur chaque bouton
unsigned long lastPressTimeIndex = 0;
unsigned long lastPressTimeMajeur = 0;
unsigned long lastPressTimeAnnuaire = 0;
unsigned long lastPressTimeAuriculaire = 0;
const int debounceDelay = 500;    // Délai pour l'anti-rebond (500ms)
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au WiFi...");
  }
  Serial.println("Connecte au WiFi");

  client.setServer(mqtt_server, mqtt_port);

    pinMode(BP_INDEX, INPUT_PULLUP);
    pinMode(BP_MAJEUR, INPUT_PULLUP);
    pinMode(BP_ANNUAIRE, INPUT_PULLUP);
    pinMode(BP_AURICULAIRE, INPUT_PULLUP);
}

void connectToMQTTBroker() {
  
 while (!client.connected()) {
    String client_id = "Gant1");
    Serial.printf("Connexion  au MQTT Broker comme %s.....\n", client_id.c_str());
    if (client.connect(mqtt_client_id,mqtt_username,mqtt_password)){ //Connexion sécurisée avec mot de passe
      Serial.print("Connecte au MQTT broker \n");
    } else {
        Serial.print("La connexion au MQTT broker a faille");
         if(client.state()==4 || client.state()==5) //client.state()=4 : MQTT_CONNECT_BAD_CREDENTIALS
                                                   //client.state()=5: MQTT_CONNECT_UNAUTHORIZED
            Serial.print(" le client n'a pas été autorisé à se connecter, revoir les identifiants\n");
        delay(5000);
    } 
  }   
}

void loop() {
  if (!client.connected()) {
    connectToMQTTBroker();
  }
  client.loop();

  unsigned long currentTime = millis(); // Récupérer l'heure actuelle

  if (digitalRead(BP_INDEX) == LOW) {
    if (currentTime - lastPressTimeIndex > debounceDelay) {
      Serial.println("Gant2 BP_Index pressé");
      client.publish(TOPIC_INDEX, "ON");
      lastPressTimeIndex = currentTime;
    }
  }

  if (digitalRead(BP_MAJEUR) == LOW) {
    if (currentTime - lastPressTimeMajeur > debounceDelay) {
      Serial.println("Gant2 BP_majeur pressé");
      client.publish(TOPIC_MAJEUR, "ON");
      lastPressTimeMajeur = currentTime;
    }
  }

  if (digitalRead(BP_ANNUAIRE) == LOW) {
    if (currentTime - lastPressTimeAnnuaire > debounceDelay) {
      Serial.println("Gant2 BP_annuaire pressé");
      client.publish(TOPIC_ANNUAIRE, "ON");
      lastPressTimeAnnuaire = currentTime;
    }
  }

  if (digitalRead(BP_AURICULAIRE) == LOW) {
    if (currentTime - lastPressTimeAuriculaire > debounceDelay) {
      Serial.println("Gant2 BP_auriculaire pressé");
      client.publish(TOPIC_AURICULAIRE, "ON");
      lastPressTimeAuriculaire = currentTime;
    }
  }

  delay(50);
}
