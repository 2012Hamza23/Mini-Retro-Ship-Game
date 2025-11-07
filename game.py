import pygame
import random
import time
import os
import sys # <--- BU KÜTÜPHANE ARTIK ZORUNLU!

# Pygame'i başlat
pygame.init()

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0) 
MAVI = (0, 0, 200)   
SARI = (255, 255, 0)

# Ekran boyutları
GENISLIK = 800
YUKSEKLIK = 600

# Ekranı oluştur
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Kanka'nın Macerası: Uzaylı Kod Avcısı")

# Durum Yönetimi
OYUN_DURUMU = "OYNANIYOR" 

# Gemi Ayarları
try:
    # 🌟 Görseli dosyanın yanından yüklüyoruz.
    gemi_resmi = pygame.image.load("gemi.png").convert_alpha() 
    gemi_resmi = pygame.transform.scale(gemi_resmi, (100, 100)) 

except Exception as e:
    # Eğer görsel yoksa, bu hata ile programı kapat
    print(f"HATA: 'gemi.png' dosyası bulunamadı. Lütfen dosyanın 'oyun.py' ile aynı klasörde olduğundan emin olun! Hata: {e}")
    time.sleep(5) 
    pygame.quit()
    sys.exit() # 🌟 DÜZELTME: Doğru ve hata vermeyecek kapatma komutu!

# Sabit Değerler (Oyunun Resetlenmesi için gereklidir)
ILK_Gemi_X = (GENISLIK - gemi_resmi.get_width()) // 2
ILK_Gemi_Y = YUKSEKLIK - gemi_resmi.get_height() - 10
ILK_CAN = 3
TEMEL_DUSMAN_HIZI = 3
ZORLUK_ARTIS_KAT_SAYISI = 0.05
ATES_COOLDOWN = 0.1
HASAR_BEKLEME_SURESI = 2

# Değişkenler (Sıfırlanması Gerekenler)
gemi_x = ILK_Gemi_X
gemi_y = ILK_Gemi_Y
gemi_hiz = 7 
dusmanlar = [] 
mermiler = [] 
puan = 0
can = ILK_CAN
son_ates_zamani = 0 
son_hasar_zamani = 0 
son_dusman_zamani = 0 
oyun_baslangic_zamani = time.time() 

# Font Ayarı
font = pygame.font.Font(None, 36) 
buyuk_font = pygame.font.Font(None, 74) 

# Düşman Oluşturma Fonksiyonu
def yeni_dusman_olustur():
    DUSMAN_BOYUT = 40
    x = random.randint(0, GENISLIK - DUSMAN_BOYUT)
    y = -DUSMAN_BOYUT 
    yeni_dusman = pygame.Rect(x, y, DUSMAN_BOYUT, DUSMAN_BOYUT)
    dusmanlar.append(yeni_dusman)

# Mermi Oluşturma Fonksiyonu
def mermi_at():
    global son_ates_zamani
    simdiki_zaman = time.time()
    
    if simdiki_zaman - son_ates_zamani > ATES_COOLDOWN:
        MERMI_GENISLIK = 5
        MERMI_YUKSEKLIK = 15
        x = gemi_x + gemi_resmi.get_width() // 2 - MERMI_GENISLIK // 2 
        y = gemi_y 
        yeni_mermi = pygame.Rect(x, y, MERMI_GENISLIK, MERMI_YUKSEKLIK)
        mermiler.append(yeni_mermi)
        son_ates_zamani = simdiki_zaman

# Oyun Sıfırlama Fonksiyonu (Tekrar Oynatmak için)
def oyunu_sifirla():
    global gemi_x, gemi_y, dusmanlar, mermiler, puan, can, son_ates_zamani, son_hasar_zamani, son_dusman_zamani, oyun_baslangic_zamani, OYUN_DURUMU
    
    gemi_x = ILK_Gemi_X
    gemi_y = ILK_Gemi_Y
    dusmanlar = []
    mermiler = []
    puan = 0
    can = ILK_CAN
    son_ates_zamani = 0
    son_hasar_zamani = 0
    son_dusman_zamani = 0
    oyun_baslangic_zamani = time.time()
    OYUN_DURUMU = "OYNANIYOR" 

# Oyun Bitti Ekranını Çizme Fonksiyonu
def oyun_bitti_ekrani(skor):
    metin_kaybettin = buyuk_font.render("KAYBETTİN", True, KIRMIZI)
    ekran.blit(metin_kaybettin, (GENISLIK // 2 - metin_kaybettin.get_width() // 2, YUKSEKLIK // 4))
    
    metin_skor = font.render(f"Skorun: {skor}", True, SARI)
    ekran.blit(metin_skor, (GENISLIK // 2 - metin_skor.get_width() // 2, YUKSEKLIK // 4 + 100))
    
    metin_tekrar = font.render("Tekrar oynamak için SPACE basın", True, BEYAZ)
    ekran.blit(metin_tekrar, (GENISLIK // 2 - metin_tekrar.get_width() // 2, YUKSEKLIK // 4 + 150))


# FPS (Kare Hızı) Ayarı
saat = pygame.time.Clock()
FPS = 60 

# Oyun döngüsü
calisiyor = True
while calisiyor:
    saat.tick(FPS)
    simdiki_zaman = time.time()

    # === OLAY KONTROLÜ (EVENTS) ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisiyor = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if OYUN_DURUMU == "OYUN_BITTI":
                    oyunu_sifirla()
                elif OYUN_DURUMU == "OYNANIYOR":
                    mermi_at()

    # === OYUN OYNANIYOR DURUMU ===
    if OYUN_DURUMU == "OYNANIYOR":
        
        # 1. HAREKET KONTROLÜ
        tuslar = pygame.key.get_pressed()
        if tuslar[pygame.K_LEFT] or tuslar[pygame.K_a]: gemi_x -= gemi_hiz
        if tuslar[pygame.K_RIGHT] or tuslar[pygame.K_d]: gemi_x += gemi_hiz
        if tuslar[pygame.K_UP] or tuslar[pygame.K_w]: gemi_y -= gemi_hiz
        if tuslar[pygame.K_DOWN] or tuslar[pygame.K_s]: gemi_y += gemi_hiz

        # Sınır Kontrolü
        if gemi_x < 0: gemi_x = 0
        if gemi_x > GENISLIK - gemi_resmi.get_width(): gemi_x = GENISLIK - gemi_resmi.get_width()
        if gemi_y < 0: gemi_y = 0
        if gemi_y > YUKSEKLIK - gemi_resmi.get_height(): gemi_y = YUKSEKLIK - gemi_resmi.get_height()

        # 2. MEKANİKLER VE GÜNCELLEMELER
        
        # Düşman hızını zamana göre artır (ZORLUK ARTIŞI)
        gecen_zaman = simdiki_zaman - oyun_baslangic_zamani
        DUSMAN_HIZI_GUNCEL = TEMEL_DUSMAN_HIZI + (gecen_zaman * ZORLUK_ARTIS_KAT_SAYISI)
        
        # Düşman Üretimi ve Hareketi
        MAKS_DUSMAN = 5 
        if len(dusmanlar) < MAKS_DUSMAN and simdiki_zaman - son_dusman_zamani > 1.5:
            yeni_dusman_olustur()
            son_dusman_zamani = simdiki_zaman

        for dusman in dusmanlar:
            dusman.y += DUSMAN_HIZI_GUNCEL 

        # Mermileri hareket ettir
        MERMI_HIZI = 10
        for mermi in mermiler:
            mermi.y -= MERMI_HIZI 

        # Çarpışma Tespiti (Mermi ve Düşman)
        vurulan_dusmanlar = [] 
        vurulan_mermiler = [] 

        for mermi in mermiler:
            for dusman in dusmanlar:
                if mermi.colliderect(dusman):
                    vurulan_dusmanlar.append(dusman)
                    vurulan_mermiler.append(mermi)
                    puan += 20 
                    break 

        # Çarpışma Tespiti (Gemi ve Düşman) HASAR ALMA
        gemi_rect = pygame.Rect(gemi_x, gemi_y, gemi_resmi.get_width() * 0.8, gemi_resmi.get_height() * 0.8)
        
        if simdiki_zaman - son_hasar_zamani > HASAR_BEKLEME_SURESI:
            for dusman in dusmanlar:
                if gemi_rect.colliderect(dusman):
                    can -= 1 # Canı 1 azalt
                    
                    vurulan_dusmanlar.append(dusman)
                    son_hasar_zamani = simdiki_zaman
                    gemi_y -= 20 
                    break 

        # Listeden silme işlemleri
        for dusman in vurulan_dusmanlar:
            if dusman in dusmanlar:
                dusmanlar.remove(dusman)

        for mermi in vurulan_mermiler:
            if mermi in mermiler:
                mermiler.remove(mermi)

        # Sınır dışına çıkan mermileri ve düşmanları sil
        dusmanlar = [d for d in dusmanlar if d.top < YUKSEKLIK] 
        mermiler = [m for m in mermiler if m.bottom > 0] 

        # OYUN BİTTİ KONTROLÜ
        if can <= 0:
            OYUN_DURUMU = "OYUN_BITTI" 

    # === ÇİZİM KISMI ===
    ekran.fill(SIYAH) 

    if OYUN_DURUMU == "OYNANIYOR":
        
        # Dokunulmazlık göstergesi
        if simdiki_zaman - son_hasar_zamani < HASAR_BEKLEME_SURESI:
            pygame.draw.rect(ekran, KIRMIZI, gemi_rect, 3) 
            
        ekran.blit(gemi_resmi, (gemi_x, gemi_y))

        for dusman in dusmanlar:
            pygame.draw.rect(ekran, MAVI, dusman) 
        
        for mermi in mermiler:
            pygame.draw.rect(ekran, KIRMIZI, mermi)
        
        # Puanı ve Canı Ekrana Yazma
        puan_metni = font.render(f"Skor: {puan}", True, BEYAZ) 
        ekran.blit(puan_metni, (10, 10)) 
        
        can_metni = font.render(f"Can: {can}", True, BEYAZ) 
        ekran.blit(can_metni, (10, 50)) 
    
    elif OYUN_DURUMU == "OYUN_BITTI":
        oyun_bitti_ekrani(puan)

    # Ekranı güncelle
    pygame.display.flip()

# Pygame'i kapat
pygame.quit()