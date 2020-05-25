import numpy as np
from random import randint
import math


class Particule:

    def __init__(self,n,v_max,mesure):
        self.mesure=mesure
        self.size=n
        self.position =  np.random.choice(2,n,p=[0.98, 0.02]) # scince 2% of our data is 1 in the dataset this can depend on the data
        # if you are using some small dataset with a lot of 1 then you may use  diffrent parameter for the p
        self.pBest = self.position
        self.Vid = randint(0,v_max)
        self.pbestFitness=0

        self.support=0
        self.confidence=0
        self.lift = 0
        self.leverage =0
        self.conviction = 0
        self.premis=frozenset()
        self.conclusion=frozenset()
    def fitness(self,df,postion=True):
        # if the particule is a valide  X=>Y  following the condification
        if(self.validParticule()):
            supportRegle = np.array([False for _ in range(df.shape[0])])
            supportPremis = np.array([False for _ in range(df.shape[0])])

            supportConclusion = np.array([False for _ in range(df.shape[0])])

            enter = False
            firstConclusion = False
            firstPremis = False
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
                        if (not firstPremis):
                            firstPremis = True
                            # for calculation sup(X)  in X=>Y
                            supportPremis = np.array(df.iloc[:, index])
                        else:
                            # for calculation sup(X)  in X=>Y
                            supportPremis = supportPremis & np.array(df.iloc[:, index])

                    else:
                        if (not firstConclusion):
                            firstConclusion = True
                            supportConclusion = np.array(df.iloc[:, index])
                        else:
                            supportConclusion = supportConclusion & np.array(df.iloc[:, index])

            supportRegle = supportPremis & supportConclusion
            supportRegle=(supportRegle).sum() / df.shape[0]
            supportPremis=(supportPremis).sum() / df.shape[0]
            supportConclusion = (supportConclusion).sum() / df.shape[0]
            if(supportPremis!=0 and supportRegle!=0):
                 temp_confidence=(supportRegle / supportPremis)
                 temp_lift = supportRegle/(supportPremis*supportConclusion)
                 temp_leverage= supportRegle - supportPremis*supportConclusion
                 if(1-self.confidence==0):
                    temp_conviction=np.inf
            if(not postion and supportPremis!=0 and supportRegle!=0):
                self.confidence = (supportRegle / supportPremis)
                self.support = supportRegle
                self.lift = supportRegle/(supportPremis*supportConclusion)
                self.leverage = supportRegle - supportPremis*supportConclusion
                if (1 - self.confidence != 0):
                    self.conviction = (1-supportConclusion)/(1-self.confidence)



            #print("support conclusion : {}, Premis : {}, regle : {}".format(supportConclusion,supportPremis,supportRegle))

            if(supportPremis!=0 and supportRegle!=0):
                #if the lift is chosen as the fitness musure
                if(self.mesure=="confidence"):
                    return temp_confidence
                if(self.mesure=="lift"):
                    return temp_lift
                if(self.mesure=="leverage"):
                    return temp_leverage
                if(self.mesure=="conviction"):
                    return temp_conviction

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
              self.fitness(df,postion=False)
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
        #print('(', end='')
        self.premis = frozenset(premis)
        self.conclusion= frozenset(conclusion)
        #print(premis,'=>',conclusion)

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
        for i in range(0,self.pBest.size,2):
            if(self.pBest[i]==1):
                 if(self.pBest[i]!=particule.pBest[i] or self.pBest[i+1]!=particule.pBest[i+1]):
                     return False

        return True





