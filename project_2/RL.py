# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()
	
class finiteMDP:

    def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):
        self.nS = nS
        self.nA = nA
        self.gamma = gamma
        self.Q = np.zeros((self.nS,self.nA))
        self.P = P
        self.R = R
        self.absorv = absorv
        self.alpha=0.2
        # completar se necessario
        
            
    def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
        #nao alterar
        traj = np.zeros((n,4))
        x = x0
        J = 0
        for ii in range(0,n):
            a = self.policy(x,poltype,polpar)
            r = self.R[x,a]
            y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0]
            traj[ii,:] = np.array([x, a, y, r])
            J = J + r * self.gamma**ii
            if self.absorv[x]:
                y = x0
            x = y
        
        return J,traj


    def VI(self):
        #nao alterar
        nQ = np.zeros((self.nS,self.nA))
        while True:
            self.V = np.max(self.Q,axis=1) 
            for a in range(0,self.nA):
                nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
            err = np.linalg.norm(self.Q-nQ)
            self.Q = np.copy(nQ)
            if err<1e-7:
                break
            
        #update policy
        self.V = np.max(self.Q,axis=1) 
        #correct for 2 equal actions
        self.Pol = np.argmax(self.Q, axis=1)
                    
        return self.Q,  self.Q2pol(self.Q)

            
    def traces2Q(self, trace):
        self.Q=np.zeros((self.nS,self.nA))
        auxQ=np.zeros((self.nS,self.nA))
        while True:
            for i in trace:
                x=max(self.Q[int(i[2]),:])
                auxQ[int(i[0]),int(i[1])]=auxQ[int(i[0]),int(i[1])]+self.alpha*(i[3]+self.gamma*x-auxQ[int(i[0]),int(i[1])])
            diff=np.linalg.norm(self.Q-auxQ)
            self.Q=np.copy(auxQ)
            if diff<0.001:
                break
        return self.Q
    
    def policy(self, x, poltype = 'exploration', par = []):
        # implementar esta funcao
        
        if poltype == 'exploitation':
            a=np.argmax(par[x])
            
        elif poltype == 'exploration':
            a=random.randint(0,self.nA-1)

                

        
        return int(a)
    
    def Q2pol(self, Q, eta=5):
        # implementar esta funcao
        return np.exp(eta*Q)/np.dot(np.exp(eta*Q),np.array([[1,1],[1,1]]))


            