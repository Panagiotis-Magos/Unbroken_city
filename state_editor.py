import sys
import os

def province_editor(input_file,owner,cores,wipe_cores=True):
    f = open(input_file, "r+")
    l = f.readlines()
    delete_lines=[] 
    for i in range(0,len(l)):
        if (owner!="NO" and(l[i].split(" ")[0]=="owner" or l[i].split(" ")[0]=="controller")) or (wipe_cores and l[i].split(" ")[0]=="add_core"):
            delete_lines.append(i)
           
    for line in sorted(delete_lines,reverse=True):
        del l[line]

    if owner!="NO":
        l.insert(0,"controller = "+owner+"\n")
        l.insert(0,"owner = "+owner+"\n")
        
    for core in cores:
        l.insert(2,"add_core="+core+"\n")
            
    with open(input_file, "w") as f:
        f.writelines(l)

og_path=sys.argv[1] #path to unbroken_city mod folder
path=og_path+"/history/provinces"
file_list=[]
for root, dirs, files in os.walk(path):
    parent_folder = os.path.basename(root)
    for file in files:
        file_list.append(f"{parent_folder}/{file}") 



states=[]
new_state= input("which states do you want to change? Type NO when done\n")

while(new_state!='NO'):
    
        states.append(new_state)
        new_state = input("which states do you want to change? Type NO when done\n")
    
states_file = open(og_path+"/map/region.txt","r")

state_content=states_file.read()
state_content=state_content.split("\n")

#print(state_content)

#this is messy as shit but finds the provinces of the state

p=[]
for i in range(len(state_content)): #create table with tables for each row
    p.append(state_content[i].split())
    
stateprov={}
for i in range(len(p)):
    if len(p[i])<3 :
        pass
    else:
        for state in states:
            if p[i][0]==state:
                stateprov[p[i][0]]=p[i][1:]

#this is messy but recieves the input
new_owner= input("which do you want to be the owner? Type NO if none\n")

new_cores=[]
new_core = input("what cores do you want to add? Type NO when done\n")

while(new_core!='NO'):
        new_cores.append(new_core)
        new_core = input("what cores do you want to add? Type NO when done\n")

wipe1= input("do you want to wipe the cores? type NO if not\n")

wipe2=True
if wipe1=="NO":
    wipe2=False
        

print(stateprov)
for file in file_list:
    if file != "word-replacer.py":
        check=file.split("/")
        check=check[1].split() #this finds province id
        #print(check)
        for state in stateprov:
            if check[0] in stateprov[state]:
                province_editor(path+"/"+file,new_owner,new_cores,wipe2)
                print("changed province "+check[0]+"\n")

#temp
#file=sys.argv[1]
#province_editor(file,"MOR",["TUR","ROM"],True)  
