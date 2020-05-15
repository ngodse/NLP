import sys,os, glob, string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
#stop_words = set(stopwords.words('english')) 
hamDirectoryList=[]
spamDirectoryList=[]
hamFileCount=0
spamFileCount=0
totalTokensHam=0
totalTokensSpam=0
ps = PorterStemmer() 
vocab={}
def createModel(vocabSize):
    try:
        with open("nbmodel.txt","w", encoding="latin1") as file_handler:
            file_handler.write(str(vocabSize)+"\n")
            file_handler.write(str(totalTokensHam)+"\n")
            file_handler.write(str(totalTokensSpam)+"\n")
            totalFileCount=hamFileCount+spamFileCount
            file_handler.write("P(ham) "+str(hamFileCount/totalFileCount)+"\n")
            file_handler.write("P(spam) "+str(spamFileCount/totalFileCount)+"\n")
            
            for token in vocab:
                values=vocab[token]
                hamProb=(values[0]+1)/(totalTokensHam+vocabSize)
                spamProb=(values[1]+1)/(totalTokensSpam+vocabSize)
                file_handler.write(token+" "+str(hamProb)+" "+str(spamProb)+"\n")
        file_handler.close()
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
                        token=ps.stem(token)
                        if token in string.punctuation:
                            continue
                        '''if token in stop_words:
                            continue'''
                        '''if token.isnumeric():
                            continue'''
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
    
    highFreqHamTokens=sorted(vocab, key=lambda k: vocab[k][0], reverse=True)
    highFreqSpamTokens=sorted(vocab, key=lambda k: vocab[k][1], reverse=True)
    print(str(len(vocab)))
    print(str(len(vocab)*0.001))
    highFrequencyWordCount=int(len(vocab)*0.001)
    highFreqHamTokens=highFreqHamTokens[:highFrequencyWordCount]
    highFreqSpamTokens=highFreqSpamTokens[:highFrequencyWordCount]
    commonWords = list(set(highFreqHamTokens).intersection(highFreqSpamTokens))
    for word in commonWords:
        del vocab[word]
        
    createModel(len(vocab))
'''
1.Stem tokens
2. Removed all tokens from string.punctuation
3. Removed stop words from nltk

'''