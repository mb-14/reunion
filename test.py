import reunion
import time

start = time.time()
f = reunion.FEC(4,2)
text= open('file.txt','r')
data = text.read()
s = f.Encode(data)
f.Decode(s[:2])
stop = time.time()
print stop - start

