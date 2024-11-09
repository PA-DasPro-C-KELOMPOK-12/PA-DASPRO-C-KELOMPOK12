import prettytable
import json
import re
from pwinput import pwinput

json_path = "D:\\KULIAH\\Praktikum ddp\\PA DASPRO\\user.json"
json_barang = "D:\\KULIAH\\Praktikum ddp\\PA DASPRO\\barang.json"


def validasi_username_password(input_str):
    if len(input_str) > 30:
        return False
    if not re.match("^[a-zA-Z0-9]*$", input_str):  # hanya huruf dan angka
        return False
    return True

def user_load():
    with open(json_path, "r") as file:
        data = json.load(file)
    return data

def user_save(data):
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)

def barang_load():
    with open(json_barang, "r") as file:
        data = json.load(file)
    return data

def barang_save(data):
    with open(json_barang, "w") as file:
        json.dump(data, file, indent=4)

penggunaterdaftar = {
    "admin": {"password": "lucky", "role": "admin"},
}
penggunalogin = {}

stock_barang = {
}

def menu_utama():
    try:
        while True:
            print('\nSelamat datang di Supermarket DasPro')
            print('1. Register')
            print('2. Login')
            print('3. Keluar')
            choice = input("Pilih menu (1 untuk Register, 2 untuk Login, 3 untuk Keluar): ")
            
            if choice == '1':
                register()
            elif choice == '2':
                login()
            elif choice == '3':
                print("Terima kasih telah menggunakan Supermarket DasPro. Sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
    except (KeyboardInterrupt, ValueError):
        print("\nOperasi dibatalkan.")

def register():
    try:
        load = user_load()
        while True:
            username = input("Username: ")
            if len(username) > 30:
                print("Username maksimal 30 karakter. Silakan coba lagi.")
            elif not validasi_username_password(username):
                print("Username hanya boleh mengandung huruf dan angka.")
            elif any(x['username'] == username for x in load):
                print('Username sudah terdaftar. Silahkan login.')
            else:
                break
        
        while True:
            password = pwinput("Password:", "*")
            if len(password) > 30:
                print("Password maksimal 30 karakter. Silakan coba lagi.")
            elif not validasi_username_password(password):
                print("Password hanya boleh mengandung huruf dan angka.")
            else:
                break
        
        akun = {
            "username": username,
            "password": password,
            "saldo": 0
        }
        load.append(akun)
        user_save(load)
        print("Registrasi berhasil! Silakan login.")
        login()
    except KeyboardInterrupt:
        print('Register dibatalkan')

def login():
    try:
        global penggunalogin
        while True:
            print("\nPilih login sebagai:")
            print("1. Admin")
            print("2. User")
            role_choice = input("Masukkan pilihan (1 untuk Admin, 2 untuk User): ")

            if role_choice == "1":
                role = "admin"
            elif role_choice == "2":
                role = "user"
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                continue
            
            while True:
                username = input("Username: ")
                if len(username) > 30:
                    print("Username maksimal 30 karakter. Silakan coba lagi.")
                elif not validasi_username_password(username):
                    print("Username hanya boleh mengandung huruf dan angka.")
                else:
                    break

            while True:
                password = pwinput("Password:", "*")
                if len(password) > 30:
                    print("Password maksimal 30 karakter. Silakan coba lagi.")
                elif not validasi_username_password(password):
                    print("Password hanya boleh mengandung huruf dan angka.")
                else:
                    break

            if role == "admin" and username in penggunaterdaftar and penggunaterdaftar[username]['password'] == password:
                penggunalogin = {'username': username, 'role': "admin"}
                print(f'\nAnda berhasil login sebagai Admin: {username}')
                menu_admin()
                break

            elif role == "user":
                users = user_load()
                user = next((user for user in users if user['username'] == username and user['password'] == password), None)
                if user:
                    penggunalogin = {'username': username, 'role': "user"}
                    print(f'\nAnda berhasil login sebagai User: {username}')
                    menu_user()
                    break
                else:
                    print("Username atau password salah. Silakan coba lagi.")
            else:
                print("Gagal login sebagai Admin. Silakan coba lagi.")
    except KeyboardInterrupt:
        print('Login dibatalkan')

def menu_admin():
    try: 
        while True:  
            
                print("1. tambah stok")
                print("2. Hapus stok")
                print("3. Lihat stok")
                print("4. Update stok (tambah barang baru)")
                print("5. Kembali")
                pilih = int(input("Masukkan pilihan: "))
                if pilih == 1:
                    tambah_stok()
                elif pilih == 2:
                    hapus_stok()
                elif pilih == 3:
                    lihat_stok()
                elif pilih == 4:
                    update_stok()
                elif pilih == 5:
                    menu_utama()
                    break  
                else:
                    print("Pilihan tidak ada.")
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")

def tambah_stok():
    try:
        stock_barang = barang_load()  
        nama_barang = input("Masukkan nama barang: ").lower()
        jumlah_stok = int(input("Masukkan jumlah stok: "))
        harga = int(input("Masukkan harga per satuan: "))        
        if nama_barang in stock_barang:
            stock_barang[nama_barang]["stok"] += jumlah_stok
            stock_barang[nama_barang]["harga"] = harga
        else:
            stock_barang[nama_barang] = {"stok": jumlah_stok, "harga": harga}
            barang_save(stock_barang)  

        print(f'Stok dan harga {nama_barang.capitalize()} berhasil diperbarui.')
        menu_admin()
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")

def update_stok():
    try:
        stock_barang = barang_load()
        nama_barang = input("Masukkan nama barang baru: ").lower()
        if nama_barang in stock_barang:
            print(f"{nama_barang.capitalize()} sudah ada di daftar stok.")
            return
        stok = int(input("Masukkan jumlah stok: "))
        harga = int(input("Masukkan harga per satuan: "))
        stock_barang[nama_barang] = {"stok": stok, "harga": harga}
        barang_save(stock_barang)
        print(f"{nama_barang.capitalize()} berhasil ditambahkan ke stok.")
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")

def hapus_stok():
    try:
        stock_barang = barang_load()
        input_hapus = input("Masukkan nama barang yang ingin dihapus: ").lower()
        if input_hapus not in stock_barang:
            print(f"{input_hapus.capitalize()} tidak ditemukan dalam daftar stok.")
            return
        item = input_hapus
        jumlah_hapus = int(input(f"Berapa banyak stok {item.capitalize()} yang ingin dihapus? "))
        if jumlah_hapus > stock_barang[item]["stok"]:
            print(f"Tidak cukup stok {item.capitalize()} untuk dihapus.")
            return
        if konfirmasi_hapus := input(f"Apakah Anda yakin ingin menghapus {jumlah_hapus} stok {item.capitalize()}? (y/n): ").lower() == 'y':
            stock_barang[item]["stok"] -= jumlah_hapus
        elif jumlah_hapus <= 0:
            print("Jumlah yang dihapus harus lebih dari 0.")
            return
        
        stock_barang[item]["stok"] -= jumlah_hapus
        if stock_barang[item]["stok"] == 0:
            confirm = input(f"Stok {item.capitalize()} habis. Apakah Anda ingin menghapus barang ini dari daftar? (y/n): ")
            if confirm.lower() == 'y':
                del stock_barang[item]
                print(f"{item.capitalize()} berhasil dihapus dari daftar barang.")
        
        barang_save(stock_barang)

        print(f"{jumlah_hapus} stok {item.capitalize()} berhasil dihapus.")
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")

def lihat_stok():
    try:
        stock_barang = barang_load()
        table = prettytable.PrettyTable(["Barang", "Stok", "Harga"])
        for item, details in stock_barang.items():
            table.add_row([item.capitalize(), details["stok"], details["harga"]])
        print(table)
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan.")

def menu_user():
    while True:
        try:
            print("1. Pesan")
            print("2. Top up saldo")
            print("3. Lihat saldo")
            print("4. Search")
            print("5. Sorting harga")
            print("6. Kembali")
            pilih = int(input("Masukkan pilihan: "))
            if pilih == 1:
                pesan()
            elif pilih == 2:
                top_up()
            elif pilih == 3:
                lihat_saldo()
            elif pilih == 4:
                search()
            elif pilih == 5:
                sort_harga()
            elif pilih == 6:
                menu_utama()
                break
            else:
                print("Pilihan tidak ada.")
        except ValueError:
            print("Input salah. Masukkan angka 1-7.")
        except KeyboardInterrupt:
            print("\nOperasi dibatalkan.")

def pesan():
    try:
        stock_barang = barang_load()
        table = prettytable.PrettyTable(["Barang", "Harga"])
        for item, details in stock_barang.items():
            table.add_row([item.capitalize(), details["harga"]])
        print(table)
        
        stock_barang = barang_load()
        users = user_load()
        username = penggunalogin['username']
        user = next((user for user in users if user['username'] == username), None)
        if not user:
            print("Pengguna tidak ditemukan.")
            return
        input_pesan = input("Masukkan nama barang yang ingin dipesan: ").lower()
        if input_pesan not in stock_barang:
            print(f"{input_pesan.capitalize()} tidak ditemukan dalam daftar stok.")
            return
        if stock_barang[input_pesan]["stok"] == 0:
            print(f"Stok {input_pesan.capitalize()} habis.")
            return
        jumlah_pesan = int(input(f"Berapa banyak {input_pesan.capitalize()} yang ingin dipesan? "))
        if jumlah_pesan > stock_barang[input_pesan]["stok"]:
            print(f"Tidak cukup stok {input_pesan.capitalize()} untuk dipesan.")
            return
        total_harga = stock_barang[input_pesan]["harga"] * jumlah_pesan
        if user['saldo'] < total_harga:
            print("Saldo tidak mencukupi untuk melakukan pemesanan ini.")
            return
        if input(f"Total harga adalah Rp{total_harga}. Konfirmasi pemesanan? (y/n): ").lower() == 'y':
            user['saldo'] -= total_harga
            stock_barang[input_pesan]["stok"] -= jumlah_pesan
            user_save(users)
            barang_save(stock_barang)
            print(f"Pesanan {jumlah_pesan} {input_pesan.capitalize()} berhasil. Saldo Anda sekarang adalah Rp{user['saldo']}.")
        else:
            print("Pesanan dibatalkan.")
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")
        
def lihat_saldo():
    try:
        users = user_load()
        username = penggunalogin['username']
        user = next((user for user in users if user['username'] == username), None)
        if user:
            print(f"Saldo Anda saat ini adalah Rp{user['saldo']}.")
        else:
            print("Pengguna tidak ditemukan.")
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan.")

def top_up():
    try:
        users = user_load()
        username = penggunalogin['username']
        user = next((user for user in users if user['username'] == username), None)
        if user:
            input_top_up = int(input("Masukkan nominal saldo yang ingin ditambahkan: "))
            user['saldo'] += input_top_up
            user_save(users)
            print(f"Saldo Anda berhasil ditambahkan sebesar Rp{input_top_up}. Saldo saat ini adalah Rp{user['saldo']}.")
        else:
            print("Pengguna tidak ditemukan.")
        
    except (ValueError, KeyboardInterrupt):
        print("Input salah atau operasi dibatalkan.")

def search():
    try:
        barang = barang_load()
        nama_barang = input("Masukkan nama barang yang dicari: ").lower()
        if nama_barang in barang:
            print(f"{nama_barang.capitalize()} ditemukan dengan harga Rp{barang[nama_barang]['harga']}.")
        else:
            print(f"{nama_barang.capitalize()} tidak ditemukan dalam stok.")
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan.")

def sort_harga():
    try:
        barang = barang_load()
        sorted_barang = sorted(barang.items(), key=lambda x: x[1]["harga"])
        print("Barang urut berdasarkan harga:")
        for item, details in sorted_barang:
            print(f"{item.capitalize()}: Rp{details['harga']}")
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan.")

menu_utama()