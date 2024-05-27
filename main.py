import hashlib
import datetime
import json
import os

TARGET_DIFFICULTY = "0000ffff00000000000000000000000000000000000000000000000000000000"
prev_hash_for_header = "0000111100000000000000000000000000000000000000000000000000000000"
folder_dir = r"D:\Visual_Code_Programes\Python\BlockChain\MasteringWeb3.0-Assignment--1-2024-main\mempool"

global data
data = []
txid = []
global data_len
data_len = 0

#loading json files from mempool
for filename in os.listdir(folder_dir):
     if filename.endswith('.json'):
         f = open(os.path.join(folder_dir , filename))
         data.append(json.load(f))
         txid.append(filename)
         data_len += 1
         f.close()

#Clearing the file if it had any input
with open("D:\Visual_Code_Programes\Python\BlockChain\output.txt", 'w') as  f:
    f.write("")
 
# My block class to handle each block
class block:
    # INIT method
    def __init__(self, data, prev_block_hash, merkel_root, tx_id_coin_based, tx_id_non_coin_based, block_name):
        self.block_name = block_name
        self.version = 1
        self.data = data
        self.prev_block_hash = prev_block_hash
        self.nonce = 0
        self.timestamp = datetime.datetime.now()
        self.merkel_root = merkel_root
        self.hash = self.Calculate_hash()

    #Method to calculate blocks hash
    def Calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.version).encode('utf-8') +
                   str(self.data).encode('utf-8') +                         
                   str(self.prev_block_hash).encode('utf-8') +
                   str(self.nonce).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.merkel_root).encode('utf-8'))
        return sha.hexdigest()
    #Method to mine block and output all required things in output.txt
    def mine_block(self, target_difficulty):
        while self.hash > target_difficulty:
            self.nonce += 1
            self.hash = self.Calculate_hash()


        file_path = "D:\Visual_Code_Programes\Python\BlockChain\output.txt"
        with open(file_path, 'a') as file:
            file.write(f"""{self.block_name}:
    {{    
        "version": {self.version},\n
        "previous_block_hash": {self.prev_block_hash},\n
        "merkle_root": {self.merkel_root},\n
        "timestamp": {self.timestamp},\n
        "difficulty_target": {TARGET_DIFFICULTY},\n
        "nonce": {self.nonce}\n
    }}\n""")
            if(len(tx_id_non_coin_based) != 0):
                file.write("Serialized Coinbase Transaction:")
                file.write("{{\n")
                for id in tx_id_non_coin_based:
                    file.write("        " + os.path.splitext(id)[0] + '\n')
                file.write("}}\n")

            if(len(tx_id_coin_based) != 0):
                file.write("Transaction IDs:\n")
                for id in tx_id_non_coin_based:
                    file.write("        " + os.path.splitext(id)[0] + '\n')
                for id in tx_id_coin_based:
                    file.write("        " + os.path.splitext(id)[0] + '\n')

#Acessing all the tx stored in data in a batch of 32 or less
for i in range(0, len(data), 32):
    j = min(32, len(data) - i)
    tx_data = []
    tx_id_coin_based = []
    tx_id_non_coin_based = []
    #segregating tx based on whether it is coin based or not 
    for l in range (0, j):
            tx_data.append(data[i + l])
            if data[i + l]['vin'][0]['is_coinbase'] == False:
                tx_id_coin_based.append(txid[i + l])
            else:
                tx_id_non_coin_based.append(txid[i + l])
    # Finding the merkel root
    while j != 0:
        for k in range(0, j, 2):
            sha = hashlib.sha256()
            if j - k == 1:
                sha.update( str(txid[k]).encode(('utf-8')))
                tx_data[k//2] = sha.hexdigest()
                continue
            sha.update( str(txid[k]).encode(('utf-8')) +
                        str(txid[k + 1]).encode(('utf-8')))   
            tx_data[k//2] = sha.hexdigest()
        j //= 2
    #Givning the block a name
    if(i == 0):
        block_name = "Block Header"
    else:
        block_name = "Block " + str(i // 32)
    #Actually creating a block
    block1 = block("Hello", prev_hash_for_header, tx_data[0], tx_id_coin_based, tx_id_non_coin_based, block_name)

    block1.mine_block(TARGET_DIFFICULTY)
    prev_hash_for_header = block1.hash