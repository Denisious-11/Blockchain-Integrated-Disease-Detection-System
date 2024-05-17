import random
import sys
import base64
import json
import os
import pandas as pd
from web3 import Web3
from solcx import compile_standard
# from ipfs import upload as up1
import ipfshttpclient
import solcx
#solcx.install_solc()

compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "phb.sol": {
             "content": '''
                 pragma solidity >=0.4.0 <0.8.16;
               

                contract PHB {

                    struct Patient
                    {            
                        int user_id;
                        string username;
                        string password;
                        string mobile;
                        string p_address;
                    }

                    Patient []pts;

                    function addPatient(int user_id,string memory username,string memory password,string memory mobile,string memory p_address) public
                    {
                        Patient memory e
                            =Patient(user_id,
                                    username,
                                    password,
                                    mobile,
                                    p_address);
                        pts.push(e);
                    }

                    function getPatient(int user_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<pts.length;i++)
                        {
                            Patient memory e
                                =pts[i];
                            
                            if(e.user_id==user_id)
                            {
                                return(e.username,
                                    e.password,
                                    e.mobile,
                                    e.p_address
                                   
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getPatientCount() public view returns(uint256)
                    {
                        return(pts.length);
                    }


                    struct Record
                    {
       
                        int r_id;
                        string username;
                        string c_date;
                        string c_time;
                        string result;
                    }

                    Record []rcd;

                    function addRecord(int r_id,string memory username,string memory c_date,string memory c_time,string memory result) public
                    {
                        Record memory e
                            =Record(r_id,
                                    username,
                                    c_date,
                                    c_time,
                                    result);
                        rcd.push(e);
                    }


                    function getRecord(int r_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<rcd.length;i++)
                        {
                            Record memory e
                                =rcd[i];
                                 
                            
                            if(e.r_id==r_id)
                            {
                                return(e.username,
                                    e.c_date,
                                    e.c_time,
                                    e.result
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }

                    function getRecordCount() public view returns(uint256)
                    {
                        return(rcd.length);
                    }

                }

               '''
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
 })


# web3.py instance



def verify_key(adr1,key,amount):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr1,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        #print(web3.toHex(tx_hash))
        return "Yes"
    except Exception as e:
        print(e)  
        return "No"  



def create_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # get bytecode
    bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    pb = w3.eth.contract(abi=abi, bytecode=bytecode)

    # # Submit the transaction that deploys the contract
    tx_hash = pb.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print("tx_receipt.contractAddress: ",tx_receipt.contractAddress)
    f=open('contract_address.txt','w')
    f.write(tx_receipt.contractAddress)
    f.close()


def add_patient1(user_id,username,password,mobile,p_address):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addPatient(user_id,username,password,mobile,p_address).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_patient(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getPatient(id1).call()
    print("store : ",store)
    return store

def get_patients():
    c=get_patient_count()
    c_names=['username','password','mobile','p_address']
    dict1={}
    for i in range(1,c+1):
        d=get_patient(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_patient_count():
    p1=get_contract()
    store = p1.functions.getPatientCount().call()
    print(store)
    return int(store)


def get_record(id1):
    id1=int(id1)
    p1=get_contract()
    print(id1,'============')
    store = p1.functions.getRecord(id1).call()
    print(store)
    return store

def get_records():
    c=get_record_count()
    c_names=['username','c_date','c_time','result']
    dict1={}
    for i in range(1,c+1):
        d=get_record(i)
        dict2={}
        for j in range(len(c_names)):
            # if j==5:
            #     dict2[c_names[j]]=d[7]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1     


def get_record_count():
    p1=get_contract()
    store = p1.functions.getRecordCount().call()
    print(store)
    return int(store)
    

def add_record1(r_id,username,c_date,c_time,result):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    # c=get_patient_count()+1
    tx_hash = p1.functions.addRecord(r_id,username,c_date,c_time,result).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)

##############################

def get_contract():
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]#'0x3529A6ee990639C32bEe5F841a9649cdd0c6e0FD'
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    return p1



def verify_adr(s):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    adrs = w3.eth.accounts
    print(adrs)

    if s in adrs:
        return True
    else:
        return False  



def bverify_transaction(tx):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvi
    x=w3.eth.getTransaction(tx)
    print(x)
    if x==None:
        print('Fake')
        return False
    else:
        print('Real')
        return True


###################

def transfer(adr1,adr2,key,amount,sender_name,receiver_name,title):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr2, #artist_address
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        generated_hash=web3.toHex(tx_hash)
        print("generated_hash : ",generated_hash)
        return generated_hash

    except Exception as e:
        print(e)  
        return False


if __name__=="__main__":
    pass

    # create_contract()




