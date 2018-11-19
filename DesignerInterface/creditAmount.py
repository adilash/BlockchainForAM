from solc import compile_source
from web3 import Web3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from contract_source import contract_sc

provider = Web3.IPCProvider(os.path.join(os.path.dirname(__file__), '../DesignNode/geth.ipc'))
w3 = Web3(provider)


compiled_sol = compile_source(contract_sc)
contract_interface = compiled_sol['<stdin>:Agreement']

w3.eth.defaultAccount = w3.eth.accounts[0]

contractAddress = input("Enter contract address: ")
contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

credit_amount = input("Enter credit amount: ")
credit_amount = int(credit_amount)

passphrase = input("Enter passphrase: ")
w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

Agreement = w3.eth.contract(
    address=contractAddress,
    abi=contract_interface['abi'],
)

try:
    tx_hash = Agreement.fallback().transact({'value': credit_amount})

except ValueError:
    print("Unauthorized or insufficient credit amount")
    exit(0)

print("Waiting for transaction to be mined...")
w3.eth.waitForTransactionReceipt(tx_hash)

print("Amount credited successfully!!")
print("Transaction hash: ", Web3.toHex(tx_hash))