import os, requests, subprocess
import time
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_KEY=os.environ.get('TELEGRAM_KEY')

CHAT_IDS = os.environ.get('CHAT_IDS').split(",")
INTERVAL = int(os.environ.get('INTERVAL'))

URL = f"https://api.telegram.org/bot{TELEGRAM_KEY}/sendMessage"

SERVICE = os.environ.get('SERVICE')

def send(text):
    for chat_id in CHAT_IDS:
        requests.get(URL, {'chat_id': chat_id, 'disable_web_page_preview': 1, 'parse_mode': 'HTML', 'text': text})

def format_log(log):
    formatted_log = log.replace('homie ', '')
    return f'<code>{formatted_log}</code>'


if __name__ == "__main__":
    print("Telegram Logger Started.")
    start_time = time.time()
    runtime = 0
    while True:
        time.sleep(INTERVAL)
        output = subprocess.Popen(["journalctl", "--since", f"{INTERVAL + runtime} seconds ago", "-u", f"{SERVICE}.service"], stdout=subprocess.PIPE).stdout.read()
        
        iteration_start = time.time()
        output = str(output, 'utf-8')
        cropped = output.split("\n")
        runtime = 0
        if '-- No entries --' in cropped: continue
        for log in cropped:
            if log.__contains__('Logs begin at') or log == '': continue
            send(format_log(log))
        iteration_end = time.time()
        runtime = round(iteration_end - iteration_start, 2)