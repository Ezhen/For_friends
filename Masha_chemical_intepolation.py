#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from lmfit.printfuncs import *
import numpy as np

# create a set of Parameters
params = Parameters()
params.add('C0',   value=0.1, min=0.01, max=1)
params.add('b', value= 10, min=-10,max=100)

# define objective function: returns the array to be minimized
def fcn2min(params, x, data):
    """ model decaying concentration"""
    C0 = params['C0']
    b = params['b']
    model = ((x/x[0])**b)*C0#*data[0]
    return model - data

a=[];m=[];c=[]

for line in open('Input.txt','r').readlines():
	#print line
	a.append(line.split()[0])
	m.append(line.split()[1])
	c.append(line.split()[2])

d=[[] for i in range(len(set(a)))];e=[[] for i in range(len(set(a)))];f=[[] for i in range(len(set(a)))]; j=-1

for i in range(len(a)):
	if a[i] in d[j]:
		j=j
	else:
		j=j+1
	d[j].append(a[i])
	e[j].append(m[i])
	f[j].append(c[i])
	#print j

for k in range(len(d)):
	try:
		x=np.array(e[k]).astype('float64');data=np.array(f[k]).astype('float64')
		# do fit, here with leastsq model
		minner = Minimizer(fcn2min, params, fcn_args=(x, data))
		kws  = {'options': {'maxiter':10}}
		result = minner.minimize()
	
		# calculate final result
		final = data + result.residual
	
		# write error report
		report_fit(result)
		text=fit_report(result)
		text_new=text.split()[34]+' '+text.split()[35]+' '+text.split()[36]+' '+text.split()[37]+'\n'+text.split()[41]+' '+text.split()[42]+' '+text.split()[43]+' '+text.split()[44]
	
		# try to plot results
	
		import pylab
		pylab.matplotlib.rcParams['axes.unicode_minus']=False
		pylab.matplotlib.rc('font',family='Times New Roman')
		fig=pylab.figure(num=None, figsize=(16,12), dpi=200, facecolor='w', edgecolor='k')
		fig, ax = pylab.matplotlib.pyplot.subplots()
		pylab.scatter(data, -x, s=30, label='Data')
		pylab.plot(final, -x, 'r', linewidth=3., label='Approximation curve')
		pylab.legend(loc=4)
		pylab.xlim(-0.01,max(data)+0.01)
		pylab.ylim(min(-x)-200,0)
		pylab.xlabel("Concentration [pM]")
		pylab.ylabel("Depth [m]")
		ax.annotate(text_new,xy=(0, 0), xycoords='figure fraction',xytext=(320, 110), textcoords='offset points',fontsize=12)
		file_name = "Station_"+str(d[k][0])+".png"
		fig.savefig(file_name, dpi=200)
	except:
		print d[k][0], "cannot be proceeded"

