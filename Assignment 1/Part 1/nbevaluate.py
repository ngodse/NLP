import sys
guessedHam=0
guessedSpam=0
trueHam=0
trueSpam=0
rightGuessHam=0
rightGuessSpam=0
def evaluate():
    precisionHam=rightGuessHam/guessedHam
    precisionSpam=rightGuessSpam/guessedSpam
    recallHam=rightGuessHam/trueHam
    recallSpam=rightGuessSpam/trueSpam
    F1Ham=(2*precisionHam*recallHam)/(precisionHam+recallHam)
    F1Spam=(2*precisionSpam*recallSpam)/(precisionSpam+recallSpam)
    
    print("Spam Precision: "+str(precisionSpam))
    print("Spam Recall: "+str(recallSpam))
    print("Spam F1 Score: "+str(F1Spam))
    print("Ham Precision: "+str(precisionHam))
    print("Ham Recall: "+str(recallHam))
    print("Ham F1 Score: "+str(F1Ham))
    return 
    
def getStatistics(outputFileName):
    with open(outputFileName, "r", encoding="latin1") as fileHandler:
        for line in fileHandler:
            data=line.split()
            if(data[0]=="HAM"):
                global guessedHam
                guessedHam+=1
            elif(data[0]=="SPAM"):
                global guessedSpam
                guessedSpam+=1
            fileName=data[1].lower()
            try:
                hamIndex=fileName.rindex("ham")
            except:
                hamIndex=0
            try:
                spamIndex=fileName.rindex("spam")
            except:
                spamIndex=0
            if hamIndex>spamIndex:
                trueLabel="HAM"
                global trueHam
                trueHam+=1
                if(trueLabel==data[0]):
                    global rightGuessHam
                    rightGuessHam+=1
            else:
                trueLabel="SPAM"
                global trueSpam
                trueSpam+=1
                if(trueLabel==data[0]):
                    global rightGuessSpam
                    rightGuessSpam+=1
                
    return
if __name__=="__main__":
    if len(sys.argv)==1:
        print("No training data")
        exit(1)
    outputFileName=sys.argv[1]
    getStatistics(outputFileName)
    print(outputFileName)
    '''print("Right Guessed Ham: "+str(rightGuessHam))
    print("Right Guessed Spam: "+str(rightGuessSpam))
    print("TrueHam: "+str(trueHam))
    print("TrueSpam: "+str(trueSpam))
    print("Guessed Ham: "+str(guessedHam))
    print("Guessed Spam: "+str(guessedSpam))'''
    evaluate()
