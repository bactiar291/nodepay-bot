lets go
# semoga bermanfaat
# nodepay-bot
# utamakan gitpull dan baca readme.md sebelum run 
jika proxy yang kalian pakai mengalami kegagalan maka otomatis akan di coba berulang selama 3 kali limit, jika masih tidak bisa otomatis proxy akan di hapus dari daftar, sc ini di buat sedemikian rupa agar menangani error pada proxy yang sering terjadi
# Mendapatkan NP_TOKEN atau user.txt
Buka tautan ini dan masuk ke akun Anda: https://app.nodepay.ai/register?ref=5TfDbxk0YrmC4PU
Tekan F12 pada halaman untuk membuka konsol, atau tekan Ctrl + Shift + I untuk membuka Developer Tools (Alat Pengembang).
Di konsol, ketik kode berikut:
```bash
localStorage.getItem('np_token');
```
NP_TOKEN akan muncul di konsol setelah Anda menekan Enter. Teks yang tercetak di konsol adalah NP_TOKEN Anda.
![Screenshot](https://raw.githubusercontent.com/bactiar291/nodepay-bot/main/ss.png)


# contoh jika berhasil konek
```bash
INFO    | __main__:ping:106 - Ping successful via proxy http://username:password@198.23.239.134:6540: {'code': 0, 'message': 'Ping successful'}
INFO    | __main__:render_profile_info:75 - Account info loaded successfully for proxy http://username:password@198.23.239.134:6540
INFO    | __main__:start_ping:91 - Ping started for proxy http://username:password@198.23.239.134:6540
INFO    | __main__:ping:106 - Ping successful via proxy http://username:password@198.23.239.134:6540: {'code': 0, 'message': 'Ping successful'}
INFO    | __main__:render_profile_info:75 - Profile information for proxy http://username:password@198.23.239.134:6540: UID: 1234567
```
# contoh jika gagal 
```bash
ERROR   | __main__:call_api:89 - Error during API call with proxy http://username:password@198.23.239.134:6540: ConnectionError('Failed to establish a new connection')
ERROR   | __main__:ping:124 - Ping failed via proxy http://username:password@198.23.239.134:6540: ConnectionError('Failed to establish a new connection')
ERROR   | __main__:render_profile_info:72 - Error in render_profile_info for proxy http://username:password@198.23.239.134:6540: ProxyError('Cannot connect to proxy.', OSError('Tunnel connection failed: 502 Bad Gateway'))
INFO    | __main__:ping:126 - Proxy http://username:password@198.23.239.134:6540 failed after 3 retries. Removing proxy from list.
```

# untuk proses instalasi ikuti instruksi dibawah ini :

```bash
git clone https://github.com/bactiar291/nodepay-bot.git
cd nodepay-bot
```
```bash
pip install -r requirements.txt
```
jika gagal bisa pakai 
```bash
python -m pip install -r requirements.txt
```
jika sudah isi user.txt dan proxy.txt nya sesuai instruksi diatas 
selanjunya 
jalankan dengan perintah :

```bash
python3 nodepay.py
```
done bang 
semoga bermanfaat 

# license 
MIT
