#!/usr/bin/env python3
import socket
import json
import re
from pathlib import Path
#pip install mcstatus
from mcstatus import JavaServer
from mcstatus import BedrockServer

# Конфигурация
SERVER_PORT = 25565
PROPERTIES_PATH = "d:/.Minecraft.1.21-paper_world_n2/server.properties"  # Измените на свой путь
OUTPUT_FILE = "_build/server_status.json"

def check_port(host='127.0.0.1', port=25565, timeout=2):
    """Проверяет, открыт ли порт сервера"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_server_info(host='127.0.0.1', port=25565, timeout=3):
    """Получает детальную информацию через протокол Minecraft"""
    try:
        server = JavaServer.lookup(host)
        status = server.status()
        print(f"The server has {status.players.online} player(s) online and replied in {status.latency} ms")

        # 'query' has to be enabled in a server's server.properties file!
        # It may give more information than a ping, such as a full player list or mod information.
        query = server.query()
        return query.raw
    except Exception as e:
        print(f"Ошибка запроса: {e}")
    return None
    
def get_bserver_info(host='127.0.0.1', port=19132, timeout=3):
    """Получает детальную информацию через протокол Minecraft"""
    try:
        server = BedrockServer.lookup(host)
        status = server.status()
        print(f"The server has {status.players.online} player(s) online and replied in {status.latency} ms")

        # 'query' has to be enabled in a server's server.properties file!
        # It may give more information than a ping, such as a full player list or mod information.
        query = server.status()
        return query
    except Exception as e:
        print(f"Ошибка запроса: {e}")
    return None


def get_version_from_properties(properties_path):
    """Извлекает версию из server.properties"""
    try:
        path = Path(properties_path)
        if not path.exists():
            return "Файл не найден"
        
        # Ищем версию в motd или server-name
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Сначала проверяем motd
        motd_match = re.search(r'^motd\s*=\s*(.+)$', content, re.MULTILINE)
        if motd_match:
            return motd_match.group(1).strip()
        
        # Затем server-name
        name_match = re.search(r'^server-name\s*=\s*(.+)$', content, re.MULTILINE)
        if name_match:
            return name_match.group(1).strip()
            
        return "Версия не указана"
    except Exception as e:
        return f"Ошибка чтения: {e}"

def main():
    
    
    print("=" * 50)
    print("Проверка Minecraft-сервера")
    print("=" * 50)
    
    # Базовая проверка порта
    is_online = check_port(port=SERVER_PORT)
    status = "🟢 ОНЛАЙН" if is_online else "🔴 ОФФЛАЙН"
    print(f"Статус: {status}")
    
    # Версия из конфига
    description = get_version_from_properties(PROPERTIES_PATH)
    
    # Детальная информация
    if is_online:
        info = get_server_info(port=SERVER_PORT)
        info_bedrock = get_bserver_info()
        if info:
            print("✓ Успешно получены данные:")
            print(f"  Описание: {description}")
            print(f"  Версия Java:    {info["version"]}")
            print(f"  Версия Bedrock: {info_bedrock.version.name}")
            
            
            # Сохраняем в JSON для веб-сайта
            output = {
                'online': True,
                'version': info["version"],
                'version_bedrock': info_bedrock.version.name,
                'numplayers': info['numplayers'],
                'maxplayers': info['maxplayers'],
                'description': description
            }
            
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(output, f, ensure_ascii=False)
            print("✓ Данные сохранены в JSON")
        else:
            print("✗ Сервер не ответил на детальный запрос")
            print("  Проверьте настройки сервера (enable-query=true)")
    else:
        # Сохраняем офлайн статус
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({'online': False, 'version': '???', 'version_bedrock':'???'}, f, ensure_ascii=False)

if __name__ == "__main__":


    main()