import sys,os, math, glob,string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
ps = PorterStemmer()
#stop_words = set(stopwords.words('english')) 
vocabSize=0
totalTokensHam=0
totalTokensSpam=0
hamProb=0
spamProb=0
vocab={}
def classify(outputFileName):
    with open(outputFileName, "w", encoding="latin1") as fileHandler:
        for directoryName, directoryList, fileList in os.walk(devDirectoryPath):
            for fileName in glob.glob(os.path.join(directoryName, "*txt")):
                mailHamProb=0
                mailSpamProb=0
                try:
                    with open(fileName,"r", encoding="latin1") as fileHandler2:
                        for line in fileHandler2:
                            tokens=line.split()
                            for token in tokens:
                                token=token.strip()
                                token=ps.stem(token)
                                if token in string.punctuation:
                                    continue
                                '''if token in stop_words:
                                    continue'''
                                '''if token.isnumeric():
                                    continue'''
                                if token in vocab:
                                    values=vocab[token]
                                    if values[0]>0:
                                        mailHamProb+=math.log(values[0])
                                    if values[1]>0:
                                        mailSpamProb+=math.log(values[1])
                                else:
                                    continue
                        if hamProb>0:
                            localHamProb=math.log(hamProb)+mailHamProb
                        else:
                            localHamProb=mailHamProb
                        if spamProb>0:
                            localSpamProb=math.log(spamProb)+mailSpamProb
                        else:
                            localSpamProb=mailSpamProb
                    if localHamProb>=localSpamProb:
                        fileHandler.write("HAM "+fileName+"\n")
                    else:
                        fileHandler.write("SPAM "+fileName+"\n")        
                except:
                    continue
    return
def getVocab(modelFileName):
    with open(modelFileName, "r", encoding="latin1") as fileHandler:
        global vocabSize
        vocabSize=float(fileHandler.readline())
        global totalTokensHam
        totalTokensHam=float(fileHandler.readline())
        global totalTokensSpam
        totalTokensSpam=float(fileHandler.readline())
        global hamProb
        hamProb=float(fileHandler.readline().split()[1])
        global spamProb
        spamProb=float(fileHandler.readline().split()[1])
        for line in fileHandler:
            tokenAndValues=line.split()
            vocab[tokenAndValues[0]]=[float(tokenAndValues[1]),float(tokenAndValues[2])]
    return 
if __name__=="__main__":
    if len(sys.argv)==1:
        print("No training data")
        exit(1)
    devDirectoryPath=sys.argv[1]
    devDirectoryPath=os.path.abspath(devDirectoryPath)
    getVocab("nbmodel.txt")
    classify("nboutput.txt")
        