def main():
    ft = open('t.txt','w')
    fo = open('o.txt','w')
    fa = open('a.txt','w')
    ft1 = open('t1.txt','w')
    fo1 = open('o1.txt','w')
    fa1 = open('a1.txt','w')   
    fterms = open('terms.txt','r')
    ftermsright = open('10-terms.txt','r')
    
    #split new
    for line in fterms:
        if 'a-' in line:
            fa1.write(line)
        elif 'o-' in line:
            fo1.write(line)
        elif 't-' in line:
            ft1.write(line)            
            
        
    #split old
    for line in ftermsright:
        if 'a-' in line:
            fa.write(line)
        elif 'o-' in line:
            fo.write(line)
        elif 't-' in line:
            ft.write(line)    
main()
        
        