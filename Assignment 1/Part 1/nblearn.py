import sys,os, glob
hamDirectoryList=[]
spamDirectoryList=[]
hamFileCount=0
spamFileCount=0
totalTokensHam=0
totalTokensSpam=0
vocab={}
def createModel(vocabSize):
    try:
        with open("nbmodel.txt","w", encoding="latin1") as file:
            totalFileCount=hamFileCount+spamFileCount
            file.write("P(ham) "+str(hamFileCount/totalFileCount)+"\n")
            file.write("P(spam) "+str(spamFileCount/totalFileCount)+"\n")
            
            for token in vocab:
                values=vocab[token]
                hamProb=(values[0]+1)/(totalTokensHam+vocabSize)
                spamProb=(values[1]+1)/(totalTokensSpam+vocabSize)
                file.write(token+" "+str(hamProb)+" "+str(spamProb)+"\n")
        file.close()
    except:
        pass
    return

def getVocab(className, directoryList):
    for directory in directoryList:
        for fileName in glob.glob(os.path.join(directory,'*txt')):
            try:
                lines=[line for line in open(fileName, "r", encoding="latin1")]
                for line in lines:
                    tokens=line.split()
                    if className=="ham":
                        global totalTokensHam
                        totalTokensHam+=len(tokens)
                    elif className=="spam":
                        global totalTokensSpam
                        totalTokensSpam+=len(tokens)
                    for token in tokens:
                        token=token.strip()
                        token=token.lower()
                        if token in vocab:
                            if className=="ham":
                                values=vocab[token]
                                values[0]+=1
                                vocab[token]=values
                            elif className=="spam":
                                values=vocab[token]
                                values[1]+=1
                                vocab[token]=values
                        else:
                            if className=="ham":
                                vocab[token]=[1, 0]
                            elif className=="spam":
                                vocab[token]=[0,1]
            except:
                continue
    return
def findDir():
    for directoryName, directoryList, fileList in os.walk(trainingFolderPath):
        if os.path.basename(directoryName).strip().lower()=="ham":
            hamDirectoryList.append(directoryName)
            global hamFileCount
            #counting number of files
            hamFileCount+=len(glob.glob(os.path.join(directoryName, '*txt'))) 
        elif os.path.basename(directoryName).strip().lower()=="spam":
            spamDirectoryList.append(directoryName)
            global spamFileCount
            spamFileCount+=len(glob.glob(os.path.join(directoryName, '*txt'))) 
    return
if __name__ =='__main__':
    if(len(sys.argv)==1):
        print('Folder not found')
        sys.exit(1);
    trainingFolderPath=sys.argv[1]
    findDir()
    if hamFileCount==0 or spamFileCount==0:
        print('No sufficient training data')
        sys.exit(1)
    getVocab("ham", hamDirectoryList)
    getVocab("spam", spamDirectoryList)
    if totalTokensHam==0 or totalTokensSpam==0:
        print('No sufficient training data')
        sys.exit(1)
    createModel(len(vocab))