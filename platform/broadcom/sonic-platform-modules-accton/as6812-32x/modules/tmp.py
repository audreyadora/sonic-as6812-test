import math
max_query_entries = 8

rmin = 80
rmax = 480
step = 2

query_step = max_query_entries*step + step
n_queries = math.ceil((rmax-rmin)/query_step)

qmin = rmin
query = []
for n in range(1,n_queries+1):
    qmax = rmax + step if qmin + query_step > rmax else qmin + query_step
    query.append("(" + ",".join([f"{i}TB" for i in range(qmin,qmax,step)]) + ")")
    query.append("(" + ",".join([f"{i} TB" for i in range(qmin,qmax,step)]) + ")")
    qmin += query_step
