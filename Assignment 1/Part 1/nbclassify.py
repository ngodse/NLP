import sys,os, math, glob
hamProb=0
spamProb=0
vocab={}
def classify(outputFileName):
    with open(outputFileName, "w", encoding="latin1") as file:
        for directoryName, directoryList, fileList in os.walk(devDirectoryPath):
            for fileName in glob.glob(os.path.join(directoryName, "*txt")):
                mailHamProb=0
                mailSpamProb=0
                try:
                    with open(fileName,"r", encoding="latin1") as file2:
                        for line in file2:
                            tokens=line.split()
                            for token in tokens:
                                token=token.strip()
                                token=token.lower()
                                if token in vocab:
                                    values=vocab[token]
                                    if values[0]>0:
                                        mailHamProb+=math.log(values[0])
                                    if values[1]>0:
                                        mailSpamProb+=math.log(values[1])
                        if hamProb>0:
                            localHamProb=math.log(hamProb)+mailHamProb
                        else:
                            localHamProb=mailHamProb
                        if spamProb>0:
                            localSpamProb=math.log(spamProb)+mailSpamProb
                        else:
                            localSpamProb=mailSpamProb
                    if localHamProb>=localSpamProb:
                        file.write("HAM\t"+fileName+"\n")
                    else:
                        file.write("SPAM\t"+fileName+"\n")        
                except:
                    continue
    return
def getVocab(modelFileName):
    with open(modelFileName, "r", encoding="latin1") as file:
        global hamProb
        hamProb=float(file.readline().split()[1])
        global spamProb
        spamProb=float(file.readline().split()[1])
        for line in file:
            tokenAndValues=line.split()
            vocab[tokenAndValues[0]]=[float(tokenAndValues[1]),float(tokenAndValues[2])]
    file.close()
    return 
if __name__=="__main__":
    if len(sys.argv)==1:
        print("No training data")
        exit(1)
    devDirectoryPath=sys.argv[1]
    devDirectoryPath=os.path.abspath(devDirectoryPath)
    getVocab("nbmodel.txt")
    classify("nboutput.txt")
        