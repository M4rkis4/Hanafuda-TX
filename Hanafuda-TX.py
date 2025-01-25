import random
import time
from web3 import Web3
from dotenv import load_dotenv
import os

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Konfigurasi koneksi ke jaringan BASE
BASE_RPC_URL = ("https://mainnet.base.org")
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# Alamat contract
CONTRACT_ADDRESS = "0xC5bf05cD32a14BFfb705Fb37a9d218895187376c"

# Wallet pengirim
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Fungsi untuk mengirim transaksi
def send_transaction():
    try:
        # Jumlah acak antara 0.000000001 dan 0.000000002
        value = random.uniform(0.000000001, 0.000000002)

        # Konversi jumlah ke wei (BASE menggunakan 18 desimal seperti Ethereum)
        value_in_wei = web3.toWei(value, "ether")

        # Dapatkan nonce untuk transaksi
        nonce = web3.eth.getTransactionCount(SENDER_ADDRESS)

        # Buat transaksi
        transaction = {
            "to": CONTRACT_ADDRESS,
            "value": value_in_wei,
            "gas": 21000,  # Gas standar untuk transfer
            "gasPrice": web3.toWei("10", "gwei"),  # Gas price (dapat disesuaikan)
            "nonce": nonce,
            "chainId": 8453,  # Chain ID untuk BASE mainnet
        }

        # Tanda tangani transaksi
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)

        # Kirim transaksi
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        print(f"Transaksi berhasil dikirim! Hash: {web3.toHex(tx_hash)}")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim transaksi: {e}")

# Looping setiap 30 detik
while True:
    print("Mengirim transaksi...")
    send_transaction()
    print("Menunggu 30 detik sebelum transaksi berikutnya...")
    time.sleep(30)
