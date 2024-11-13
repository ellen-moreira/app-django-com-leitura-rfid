#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h> // Alterado para ESP32

// Defina os pinos do módulo RFID
#define RX_PIN 16 // GPIO 16 para RX
#define TX_PIN 17 // GPIO 17 para TX

// Configuração da rede Wi-Fi
const char* ssid = "IoTLab";
const char* password = "40068718";
const String serverUrl = "http://192.168.0.104:8000/pecuaria/api/animal/"; // IP da máquina

String text;
String lastCardNumber = ""; // Variável para armazenar o último RFID lido

WebServer server(80); // Cria um servidor na porta 80

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // Inicia Serial1 com os pinos RX e TX definidos

  // Conecta ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Conectando ao Wi-Fi...");
  }
  Serial.println("Conectado ao Wi-Fi!");
  Serial.print("IP do ESP32: ");
  Serial.println(WiFi.localIP());
  Serial.println("Aproxime a tag...");

  // Inicia o servidor e define a rota
  server.on("/latest_rfid", HTTP_GET, []() {
    server.send(200, "text/plain", lastCardNumber); // Retorna o último RFID lido
  });
  server.begin();
}

void loop() {
  server.handleClient(); // Trata as requisições do servidor

  while (Serial1.available() > 0) {
    delay(5);
    char c = Serial1.read();
    text += c;
  }

  if (text.length() > 20) {
    check();  // Verifica o ID do cartão
    text = "";  // Limpa o texto para a próxima leitura
  }
}

void check() {
  // Extrai o ID do cartão
  String CardNumber = text.substring(1, 11);
  Serial.println("Card ID : " + CardNumber);
  
  lastCardNumber = CardNumber; // Armazena o último RFID lido
  // Envia o ID do cartão ao servidor
  sendToServer(CardNumber);
}

// Função para enviar o identificador ao servidor
void sendToServer(String rfid) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = serverUrl + rfid + "/";
    Serial.println(url);
    http.begin(url); // Define o URL para requisição

    int httpCode = http.GET(); // Faz uma requisição GET ao servidor
    Serial.print("Código HTTP: "); 
    Serial.println(httpCode); // Imprime o código HTTP recebido

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Resposta do servidor:");
      Serial.println(payload);
    } else {
      Serial.print("Erro ao enviar requisição: ");
      Serial.println(http.errorToString(httpCode)); // Imprime o erro
    }
    http.end(); // Fecha a conexão HTTP
  } else {
    Serial.println("Erro: Não conectado ao Wi-Fi.");
  }
}
#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h> // Alterado para ESP32

// Defina os pinos do módulo RFID
#define RX_PIN 4 // GPIO 4 para RX
#define TX_PIN 2 // GPIO 2 para TX

// Configuração da rede Wi-Fi
const char* ssid = "teste2";
const char* password = "teste321";
const String serverUrl = "http://192.168.137.17:8000/pecuaria/api/animal/"; // IP da máquina

String text;
String lastCardNumber = ""; // Variável para armazenar o último RFID lido

WebServer server(80); // Cria um servidor na porta 80

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // Inicia Serial1 com os pinos RX e TX definidos

  // Conecta ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Conectando ao Wi-Fi...");
  }
  Serial.println("Conectado ao Wi-Fi!");
  Serial.print("IP do ESP32: ");
  Serial.println(WiFi.localIP());
  Serial.println("Aproxime a tag...");

  // Inicia o servidor e define a rota
  server.on("/latest_rfid", HTTP_GET, []() {
    server.send(200, "text/plain", lastCardNumber); // Retorna o último RFID lido
  });
  server.begin();
}

void loop() {
  server.handleClient(); // Trata as requisições do servidor

  while (Serial1.available() > 0) {
    delay(5);
    char c = Serial1.read();
    text += c;
  }

  if (text.length() > 20) {
    check();  // Verifica o ID do cartão
    text = "";  // Limpa o texto para a próxima leitura
  }
}

void check() {
  // Extrai o ID do cartão
  String CardNumber = text.substring(1, 11);
  Serial.println("Card ID : " + CardNumber);
  
  lastCardNumber = CardNumber; // Armazena o último RFID lido
  // Envia o ID do cartão ao servidor
  sendToServer(CardNumber);
}

// Função para enviar o identificador ao servidor
void sendToServer(String rfid) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = serverUrl + rfid + "/";
    Serial.println(url);
    http.begin(url); // Define o URL para requisição

    int httpCode = http.GET(); // Faz uma requisição GET ao servidor
    Serial.print("Código HTTP: "); 
    Serial.println(httpCode); // Imprime o código HTTP recebido

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Resposta do servidor:");
      Serial.println(payload);
    } else {
      Serial.print("Erro ao enviar requisição: ");
      Serial.println(http.errorToString(httpCode)); // Imprime o erro
    }
    http.end(); // Fecha a conexão HTTP
  } else {
    Serial.println("Erro: Não conectado ao Wi-Fi.");
  }
}
