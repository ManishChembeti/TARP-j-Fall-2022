from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import json
from web3 import Web3, HTTPProvider
import time

global details
details=''
global contract

def readDetails():
    global details
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'IndustrialEquipmentContract.json' #industrial contract code
    deployed_contract_address = '0x53E86569FD8C0e4DCFf2FBA266E340e0a1cA0Fa4' #hash address to access industrail contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    details = contract.functions.getData().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

def saveDataBlockChain(currentData):
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'IndustrialEquipmentContract.json'
    deployed_contract_address = '0x53E86569FD8C0e4DCFf2FBA266E340e0a1cA0Fa4'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails()
    details+=currentData
    msg = contract.functions.setData(details).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def getDetails():
    global details
    readDetails()
    print("p det "+details)
    arr = details.split("\n")
    output = ''
    font = "<font size=3 color=black>"
    for i in range(len(arr)):
        data = arr[i].split("$")
        if data[0] == 'ProductionDetails':
            output+='<tr><td>'+font+data[1]+'</td><td>'+font+data[2]+'</td><td>'+font+data[3]+'</td><td>'+font+data[4]+'</td><td>'
            output+=font+data[5]+'</td><td>'+font+data[6]+'</td><td>'
            output+='<img src=/static/products/'+data[1]+'.png height=100 width=100/></td></tr>'
    output+='</table><br/><br/><table align=center border=1><tr><th>Equipment ID or Code</th><th>Location Details</th><th>Location Date</th></tr>'
    for i in range(len(arr)):
        data = arr[i].split("$")
        if data[0] == 'LogisticDetails':
            output+='<tr><td>'+font+data[1]+'</td><td>'+font+data[2]+'</td><td>'+font+data[3]+'</td><tr>'
    output+='</table><br/><br/><table align=center border=1><tr><th>Equipment ID or Code</th><th>Supervision Details</th><th>Comment Date</th></tr>'
    for i in range(len(arr)):
        data = arr[i].split("$")
        if data[0] == 'SupervisionDetails':
            output+='<tr><td>'+font+data[1]+'</td><td>'+font+data[2]+'</td><td>'+font+data[3]+'</td><tr>'

    output+='</table><br/><br/><table align=center border=1><tr><th>Equipment ID or Code</th><th>Sold To</th><th>Sold Date</th></tr>'
    for i in range(len(arr)):
        data = arr[i].split("$")
        if data[0] == 'DistributionDetails':
            output+='<tr><td>'+font+data[1]+'</td><td>'+font+data[2]+'</td><td>'+font+data[3]+'</td><tr>'
    return output            


def ViewLogisticDetails(request):
    if request.method == 'GET':
        output = getDetails()
        context= {'data':output}        
        return render(request, 'ViewLogisticDetails.html', context)
    
def ViewEquipmentDetails(request):
    if request.method == 'GET':
        output = getDetails()
        context= {'data':output}        
        return render(request, 'ViewEquipmentDetails.html', context)

def ViewDistributionDetails(request):
    if request.method == 'GET':
        output = getDetails()
        context= {'data':output}        
        return render(request, 'ViewDistributionDetails.html', context)

def ViewSupervisionDetails(request):
    if request.method == 'GET':
        output = getDetails()
        context= {'data':output}        
        return render(request, 'ViewSupervisionDetails.html', context)

def AddSupervisionAction(request):
    if request.method == 'POST':
        global details
        today = date.today()
        code = request.POST.get('t1', False)
        location = request.POST.get('t2', False)
        saveDataBlockChain("SupervisionDetails$"+code+"$"+location+"$"+str(today)+"\n")
        '''
        if len(details) == 0:
            details = "SupervisionDetails$"+code+"$"+location+"$"+str(today)+"\n"
        else:
            details+="SupervisionDetails$"+code+"$"+location+"$"+str(today)+"\n"
        '''
        context= {'data':'Supervision comment details added'}
        return render(request, 'SupervisionScreen.html', context)      

def AddSupervision(request):
    if request.method == 'GET':
        output = '<tr><td><font size=3 color=black>Product&nbsp;Code</b></td><td><select name="t1">'
        global details
        arr = details.split("\n")
        for i in range(len(arr)):
            data = arr[i].split("$")
            if data[0] == 'ProductionDetails':
                output+='<option value='+data[1]+'>'+data[1]+'</option>'
        output+='</option></td></tr>'
        context= {'data1':output}
        return render(request, 'AddSupervision.html', context)    

def AddDistribution(request):
    if request.method == 'GET':
        output = '<tr><td><font size=3 color=black>Product&nbsp;Code</b></td><td><select name="t1">'
        global details
        arr = details.split("\n")
        for i in range(len(arr)):
            data = arr[i].split("$")
            if data[0] == 'ProductionDetails':
                output+='<option value='+data[1]+'>'+data[1]+'</option>'
        output+='</option></td></tr>'
        context= {'data1':output}
        return render(request, 'AddDistribution.html', context)

def AddDistributionAction(request):
    if request.method == 'POST':
        global details
        today = date.today()
        code = request.POST.get('t1', False)
        location = request.POST.get('t2', False)
        saveDataBlockChain("DistributionDetails$"+code+"$"+location+"$"+str(today)+"\n")
        '''
        if len(details) == 0:
            details = "DistributionDetails$"+code+"$"+location+"$"+str(today)+"\n"
        else:
            details+="DistributionDetails$"+code+"$"+location+"$"+str(today)+"\n"
        '''
        context= {'data':'Distribution details added'}
        return render(request, 'DistributionScreen.html', context)     
        

def AddLogisticAction(request):
    if request.method == 'POST':
        global details
        today = date.today()
        code = request.POST.get('t1', False)
        location = request.POST.get('t2', False)
        saveDataBlockChain("LogisticDetails$"+code+"$"+location+"$"+str(today)+"\n")
        '''
        if len(details) == 0:
            details = "LogisticDetails$"+code+"$"+location+"$"+str(today)+"\n"
        else:
            details+="LogisticDetails$"+code+"$"+location+"$"+str(today)+"\n"
        '''
        context= {'data':'Logistic details added'}
        return render(request, 'CirculationScreen.html', context) 

def AddEquipmentAction(request):
    if request.method == 'POST':
        global details
        code = request.POST.get('t1', False)
        batch = request.POST.get('t2', False)
        pdate = request.POST.get('t3', False)
        name = request.POST.get('t4', False)
        desc = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        myfile = request.FILES['t7']
        fname = request.FILES['t7'].name
        fs = FileSystemStorage()
        filename = fs.save('EquipmentBCApp/static/products/'+code+".png", myfile)
        saveDataBlockChain("ProductionDetails$"+code+"$"+batch+"$"+pdate+"$"+name+"$"+desc+"$"+address+"\n")
        '''
        if len(details) == 0:
            details = "ProductionDetails$"+code+"$"+batch+"$"+pdate+"$"+name+"$"+desc+"$"+address+"\n"
        else:
            details+="ProductionDetails$"+code+"$"+batch+"$"+pdate+"$"+name+"$"+desc+"$"+address+"\n"
        '''    
        context= {'data':'Production details added'}
        return render(request, 'AddEquipment.html', context)       
        

def AddLogistic(request):
    if request.method == 'GET':
        output = '<tr><td><font size=3 color=black>Product&nbsp;Code</b></td><td><select name="t1">'
        global details
        arr = details.split("\n")
        for i in range(len(arr)):
            data = arr[i].split("$")
            if data[0] == 'ProductionDetails':
                output+='<option value='+data[1]+'>'+data[1]+'</option>'
        output+='</option></td></tr>'
        context= {'data1':output}
        return render(request, 'AddLogistic.html', context)


def AddEquipment(request):
    if request.method == 'GET':
       return render(request, 'AddEquipment.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        usertype = request.POST.get('usertype', False)
        if username == 'Production' and password == 'Production' and usertype == 'Production':
            context= {'data':'welcome '+username}
            return render(request, 'ProductionScreen.html', context)
        elif username == 'Circulation' and password == 'Circulation' and usertype == 'Circulation':
            context= {'data':'welcome '+username}
            return render(request, 'CirculationScreen.html', context)
        elif username == 'Distribution' and password == 'Distribution' and usertype == 'Distribution':
            context= {'data':'welcome '+username}
            return render(request, 'DistributionScreen.html', context)
        elif username == 'Supervision' and password == 'Supervision' and usertype == 'Supervision':
            context= {'data':'welcome '+username}
            return render(request, 'SupervisionScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)    
