from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account
from loguru import logger
import csv

try:
    user_input = input("Введите количество генерируемых кошельков: ").strip()
    if not user_input:
        raise ValueError("Количество кошельков не может быть пустым.")
    num_accounts = int(user_input)
    if num_accounts <= 0:
        raise ValueError("Количество кошельков должно быть положительным числом.")
except ValueError as e:
    logger.error(f"Ошибка ввода: {e}")
    exit(1)

def generate_erc20(num_accounts):
    addresses = []
    private_keys = []
    mnemonics = []
    for i in range(num_accounts):
        try:
            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
            seed = Bip39SeedGenerator(mnemonic).Generate()
            bip_obj = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
            private_key = bip_obj.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PrivateKey().Raw().ToBytes()
            account = Account.from_key(private_key)
            private_keys.append(account._private_key.hex())
            addresses.append(account.address)
            mnemonics.append(mnemonic)
            logger.info(f"✅ Кошелек {i+1}/{num_accounts} успешно сгенерирован.")
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации кошелька {i+1}: {e}")
            continue
    return private_keys, addresses, mnemonics

try:
    private_keys, addresses, mnemonics = generate_erc20(num_accounts)
    
    with open('wallets.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'PrivateKey', 'Mnemonic'])
        for address, private_key, mnemonic in zip(addresses, private_keys, mnemonics):
            writer.writerow([address, private_key, mnemonic])
    
    logger.success(f"✅ Генерация завершена! Сохранено {len(addresses)} кошельков в wallets.csv")
except Exception as e:
    logger.critical(f"❌ Критическая ошибка: {e}")
