def mergesort(ulist):
    print("Splitting ",ulist)
    if len(ulist) > 1:
        mid = len(ulist) // 2  
        lefthalf = ulist[:mid]
        righthalf = ulist[mid:]
        mergesort(lefthalf)  
        mergesort(righthalf)
        
        i = 0
        j = 0
        k = 0
        print("\nchegou\n",ulist,lefthalf,righthalf,len(lefthalf),len(righthalf),len(ulist))
        
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                print('p1 ulist:',k,'=',lefthalf[i])
                ulist[k] = lefthalf[i]
                i += 1
            else:
                print('p2 ulist:',k,'=',righthalf[j])
                ulist[k] = righthalf[j]
                j += 1   
            k += 1

        while i < len(lefthalf):
            print('p3 ulist:',k,'=',lefthalf[i])
            ulist[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            print('p4 ulist:',k,'=',righthalf[j])
            ulist[k] = righthalf[j]
            j += 1
            k += 1

    print('merging ',ulist)

#listateste = [54,26,93,17,77,31,44,55,20]
listateste = [54,26,93,17]
print(listateste)
mergesort(listateste)
print(listateste)