from bsddb3 import db
import re
import os
def main():
    sourceFile= input("Enter name of source file\n")
    fr = open(sourceFile,'r')
    fterms = open('terms.txt','w')
    fyears = open('years.txt','w')
    frecs = open('recs.txt','w')
    
    for line in fr:
        reline = re.findall(r"[a-zA-Z0-9_ /-]+", line)    
        if reline[0] == "article key" or reline[0] == "inproceedings key":
            key = reline[1]
            frecs.write(key + ":" + line)
            for index in range(len(reline)):
                if reline[index] =="author":
                    temptstring = ""
                    tempindex = index + 1
                    while reline[tempindex] != "/author" and reline[tempindex] != "/inproceedings" and reline[tempindex] != "/article":
                        if len(reline[tempindex]) >2 :
                            temptstring += ' ' + reline[tempindex]
                        tempindex += 1
                    temp1 = re.split(' |/|-',temptstring)
                    for each in temp1: 
                      
                        # length check
                        if len(each) > 2:
                            each = each.lower()
                            temp2 = "a-" + each + ":" + key + "\n"
                            fterms.write(temp2)
            
                elif reline[index] == "title":
                    temptstring = ""
                    tempindex = index + 1
                    while reline[tempindex] != "/title" and reline[tempindex] != "/inproceedings" and reline[tempindex] != "/article":
                        if len(reline[tempindex]) >2 :
                            temptstring += ' ' + reline[tempindex]
                        tempindex += 1
                    temp1 = re.split(' |/|-',temptstring) 
                    for each in temp1: 
                        # length check
                        if len(each) > 2:
                            each = each.lower()
                            temp2 = "t-" + each + ":" + key + "\n"
                            fterms.write(temp2)
                            
                elif reline[index] == "journal":
                    temptstring = ""
                    tempindex = index + 1
                    while reline[tempindex] != "/journal" and reline[tempindex] != "/inproceedings" and reline[tempindex] != "/article":
                        if len(reline[tempindex]) >2 :
                            temptstring += ' ' + reline[tempindex]
                        tempindex += 1
                    temp1 = re.split(' |/|-',temptstring) 
                    for each in temp1: 
                        # length check
                        if len(each) > 2:
                            each = each.lower()
                            temp2 = "o-" + each + ":" + key + "\n"
                            fterms.write(temp2)
                elif reline[index] == "booktitle":
                    temptstring = ""
                    tempindex = index + 1
                    while reline[tempindex] != "/booktitle" and reline[tempindex] != "/inproceedings" and reline[tempindex] != "/article":
                        if len(reline[tempindex]) >2 :
                            temptstring += ' ' + reline[tempindex]
                        tempindex += 1
                    temp1 = re.split(' |/|-',temptstring) 
                    for each in temp1: 
                        # length check
                        if len(each) > 2:
                            each = each.lower()
                            temp2 = "o-" + each + ":" + key + "\n"
                            fterms.write(temp2)
                elif reline[index] == "publisher":
                    temptstring = ""
                    tempindex = index + 1
                    while reline[tempindex] != "/publisher" and reline[tempindex] != "/inproceedings" and reline[tempindex] != "/article":
                        if len(reline[tempindex]) >2 :
                            temptstring += ' ' + reline[tempindex]
                        tempindex += 1
                    temp1 = re.split(' |/|-',temptstring) 
                    for each in temp1: 
                        # length check
                        if len(each) > 2:
                            each = each.lower()
                            temp2 = "o-" + each + ":" + key + "\n"
                            fterms.write(temp2)                                    
                                 
                elif reline[index] == "year":
                    temp1 = reline[index + 1]
                    temp2 = temp1 + ":" + key + "\n"
                    fyears.write(temp2) 
                                  
main() 



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
    