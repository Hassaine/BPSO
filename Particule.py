import numpy as np
from random import randint
import math


class Particule:

    def __init__(self,n,v_max,lift):
        self.size=n
        self.position =  np.random.choice(2,n,p=[0.98, 0.02]) # scince 2% of our data is 1 in the dataset this can depend on the data
        # if you are using some small dataset with a lot of 1 then you may use  diffrent parameter for the p
        self.pBest = self.position
        self.Vid = randint(0,v_max)
        self.pbestFitness=0
        self.lift=lift

    def fitness(self,df,postion=True):
        # if the particule is a valide  X=>Y  following the condification
        if(self.validParticule()):
            supportRegle = np.array([False for _ in range(df.shape[0])])
            supportPremis = np.array([False for _ in range(df.shape[0])])
            if(self.lift):
                supportConclusion = np.array([False for _ in range(df.shape[0])])

            enter = False
            # this conditon is used when we try to get the fitness of new postion
            if(postion):
                particule=self.position
            # if we want to get the fitness fo the pbest position
            else:
                particule=self.pBest
            for i in range(0, self.size, 2):
                index = round(i / 2)
                if (particule[i] == 1):
                    if (particule[i + 1] == 0):
                        # enter the if (particule[i]==1) for the first time
                        if (not enter):
                            # for calculation sup(X)  in X=>Y
                            supportPremis = np.array(df.iloc[:, index] == 1)
                        else:
                            # for calculation sup(X)  in X=>Y
                            supportPremis = supportPremis & np.array(df.iloc[:, index] == 1)
                    elif (self.lift):

                        if (not enter):
                            # for calculation sup(Y)  in X=>Y
                            supportConclusion = np.array(df.iloc[:, index] == 1)
                        else:
                            # for calculation sup(Y)  in X=>Y
                            supportConclusion = supportConclusion & np.array(df.iloc[:, index] == 1)

                    # enter the if (particule[i]==1) for the first time
                    if (not enter):
                        # for calculation sup(X=>Y)  in X=>Y
                        supportRegle = np.array(df.iloc[:, index] == 1)
                        enter = True
                    else:
                        # for calculation sup(X=>Y)  in X=>Y
                        supportRegle = supportRegle & np.array(df.iloc[:, index] == 1)
            supportRegle=(supportRegle==True).sum() / df.shape[0]
            supportPremis=(supportPremis==True).sum() / df.shape[0]

            if(supportPremis!=0 and supportRegle!=0):
                #if the lift is chosen as the fitness musure
                if(self.lift):
                    supportConclusion=(supportConclusion==True).sum() / df.shape[0]
                    if(supportConclusion != 0):
                        return (supportRegle/(supportPremis*supportConclusion))
                    else:
                        return 0

                #else we use the support as default
                else:
                    return (supportRegle/supportPremis)*supportRegle
            else:
                return 0
        else:
            return 0

    def updatePosition(self,df):
        bestScore = self.pbestFitness
        i=0

        while(i<self.Vid):
          indice = np.random.randint(self.size)
          self.position[indice]=int(math.fabs(self.position[indice]-1))
          newScore=self.fitness(df)
          if(newScore - bestScore < 0):
              self.position[indice] = int(math.fabs(self.position[indice] - 1))

          else:
              self.pBest=self.position
              self.pbestFitness=newScore
          i+=1


    def getRule(self,columns):
        premis = []
        conclusion = []
        for i in range(0, self.size, 2):
            if (self.pBest[i] == 1):
                # if particule has the conclusion part
                if (self.pBest[i + 1] == 1):
                    conclusion.append(columns[i / 2])
                # if particule has the premis part
                else:
                    premis.append(columns[i / 2])
        print('(', end='')
        for pre in premis:
            print(pre, end=',')
        print(')=>', end=' ')
        for con in conclusion:
            print(con, end=',')

    def validParticule(self):
        validConclusion = False
        validPremis = False
        for i in range(0, self.size, 2):
            if (self.position[i] == 1):
                # if particule has the conclusion part
                if (self.position[i + 1] == 1):
                    validConclusion = True
                # if particule has the premis part
                else:
                    validPremis = True
        if (validPremis and validConclusion):
            return True
        else:
            return False

    def equal(self,particule):
        return ((self.pBest == particule.pBest) == True).sum() == self.size





