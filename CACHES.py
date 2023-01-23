'''
 This model uses LRU replacement policy in cache implementation and returns the Hit Accuracy for each trace file
 Structure of cache can be customized as per user's wish
 User can enter 
 -> 1) No. of ways in cache  (a power of 2) 
 -> 2) Block size            (a power of 2)  
 -> 3) Total size of cache   (a power 0f 2)
'''

from math import *
# from tabulate import tabulate
def binaryToDecimal(n):
    return int(n,2)
def accuracy(file_name,w,bs,s):
    finput = open(file_name, 'r')   #.trace
    Lines = finput.readlines() 
    foutput = open("to_text.txt", "w")   #.txt
    for line in Lines:
        foutput.write(line)
    foutput.close()
    finput.close()
    fin = open('to_text.txt','r')
    fout= open('binary.txt','w')
    Lines=fin.readlines()
    count=0
    for q in Lines:
        a=q[4:12]  
        b=q[4:]
        res = "{0:08b}".format(int(a, 16))  
        fout.write(str(res).zfill(32)+'\n')            
    fin.close()
    fout.close()
    ways=w  # no. of ways
    block_size=bs # block size
    total_size=s*1024 #total size of cache
    byte_offset=int(log(block_size,2)) # no. of Byte Offset bits
    index_bits=int(log((total_size/(block_size*ways)),2)) # no. of index bits
    index=int(total_size/(block_size*ways)) # no. of sets
    tag_bits=32-index_bits-byte_offset # no. of Tag bits
    cache={} # cache dictionary 
    instr_status=[] # stores the line instruction with its miss/hit status.
    valid_bit=0 
    data='data'
    flag=0
    list_of_values=[] # stores n ways for a set
    tag_data_pairs=[valid_bit,-1,data,0] # stores valid bit, tag bits, data & max_priority(replace the way with max_priority) of a way
    hit_count=0 # no. of hits
    miss_count=0 #no. of misses
    for set_no in range(0,index):
        for clmns in range(0,ways):
            list_of_values.append(tag_data_pairs.copy())
        cache[set_no]=list_of_values
        list_of_values=[]
    fin1=open('binary.txt','r')
    Lines=fin1.readlines()
    fin1.close()
    for l in Lines:
        validity=0
        max_priority=0
        no_match=0
        flag=0
        tag=l[0:tag_bits]
        ind=l[tag_bits:30]
        bo=l[tag_bits+index_bits:-1]
        current_set=cache[binaryToDecimal(ind)]   
        for i in current_set:    
            if(i[0]==1):    validity+=1
        #all empty
        if(validity==0):
            miss_count+=1
            instr_status.append([l,"MISS"])
            current_set[0][3]=0
            current_set[0][0]=1
            current_set[0][1]=tag
        #semi-filled
        elif(validity<ways):
            for i in current_set :
                if(tag==i[1]):
                    flag=1
                    hit_count+=1
                    instr_status.append([l,"HIT"])
                    i[3]=0
                    target_way=i
                    for j in current_set :
                        if(j!=target_way):
                            j[3]+=1 
            if(flag==0):
                miss_count+=1
                instr_status.append([l,"MISS"])
                current_set[validity][0]=1
                current_set[validity][1]=tag
                for i in current_set :
                    i[3]+=1
                current_set[validity][3]=0
        #completely-filled
        elif(validity==ways):
            for i in current_set:
                max_priority=max(max_priority,i[3])   # the max gets replaced
            for i in current_set :
                if(tag==i[1]):
                    hit_count+=1
                    instr_status.append([l,"HIT"])
                    i[3]=0
                    target_way=i
                    for j in current_set :
                        if(j!=target_way):
                            j[3]+=1
                    break
                else:
                    no_match+=1
            if(no_match==ways):
                miss_count+=1
                instr_status.append([l,"MISS"])
                for i in current_set:
                    if(i[3]==max_priority):
                        i[3]=0
                        i[1]=tag
                        target_way=i
                        for j in current_set :
                            if(j!=target_way):
                                j[3]+=1
    print("Hit Count : " ,hit_count)
    print("Miss Count : ",miss_count)
    print("Hit Accuracy : ",hit_count/(hit_count+miss_count)*100)
    
    # col_names = ["Instruction", "Hit/Miss"]
    # print(tabulate(instr_status, headers=col_names, tablefmt="fancy_grid"))

#main
w = int(input("Enter Number of Ways : "))
bs= int(input("Enter Block Size in Bytes : "))
s = int(input("Enter Total Size of Cache in Kilobytes : "))
print("gcc")
accuracy("gcc.trace",w,bs,s)
print("-----------------------------------------------------------------------------------")
print("mcf")
accuracy("mcf.trace",w,bs,s)
print("-----------------------------------------------------------------------------------")
print("gzip")
accuracy("gzip.trace",w,bs,s)
print("-----------------------------------------------------------------------------------")
print("swim")
accuracy("swim.trace",w,bs,s)
print("-----------------------------------------------------------------------------------")
print("twolf")
accuracy("twolf.trace",w,bs,s)