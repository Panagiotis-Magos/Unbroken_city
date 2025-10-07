import sys
import os

#Goals - I need to write a program to make pop handling easy, such that vic 2 modding is not such a fucking drag
#It should include: 
#Both state and province level interaction. If developed into an app it could be system level
#but for now will be a prompt

#Ability to modify pops by percent. There are different pop types - try an equal split?

#Ability for total number to increase/decrease

#Ability for some pop numbers to increase for certain cultures providing a skew?

#Start by requesting states/provinces (can be done in a single function checking chars)

#ask if I want to alter ethnicity of pops

#Continue requesting sets of culture/religion/percent. Percent reflects change from current pops.

#this will spew out equal sized parts of all poptypes.
 


#This is only intended to capture cultures. Other pop types may pop up later or be added manually.






poptypes= ["farmers","slaves","bureaucrats","clergymen","artisans","soldiers","aristocrats","officers","capitalists","craftsmen","labourers","clerks"]

#ask user the cultures/proportions they want to add
def inquire():
    cult=input("do you want to add more cultures/religions? Type \"n\" if not ")
    pops=[]
    while cult!="n":
        culture=input("what culture do you want to add? ")
        religion=input("what religion does it have? ")
        size=input("what size will that culture have?Input for example \"12\" for 12% of total pop size ")
        pops.append((culture,religion,int(size)))
        cult=input("do you want to add more cultures/religions? Type \"n\" if not ")
        
    if len(pops)>0: 
        print("The pop composition you have chosen is:")
        for i in range(len(pops)):
            print(pops[i][0] + " " + pops[i][1]+ " "+ str(pops[i][2])+"%")
    else:
        print("you have not added any pops. If this is by mistake, restart the program")
        
    
        
    return pops

#We now know the culture composition of our provinces and the addition of poptypes that might not exist. In case the poptypes do exist, this will be an additive change

#This function creates the text for the new province info
      
def createtext(prov,pops,cultures): #here pops is a dict where pops[poptype]=size
    text=[]
    text.append( str(prov)+ " = {\n" )
    for pop in pops:
        line1="\t"+pop+" = {\n"
        for culture in cultures:
            line2="\t\tculture = "+culture[0]+"\n"
            line3="\t\treligion = "+culture[1]+"\n"
            line4="\t\tsize = "+str(int(round(culture[2]*pops[pop]/100)))+"\n"
            line5="\t}\n"
            line6="\n"
            if(line4 == "\t\tsize = 0"):
                continue
            else:
                text.append(line1)
                text.append(line2)
                text.append(line3)
                text.append(line4)
                text.append(line5)
                text.append(line6)
    return text
            

        



def reader(input_file,provs,cultures): #provs is relevant list of provinces. Reads it and returns a dict in the format dict[province][poptype]=total size
    f = open(input_file, "r+")
    l = f.readlines()
    res={}
    a=[]
    replacements = []  # list of (start, end, province, res) Chatgpt help to do it in reverse and not fuck up indexing
    for i in range(len(l)): #create table with tables for each row
        a.append(l[i].split())
    province="0"
    outofpop=0
    #print(len(a))
    for i in range(len(a)):
        if(len(a[i])==0):
            continue
        if province == "0" and len(a[i])==3 and a[i][0]!="#" and a[i][2]=="{": #if you have entered a province    
            if(a[i][0] in provs ):
                province=a[i][0]
                start=i
        if(province!="0"): #you are within a province you care about
            if(a[i][0] in poptypes):
                pop=a[i][0]
                if(pop not in res):
                    res[pop]=0
            if a[i][0] == "size":
                res[pop]+=int(a[i][2])
            if('}'in a[i]):
                if outofpop:
                    print(province)
                    print(res)
                    end=i
                    replacements.append((start, end, province, res))
                    #l[start:end]=createtext(province,res,cultures)
                    #print(createtext(province,res,cultures))
                    province="0"
                    res={}
                else:
                    outofpop=1
            if('{'in a[i]):
                outofpop=0
     
    f.close
    for start, end, province, res in reversed(replacements):
        l[start:end] = createtext(province, res, cultures)
    #print(l)
    with open(input_file, "w") as f:
        f.writelines(l)     
    return res

def state_and_province_getter(og_path): #this function creates a list of provinces from provinces and states
    new_state= input("which states/provinces do you want to change? Type \"n\" when done\n")
    states=[]
    provinces=[]
    provtostate=[]

    while(new_state!='n'):
        if not new_state[0].isdigit():
            states.append(new_state)
        elif new_state[len(new_state)-2]=="s":
            provtostate.append(new_state[0:(len(new_state)-1)])
        else:
            provinces.append(new_state)
        new_state= input("which states/provinces do you want to change? Type \"n\" when done. End a province with s to nab all of its state\n")
        
    states_file = open(og_path+"/map/region.txt","r")

    state_content=states_file.read()
    state_content=state_content.split("\n")

    #print(state_content)

    #this is messy as shit but finds the provinces of the state

    p=[]
    for i in range(len(state_content)): #create table with tables for each row
        p.append(state_content[i].split())
    
    #this finds the states of the provinces marked with an s
    for i in range(len(p)):
        for j in range(len(p[i])):
            if(p[i][j] in provtostate):
                states.append(p[i][0])
        
    #this takes provinces from states
    for i in range(len(p)):
        if len(p[i])<3 :
            pass
        else:
            for state in states:
                if p[i][0]==state:
                    for j in range(1,len(p[i])):
                        if p[i][j]!="{" and p[i][j]!="}" and p[i][j]!="=":
                            provinces.append(p[i][j])
    
    return provinces 

og_path=sys.argv[1] #path to unbroken_city mod folder
path=og_path+"/history/pops"
file_list=[]
for root, dirs, files in os.walk(path):
    parent_folder = os.path.basename(root)
    for file in files:
        file_list.append(f"{parent_folder}/{file}") 

provinces=state_and_province_getter(og_path)
print(provinces)

mycult=inquire()
confirm=input("Are you sure you want to apply this? press \"y\" if yes")
if confirm=="y":
    for file in file_list:
        reader(path+"/"+file,provinces,mycult)