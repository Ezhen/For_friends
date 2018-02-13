#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on May 20/05/2017
Author: Evgeny Ivanov
"""

#from __future__ import unicode_literals
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from lmfit.printfuncs import *
import numpy as np

# Please specify here a number of rows you would like to proceed
begin=1; number_r=20

# Constants of the equation
r=8.314 ; t=273.0 ; mt=0.00025; g=-65000

# Initial guesses and constrains for the other three parameters, m,n,u.
params = Parameters()
params.add('n', value=0.7, min=0.5, max=1)
params.add('u', value= 0.7, min=0.5,max=1)
params.add('m', value= 7000., min=0.5,max=100000)

# Define objective function: returns the array to be minimized
def fcn2min(params, y, zz, x):
    n = params['n']
    u = params['u']
    m = params['m']
    model = n + u * (((2*(np.exp((-(g+m*x))/(r*(t+zz)))*(mt)))+1-np.sqrt(4*(np.exp((-(g+m*x))/(r*(t+zz)))*(mt))+1))/(2*np.power((np.exp((-(g+m*x))/(r*(t+zz)))*(mt)),2)))
    return model - x

f = [[] for x in xrange(0,number_r-1)]; k=0; z=[]

# I create a list with concentrations
y=open('20170404_prometheus_lyso_fib_20_60_ratiounfolding.txt','r').readlines()[0].split()[2:]

# This algorythm reads the tabulated version of your csv file. I resaved it as a text file with tabulation, cause I prefer this format
for line in open('20170404_prometheus_lyso_fib_20_60_ratiounfolding.txt','r').readlines()[1:number_r]:
	z.append(float(line.split()[0]))
	for i in range(len(line.split())-1):
		f[k].append(line.split()[i+1])
	k=k+1

# Final plotting
for k in range(len(f)):
		y=np.array(y).astype('float64');x=np.array(f[k]).astype('float64')
		# do fit, here with leastsq model
		minner = Minimizer(fcn2min, params,  fcn_args=(y, z[k], x))
		kws  = {'options': {'maxiter':10}}
		result = minner.minimize()
	
		# calculate final result
		final = x + result.residual
	
		# write error report
		report_fit(result)
		text=fit_report(result)
		text_new='Temperature:'+' '+str(z[k])+' [C]'+'\n'+text.split()[34]+' '+text.split()[35]+' '+text.split()[36]+' '+text.split()[37]+'\n'+text.split()[41]+' '+text.split()[42]+' '+text.split()[43]+' '+text.split()[44]+'\n'+text.split()[48]+' '+text.split()[49]+' '+text.split()[50]+' '+text.split()[51]

		# try to plot results
	
		import pylab
		pylab.matplotlib.rcParams['axes.unicode_minus']=False
		pylab.matplotlib.rc('font',family='Times New Roman')
		fig=pylab.figure(num=None, figsize=(16,12), dpi=200, facecolor='w', edgecolor='k')
		fig, ax = pylab.matplotlib.pyplot.subplots()
		pylab.scatter(x, y, s=30, label='Data')
		pylab.plot(final, y, 'r', linewidth=3., label='Approximation curve')
		pylab.legend(loc=4)
		#pylab.xlim(-0.01,max(x)+0.01)
		pylab.ylim(0,7.7)
		pylab.xlabel("Concentration [units]")
		pylab.ylabel("Lyso [units]")
		ax.annotate(text_new,xy=(0, 0), xycoords='figure fraction',xytext=(330, 110), textcoords='offset points',fontsize=12)
		file_name = str(k+1)+"_Temp_"+str(z[k])+".png"
		fig.savefig(file_name, dpi=200)

		
