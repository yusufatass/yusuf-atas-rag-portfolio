# Streamlit uygulamasını güvenli bir şekilde yeniden başlatır.
# Önce varsa asılı kalmış Python işlemlerini temizler, sonra uygulamayı başlatır.

Write-Host "Uygulama hazırlanıyor... Eski oturumlar temizleniyor." -ForegroundColor Cyan

# Varsa eski python süreçlerini zorla durdur
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Portun boşalması için kısa bir süre bekle
Start-Sleep -Seconds 1

Write-Host "Başlatılıyor: Yusuf Ataş | AI Kariyer Asistanı" -ForegroundColor Green
streamlit run app.py
