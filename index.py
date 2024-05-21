import subprocess
import paho.mqtt.client as mqtt

# Função para verificar o nível da bateria
def check_battery_level():
    try:
        # Obtém o nível da bateria usando o comando acpi
        output = subprocess.check_output(["acpi", "-b"]).decode("utf-8").strip()
        battery_level = int(output.split(", ")[1].split()[0][:-1])  # Extrai o nível da bateria em porcentagem
        return battery_level
    except Exception as e:
        print("Erro ao obter o nível da bateria:", e)
        return None

# Função de callback para quando a conexão MQTT é estabelecida
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker MQTT com código de resultado:", rc)

# Endereço do broker MQTT
broker_address = "<broker_address>"

# Cria um cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conecta ao broker MQTT
client.connect(broker_address)

# Verifica o nível da bateria
battery_level = check_battery_level()

# Se o nível da bateria for inferior a 25%, envia uma notificação MQTT
if battery_level is not None and battery_level < 25:
    client.publish("#A5/bateria", "Atenção! Nível da bateria abaixo de 25%.")

# Fecha a conexão MQTT
client.disconnect()
