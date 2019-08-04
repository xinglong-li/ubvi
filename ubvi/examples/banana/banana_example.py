import autograd.numpy as np
from autograd.scipy.misc import logsumexp

from UBVI import ubvi
from BBVI import bbvi, mvnlogpdf
import matplotlib.pyplot as plt
import pickle as pk
import os

def banana(X):
    b = 0.1
    x = X[:,0]
    y = X[:,1]
    return -x**2/200 - (y+b*x**2-100*b)**2/2 - np.log(2*np.pi*10)

def logf(x):
   return 0.5*banana(x)



N_runs = 1000
N = 10

d = 2
n_samples = 100
n_logfg_samples = 10000
adam_num_iters = 3000
adam_learning_rate = lambda itr : 0.1/np.sqrt(1.+itr)
print_every=1000
n_init=1000
lmb_good = lambda itr : 70./(itr+1)
lmb_bad = lambda itr : 1./(itr+1)

if not os.path.exists('results/'):
  os.mkdir('results')


################################################################################

for i in range(N_runs):
  print('RUN ' + str(i+1)+'/'+str(N_runs))
  ubvi_ = ubvi(logf, N, d, n_samples, n_logfg_samples, adam_learning_rate, adam_num_iters, print_every, n_init=n_init)

  bbvi_ = bbvi(banana, N, d, n_samples, lmb_good, adam_learning_rate, adam_num_iters, print_every, n_init)

  bbvi2_ = bbvi(banana, N, d, n_samples, lmb_bad, adam_learning_rate, adam_num_iters, print_every, n_init)

  if os.path.exists('results/banana.pk'):
    f = open('results/banana.pk', 'rb')
    res = pk.load(f)
    f.close()
    res[0].append(ubvi_)
    res[1].append(bbvi_)
    res[2].append(bbvi2_)
    f = open('results/banana.pk', 'wb')
    pk.dump(res, f)
    f.close()
  else:
    f = open('results/banana.pk', 'wb')
    pk.dump(([ubvi_], [bbvi_], [bbvi2_]), f)
    f.close()

#f = open('banana.pk', 'rb')
#res = pk.load(f)
#f.close()
#
#f = open('banana.pk', 'wb')
#pk.dump((res[0], res[1], bbvi2s), f)
#f.close()
#
##f = open('banana.pk', 'wb')
##pk.dump((ubvis, bbvis, bbvi2s), f)
##f.close()
#
#