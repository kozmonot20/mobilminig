import socket
import hashlib
import urllib.request
import json
import time
import threading

# --- KULLANICI AYARLARI ---
USERNAME = "KENDI_DUCO_KULLANICI_ADIN"  # Buraya kendi Duino-Coin kullanıcı adınızı yazın
MINER_NAME = "StealthPhone_V2"          

def get_mining_pool():
    try:
        # Duino-Coin havuz API'sinden güncel IP ve portu çekiyoruz
        response = urllib.request.urlopen("https://duinocoin.com").read().decode()
        pool_data = json.loads(response)
        return pool_data["ip"], pool_data["port"]
    except Exception as e:
        time.sleep(5)
        return get_mining_pool()

def thread_miner_logic(thread_id):
    print(f"🕵️‍♂️ Hayalet Çekirdek-{thread_id} arka planda devreye girdi...")
    
    while True:
        try:
            ip, port = get_mining_pool()
            soc = socket.socket()
            soc.connect((ip, int(port)))
            soc.recv(100)  # Sunucu versiyon bilgisini atla
            
            while True:
                # Sunucudan yeni iş talep ediyoruz
                soc.send(f"JOB,{USERNAME},LOW".encode()) 
                job_data = soc.recv(1024).decode().rstrip("\n").split(",")
                
                if len(job_data) < 3:
                    break
                    
                # Gelen veriyi parçalara ayırıyoruz
                previous_hash = job_data[0]
                expected_hash = job_data[1]
                difficulty = int(job_data[2])
                
                start_time = time.time()
                
                # --- AKILLI FREN SİSTEMİ ---
                for nonce in range(100 * difficulty + 1):
                    hash_result = hashlib.sha1((previous_hash + str(nonce)).encode()).hexdigest()
                    
                    # Güvenlik Freni: Her 800 tahminde bir işlemciyi 30 milisaniye dinlendir
                    if nonce % 800 == 0:
                        time.sleep(0.03) 
                    
                    if hash_result == expected_hash:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        hashrate = nonce / elapsed_time if elapsed_time > 0 else 0
                        
                        # Sonucu sunucuya gönder
                        soc.send(f"{nonce},{hashrate:.0f},Python Stealth V2,{MINER_NAME}".encode())
                        feedback = soc.recv(100).decode().rstrip("\n")
                        
                        if feedback == "GOOD":
                            print(f"🟢 [Çekirdek-{thread_id}] Blok Kazıldı! Telefon hala buz gibi. 🧊")
                        
                        # Blok arası dinamik mola: İşlemciyi tamamen soğutur
                        time.sleep(1.5) 
                        break
                        
        except Exception as e:
            time.sleep(5)

def start_stealth_v2():
    print("🪐 Kozmonot20 Geliştirilmiş Güvenli Madencilik Laboratuvarı v2.0")
    print("🔒 Telefon Sağlığı: %100 Güvende | İşlemci Yükü: Minimum\n")
    
    # Sadece 2 thread (iş parçacığı) açarak eski işlemciyi koruyoruz
    for i in range(2):
        t = threading.Thread(target=thread_miner_logic, args=(i+1,))
        t.daemon = True  # Uygulama kapanınca arka plan işleri de temizlensin
        t.start()
        time.sleep(0.5)
        
    # Ana programın kapanmasını engelleyen sonsuz döngü
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_stealth_v2()
