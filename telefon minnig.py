import socket
import hashlib
import urllib.request
import json
import time

# --- KULLANICI AYARLARI ---
USERNAME = "KENDI_DUCO_KULLANICI_ADIN" # Cüzdan kullanıcı adını buraya yaz!
MINER_NAME = "StealthPhone"          # Hayalet madenci adı

def get_mining_pool():
    try:
        response = urllib.request.urlopen("https://duinocoin.com").read().decode()
        pool_data = json.loads(response)
        return pool_data["ip"], pool_data["port"]
    except:
        time.sleep(10)
        return get_mining_pool()

def start_stealth_mining():
    print("🕵️‍♂️ Hayalet Madenci Arka Planda Başlatıldı (Güvenli Mod)...")
    
    while True:
        try:
            ip, port = get_mining_pool()
            soc = socket.socket()
            soc.connect((ip, int(port)))
            soc.recv(100) # Versiyon kontrolünü geç
            
            while True:
                # Sunucudan iş iste
                soc.send(f"JOB,{USERNAME},LOW,KozmoSecretKey".encode())
                job_data = soc.recv(1024).decode().rstrip("\n").split(",")
                
                if len(job_data) < 3:
                    break
                    
                previous_hash = job_data[0]
                expected_hash = job_data[1]
                difficulty = int(job_data[2])
                
                start_time = time.time()
                
                # --- GÜVENLİ VE YAVAŞLATILMIŞ DÖNGÜ ---
                for nonce in range(100 * difficulty + 1):
                    hash_result = hashlib.sha1((previous_hash + str(nonce)).encode()).hexdigest()
                    
                    # 🚨 TELEFONU KORUMA HAMLESİ: Her 500 denemede bir işlemciyi dinlendir!
                    if nonce % 500 == 0:
                        time.sleep(0.05) # İşlemcinin nefes alması için 50 milisaniye uyu
                    
                    if hash_result == expected_hash:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        hashrate = nonce / elapsed_time if elapsed_time > 0 else 0
                        
                        # Sonucu gönder
                        soc.send(f"{nonce},{hashrate:.0f},Python Stealth Miner,{MINER_NAME}".encode())
                        feedback = soc.recv(100).decode().rstrip("\n")
                        
                        if feedback == "GOOD":
                            print(f"🟢 Güvenli Mod: Blok Kazıldı! Telefon Sıcaklığı: Normal 🧊")
                        
                        # 🚨 BLOK ARASI BÜYÜK MOLA: İki blok arasında telefonu tamamen dinlendir!
                        time.sleep(3) # Her blok kazıldığında 3 saniye tamamen dur. Telefon buz gibi kalsın.
                        break
                        
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    start_stealth_mining()
