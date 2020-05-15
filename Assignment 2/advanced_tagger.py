import sys
import pycrfsuite
import hw2_corpus_tool
import os

def parse(data):
    speaker = ""
    firstUtterance = True
    features=[]
    label=[]
    for record in data:
        utterance = []
        label.append(record.act_tag)
        if firstUtterance:
            utterance.append("F")
            firstUtterance = False
            speaker = record.speaker
        if speaker != record.speaker :
            utterance.append("S")
        speaker = record.speaker
        if record.pos:
            tokenPrev = record.pos[0].token
            posPrev = record.pos[0].pos
            utterance.append("TOKEN_"+tokenPrev)
            utterance.append("POS_"+posPrev)
            for i, word in enumerate(record.pos):
                utterance.append("TOKENPREV"+"_"+tokenPrev+"_"+word.token)
                utterance.append("POSPREV"+"_"+posPrev+"_"+word.pos)
                utterance.append("TOKEN_"+word.token)
                utterance.append("POS_"+word.pos)
                utterance.append("TOKENLEN_"+str(len(word.token)))
                utterance.append("POSLEN_"+str(len(word.pos)))
                tokenPrev = word.token
                posPrev = word.pos
                try:
                    utterance.append("TOKENCOMBINATION_"+record.pos[i-1].token+"_"+record.pos[i].token+"_"+record.pos[i+1].token)
                    utterance.append("POSCOMBINATION_"+record.pos[i-1].pos+"_"+record.pos[i].pos+"_"+record.pos[i+1].pos)
                except:
                    pass
        else:
            utterance.append("NOWORD")    
        features.append(utterance)
    features[len(features) - 1].append("LAST")
    return features, label
def calculate_accuracy(correct,total):
    accuracy = (correct / total) * 100
    return accuracy

if __name__=="__main__":
    if (len(sys.argv)<4):
        print("Invalid input")
        sys.exit(1);
    trainDir=os.path.abspath(sys.argv[1])
    devDir=os.path.abspath(sys.argv[2])
    outputFile=sys.argv[3]
    featureList = []
    labelList = []
    allData=hw2_corpus_tool.get_data(trainDir)
    for data in allData:
        features, labels=parse(data)
        featureList.extend(features)
        labelList.extend(labels)
    trainer = pycrfsuite.Trainer(verbose=False)
    trainer.append(featureList, labelList)
    trainer.set_params({
        'c1': 1.0,  
        'c2': 1e-3,  
        'max_iterations': 50,  
        'feature.possible_transitions': True
    })
    trainer.train('model')
    tagger = pycrfsuite.Tagger()
    tagger.open('model')
    #testFiles = glob.glob(os.path.join(devDir, "*.csv"))
    testData=hw2_corpus_tool.get_data(devDir)
    total=0
    correct=0
    
    with(open(outputFile,"w", encoding="latin1"))as writeFilePointer:
        for data in testData:
            features, labels=parse(data)
            preditedLabel=tagger.tag(features)
            #writeFilePointer.write("FileName=\""+os.path.basename(file)+"\"\n")
            for i in range(0, len(labels)):
                if(labels[i]==preditedLabel[i]):
                    correct=correct+1
                total=total+1
            for label in preditedLabel:
                writeFilePointer.write(label+"\n")
            writeFilePointer.write("\n")  
    print("Advanced correct")
    print(correct)        
    print("Advanced Total")
    print(total)
    print("Accuracy of Advanced")
    print(calculate_accuracy(correct, total))      
