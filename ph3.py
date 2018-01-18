import re
from bsddb3 import db
total_mat = []
output_type = "output=key"
#this is the main function
def main():
    global total_mat, output_type
    
    # database init
    
    DB_File1 = "te.idx"
    database1 = db.DB()
    database1.open(DB_File1,None, db.DB_BTREE, db.DB_CREATE)
    cur1 = database1.cursor()

    DB_File2 = "ye.idx"
    database2 = db.DB()
    database2.open(DB_File2,None, db.DB_HASH, db.DB_CREATE)
    cur2 = database2.cursor()

    DB_File3 = "re.idx"
    database3 = db.DB()
    database3.open(DB_File3,None, db.DB_BTREE, db.DB_CREATE)
    cur3 = database3.cursor()
    
    # enter query
    query = input("Please Enter query!!!\n")
    commands = re.split(' ', query)
    final =[]
    # operate each command
    for each in commands:
        each = each.lower()
        if ":" in each or ">" in each or "<" in each:
            final.append(each)
        elif each == "database":
            final.append(each)
        else:
            final[len(final)-1] += " "+each
    # continue operating
    for each in final:
        each = each.lower()
        # if command in term
        if "title" in each or "author" in each or "other" in each:
            if ':"' in each:
                partial_result= phrase(each,cur1,cur3)
                if not total_mat:
                    total_mat = partial_result
                else:
                    total_mat = list(set(partial_result).intersection(total_mat))
            else:
                partial_result=termdatabase(each,cur1)
                if not total_mat:
                    total_mat = partial_result
                else:
                    total_mat = list(set(partial_result).intersection(total_mat))
        # if command in year
        elif "year" in each:
            partial_result = yeardatabase(each, cur2)
            if not total_mat:
                total_mat = partial_result
            else:
                total_mat = list(set(partial_result).intersection(total_mat))
        # if command in all
        elif "database" in each:
            iter = cur3.first()
            partial_result = []
            while iter:
                partial_result.append(iter[0].decode("utf-8"))
                iter = cur3.next()
            if not total_mat:
                total_mat = partial_result
            else:
                total_mat = list(set(partial_result).intersection(total_mat))

    exitCode = False
    print("numbers of matches:",len(total_mat))
    oricommand = input("See full results: output=all|See keys only: output=key|default: Press enter\n")
    # display information
    if oricommand != '':
        output_type = oricommand
    full_result=findAllRec(cur3)
    if output_type == "output=key":
        for item in total_mat:
            print(item)
    elif output_type == "output=all":
        for item in full_result:
            print(item)
    else:
        print("Error!Error!Error!\n")

# find all records
def findAllRec(cur):
    global total_mat
    partial_result =[]
    iter = cur.first()
    while iter:
        for key in total_mat:
            if bytes(key, 'utf-8') == iter[0]:
                partial_result.append(iter[0].decode("utf-8")+":"+iter[1].decode("utf-8"))
        iter = cur.next()
    return(partial_result)

# find data in te.idx
def termdatabase(cmd,cur):#
    global total_mat
    partial_result =[]

    keyword = cmd.split(":")
    if keyword[0] == "title":
        key = bytes("t-", 'utf-8') + bytes(keyword[1], 'utf-8')
        iter = cur.first()
        while iter:
            if key == iter[0]:
                partial_result.append(iter[1].decode("utf-8"))
            iter = cur.next()

    elif keyword[0] == "author":
        key = bytes("a-", 'utf-8') + bytes(keyword[1], 'utf-8')
        iter = cur.first()
        while iter:
            if key == iter[0]:
                partial_result.append(iter[1].decode("utf-8"))
            iter = cur.next()

    elif keyword[0] == "other":
        key = bytes("o-", 'utf-8') + bytes(keyword[1], 'utf-8')
        iter = cur.first()
        while iter:
            if key == iter[0]:
                partial_result.append(iter[1].decode("utf-8"))
            iter = cur.next()
    return partial_result

'''
bug detail:
total_mat should be None before line 47
But it is assigned incorrectly at if statement in line 146

debug detail:
global total_mat is replaced by sub_total
'''

# find data in ye.idx

def yeardatabase(cmd,cur):
    global total_mat
    partial_result =[]
    sub_total = []
    if ":" in cmd:
        keyword = cmd.split(":")
        result = cur.set_range(keyword[1].encode("utf-8"))
        if(result != None):
            while(result != None):
                if str(result[0].decode("utf-8")[:]) != keyword[1]:
                    break
                partial_result.append(result[1].decode("utf-8"))
                result = cur.next()
    elif ">" in cmd:
        keyword = cmd.split(">")
        iter = cur.first()
        while iter:
            if not sub_total:
                sub_total = partial_result
            else:
                    sub_total = list(set(partial_result).intersection(sub_total))
            if int(keyword[1]) < int(iter[0].decode("utf-8")):
                partial_result.append(iter[1].decode("utf-8"))

            iter = cur.next()

    elif "<" in cmd:
        keyword = cmd.split("<")
        iter = cur.first()
        while iter:
            if int(keyword[1]) > int(iter[0].decode("utf-8")):
                partial_result.append(iter[1].decode("utf-8"))
            iter = cur.next()

    return partial_result

# deal with phrase command
def phrase(command,cur1,cur3):
    command = command.lower()
    recommand = re.findall(r"[a-zA-Z0-9_]+", command)
    partial_cmd = []
    total_cmd = []
    substring = ''
    partial_result = []
    for i in range(1,len(recommand)):
        if i == len(recommand) - 1:
            substring += recommand[i]
        else:
            substring += recommand[i] +' '
    # if title in phrase
    if recommand[0]== "title":
        for i in range(1,len(recommand)):
            cmd = recommand[0] + ":" + recommand[i]
            partial_cmd = termdatabase(cmd,cur1)
            if not total_cmd:
                total_cmd = partial_cmd
            else:
                total_cmd = list(set(partial_cmd).intersection(total_cmd))

            # record

            for each in total_cmd:
                iter = cur3.first()
                while iter:
                    if bytes(each, 'utf-8') == iter[0]:
                        temp = iter[1].decode("utf-8")
                        temp = temp.lower()
                        temp = temp.split('<title>')
                        for i in range(1,len(temp)):
                            if '</title>' in temp[i]:
                                temp[i].lower()
                                tem = temp[i].split()
                                if substring in tem and each not in partial_result :
                                    partial_result.append(each)
                    iter = cur3.next()



    # if author in phrase
    
    elif recommand[0]== "author":
        for i in range(1,len(recommand)):
            cmd = recommand[0] + ":" + recommand[i]
            partial_cmd = termdatabase(cmd,cur1)
            if not total_cmd:
                total_cmd = partial_cmd
            else:
                total_cmd = list(set(partial_cmd).intersection(total_cmd))

            # record

            for each in total_cmd:
                iter = cur3.first()
                while iter:
                    if bytes(each, 'utf-8') == iter[0]:
                        temp = iter[1].decode("utf-8")
                        temp = temp.lower()
                        temp = temp.split('<author>')
                        for i in range(1,len(temp)):
                            if '</author>' in temp[i]:
                                temp[i].lower()
                                tem = temp[i].split()
                                if substring in tem and each not in partial_result :
                                    partial_result.append(each)
                    iter = cur3.next()
    # if other in phrase

    elif recommand[0]== "other":
        # for i in range(1,len(recommand)):
            cmd = recommand[0] + ":" + recommand[i]
            partial_cmd = termdatabase(cmd,cur1)
            if not total_cmd:
                total_cmd = partial_cmd
            else:
                total_cmd = list(set(partial_cmd).intersection(total_cmd))

            # record

            for each in total_cmd:
                iter = cur3.first()
                while iter:
                    if bytes(each, 'utf-8') == iter[0]:
                        temp = iter[1].decode("utf-8")
                        temp = temp.lower()
                        
                        temp=temp.replace("<journal>", "<other>")
                        temp=temp.replace("<booktitle>", "<other>")
                        temp=temp.replace("<publisher>", "<other>")

                        temp = temp.split('<other>')
                        for i in range(1,len(temp)):
                            if '</journal>' in temp[i] or '</booktitle>' in temp[i] or '</publisher>' in temp[i] :
                                temp[i].lower()
                                tem = temp[i].split()
                                if substring in tem and each not in partial_result :
                                    partial_result.append(each)
                    iter = cur3.next()
    return partial_result
while True:
    total_mat = []
    main()   