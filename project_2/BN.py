# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

import numpy as np

class Node():
    def __init__(self, prob, parents = []):
        self.parents = parents 
        if len(parents) == 0:
            self.prob = prob[0]
        else: 
            self.prob = prob
    
    def computeProb(self, evid):
        prob = self.prob
        # select through the levels of indirection
        for p in self.parents:
            # parent boolean value index
            idx = evid[p] 
            prob = prob[idx]

        return np.array([1 - prob, prob])
    
class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob

    def computePostProb(self, evid):
        def generate_evid(new_evid):
            """
                Generates every combination for evid, substituting the unknown values
                (i.e. []) for 1 and 0 
            """
            for i in range(len(new_evid)):
                if new_evid[i] == []:
                    return generate_evid(new_evid[0:i] + (0,) + new_evid[i + 1:]) + generate_evid(new_evid[0:i] + (1,) + new_evid[i + 1:])
            
            return (new_evid,)

        target_idx = evid.index(-1)
        prob = 0
        normalize = 0

        # compute joint probability for the unknown values
        evid_list = generate_evid(evid)
        for e in evid_list:
            # calculate for both target = True and target = False
            e = e[0:target_idx] + (1,) + e[target_idx + 1:]
            prob += self.computeJointProb(e)
            e = e[0:target_idx] + (0,) + e[target_idx + 1:]
            normalize += self.computeJointProb(e)
        
        # return the normalized result
        return prob / (prob + normalize)
        
        
    def computeJointProb(self, evid):
        joint_prob = 1
        for i in range(len(self.prob)):
            # compute the prob
            c_prob = self.prob[i].computeProb(evid)
            # select the right prob according to evid
            joint_prob *= c_prob[evid[i]]

        return joint_prob