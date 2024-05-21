#!/bin/bash

# Verifica se o sistema suporta a leitura do nível da bateria
if ! command -v acpi &> /dev/null; then
    echo "Este sistema não suporta a leitura do nível da bateria."
    exit 1
fi

# Obtém o nível da bateria
battery_level=$(acpi -b | grep -P -o '[0-9]+(?=%)')

# Verifica se a bateria está presente
if [ -z "$battery_level" ]; then
    echo "Nenhuma bateria detectada."
    exit 1
fi

# Exibe o nível da bateria
echo "Nível da bateria: $battery_level%"

# Verifica se o nível da bateria está abaixo de 25%
if [ "$battery_level" -lt 25 ]; then
    # Envia a notificação MQTT
    mosquitto_pub -h <broker_address> -t '#A5/bateria' -m "Atenção! Nível da bateria abaixo de 25%."
fi
