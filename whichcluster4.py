set1=range(370,710)
#set2=[51,54,67,73,82,122,138,162,166,173,180,185,186,201,202,215,219,225,\
#      231,263,264,265,266,287,290,294,300,315,332,348]
set2=[401,402,403,408,409,410,418,419,502,503,504,506,557]
filename=[i for i in set1 if i not in set2]
f1=open('C:/users/dawei/downloads/test2.txt','w')
for i in range(len(filename)):
    f=open('C:/users/dawei/downloads/images/{}.jpg.csv'.format(filename[i]),'r')
    line=f.readlines()   
    new_line=''
    for j in line:
        j=j.strip()
        j=j.rstrip(' \n')
        new_line=new_line+j
    f.close()    
    f1.write(new_line+'\n')

f1.close()
