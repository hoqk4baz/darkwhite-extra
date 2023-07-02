from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import os
import time
import requests
import subprocess

# [x]: Reddedildi [!]: Hata [*]: Ilerleme [+]: Basarili islem [-]: Basarisiz islem

subprocess.run(['clear'])

client = MongoClient("mongodb+srv://hoqk4baz:zsezsert55@cluster0.rvpzndm.mongodb.net/hoqk4baz?retryWrites=true&w=majority") #mongodb adresim
db = client["dwextra"]  # Veritabanını seçin
kullanicilar = db["kullanicilar"]  # Koleksiyonu seçin

#bot_baglanti = Client("turannsplayground", api_id = "22797267", api_hash = "d130fc53a7dc465bdb307c3e3fde9978", bot_token = "6025751117:AAFgaTq1v6tamifpeIDrwPxUIrKKglkfETk") # https://t.me/signer_beta_test_bot
bot_baglanti = Client("dwextra", api_id = "27149351", api_hash = "2edf2bdf7cb587effd7dc089f1989cb5", bot_token = "6002267061:AAHjDhdCETuf-bjrCByHdWl9I4hEudyg_YQ") # https://t.me/FavourSigner_bot

#/start mesajı 
yonetici_listesi = ["5826900952"]

#---------------------------------------
# Kullanıcı ekle: `/ekle 12345678`
# Kullanıcı sil: `/sil 12345678`
#---------------------------------------

def is_admin(user):
    return str(user.id) in yonetici_listesi

@bot_baglanti.on_message(filters.private & filters.command("start"))
def baslatan_kullanici(client, message):
    user_id = str(message.from_user.id)

    # Kullanıcı kaydını kontrol et
    kullanici = kullanicilar.find_one({"kullanici_id": user_id})
    if kullanici is None:
        # Kaydedilmemiş kullanıcıya mesaj gönder
        unregistered_user_text = f"Merhaba, {message.from_user.first_name}!\n😞Üzgünüm Kayıtlı Değilsin\nBot Kullanım Ücreti Aylık 10TL\nÖdeme Ve Bot Kullanımı İçin Admine Ulaşın."
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("☬𝐃𝐀𝐑𝐊 | 𝐄𝐍𝐙𝐀☬", url="https://t.me/dark_enza")],
            ]
        )
        print(f"[x]: {user_id} Kullanıcı kayıtlı değil")
        message.reply_text(unregistered_user_text, reply_markup=keyboard)
            
    else:
        user_name = message.from_user.first_name # Hoşgeldin mesajı
        welcome_text = f"Merhaba! {user_name}\nBol Kullanımlar Dilerim."

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Menu", callback_data="menu")],
                [InlineKeyboardButton("Hakkında", callback_data="hakkinda")],
            ]
        )

        message.reply_text(welcome_text, reply_markup=keyboard)


@bot_baglanti.on_message(filters.private & filters.command("ekle"))
def ekle_kullanici(client, message):
    user = message.from_user

    if is_admin(user):
        command_parts = message.text.split(" ")

        if len(command_parts) == 2:
            new_user_id = command_parts[1]

            kullanici = { "kullanici_id": new_user_id, } # Kullanıcıyı kaydet
            kullanicilar.update_one({"kullanici_id": new_user_id}, {"$set": kullanici}, upsert=True)
            message.reply_text(f"Kullanıcı {new_user_id} başarıyla eklendi.")
            print("[+]: Yeni kullanıcı kaydı başarılı.")
            bot_baglanti.send_message(new_user_id, "Selam Dostum, Artık Botumuzu kullanabilirsin.")             # Kullanıcıya kayit edildiginin haberini ver
        else:
            message.reply_text("Hatalı komut kullanımı. Ornek: /ekle <kullanıcı_id>")
    else:
        message.reply_text("Üzgünüm, sadece yöneticiler tarafından kullanıcı eklenebilir.")

@bot_baglanti.on_message(filters.private & filters.command("sil"))
def sil_kullanici(client, message):
    user = message.from_user

    if is_admin(user):
        command_parts = message.text.split(" ")

        if len(command_parts) == 2:
            delete_user_id = command_parts[1]

            # Kullanıcı sil
            result = kullanicilar.delete_one({"kullanici_id": delete_user_id})

            if result.deleted_count > 0:
                message.reply_text(f"Kullanıcı {delete_user_id} başarıyla silindi.")
                print("[+]: Kullanıcı kaydı silindi.")
                bot_baglanti.send_message(delete_user_id, "Üzgünüm Dostum, Kullanımın yasaklandı.")
            else:
                message.reply_text(f"Kullanıcı {delete_user_id} zaten kayıtlı değil.")
        else:
            message.reply_text("Hatalı komut kullanımı. Ornek: /sil <kullanıcı_id>")
    else:
        message.reply_text("Üzgünüm, bu komutu yalnızca yöneticiler kullanabilir.")
bot_baglanti.run()
