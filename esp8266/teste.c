#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WebServer.h> // Adicione esta linha

// Defina os pinos do módulo RFID
#define RX_PIN D7
#define TX_PIN D8

// Configuração da rede Wi-Fi (Para funcionar para testes, deve estar conectado na mesma rede que o servidor django)
const char* ssid = "teste2"; // Nome da rede Wifi
const char* password = "teste321"; // Senha da rede Wifi
const String serverUrl = "http://192.168.137.17:8000/pecuaria/api/animal/"; // IP da máquina 

// Para obter o ip, digitar ipconfig no cmd e pegar o ipv4

SoftwareSerial RFID(RX_PIN, TX_PIN);
String text;
String lastCardNumber = ""; // Variável para armazenar o último RFID lido

ESP8266WebServer server(80); // Cria um servidor na porta 80

void setup() {
	Serial.begin(9600);
	RFID.begin(9600);

	// Conecta ao Wi-Fi
	WiFi.begin(ssid, password);

	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.println("Conectando ao Wi-Fi...");
	}

	Serial.println("Conectado ao Wi-Fi!");
	Serial.println("IP do ESP8266: ");
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

	while (RFID.available() > 0) {
		delay(5);
		char c = RFID.read();
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
		WiFiClient client;
		String url = serverUrl + rfid + "/";

		Serial.println(url);

		http.begin(client, url); // Define o URL para requisição

		int httpCode = http.GET(); // Faz uma requisição GET ao servidor

		Serial.println("Código HTTP: "); 
		Serial.println(httpCode); // Imprime o código HTTP recebido

		if (httpCode > 0) {
			String payload = http.getString();

			Serial.println("Resposta do servidor:");
			Serial.println(payload);
		} else {
			Serial.println("Erro ao enviar requisição: ");
			Serial.println(http.errorToString(httpCode)); // Imprime o erro
		}

			http.end(); // Fecha a conexão HTTP
	} else {
		Serial.println("Erro: Não conectado ao Wi-Fi.");
	}
}