import random
import time

def getrandata(num):
	ret_list,i = [],0

	while i<num:
		ret_list.append(random.randint(0,100000))
		i += 1

	return ret_list

def bubbleSort(a):  
    l=len(a)-2  
    i=0  
    while i<l:  
        j=l  
        while j>=i:  
            if(a[j+1]<a[j]):  
                a[j],a[j+1]=a[j+1],a[j]  
            j-=1  
        i+=1
    return a

def insertSort(arr):
	for i in range(1,len(arr)):
		j = i
		while j > 0 and arr[j-1] > arr[i]:
			j -= 1
		arr.insert(j,arr[i])
		arr.pop(i+1)
		print i,arr
	return arr

def zjhSort(arr):
	for i in range(len(arr)-1):
		middle = arr[i]
		pos = i
		j = 1
		while j<len(arr)-i:
			if arr[i+j] < middle:
				middle = arr[i+j]
				pos = i+j
				print 'pos:%d,i:%d' % (pos,i)
			j += 1
		print 'second=i:%d' % i
		if i != pos:
			arr[i],arr[pos] = arr[pos],arr[i]
	return arr

def shellSort(arr):  
    dist=len(arr)/2  
    while dist>0:  
        for i in range(dist,len(arr)):  
            tmp=arr[i]  
            j=i  
            while j>=dist and tmp<arr[j-dist]:  
                arr[j]=arr[j-dist]  
                j-=dist  
            arr[j]=tmp  
        dist/=2
    return arr


lis = getrandata(100000)
then = time.time()
shellSort(lis)
print time.time()-then

