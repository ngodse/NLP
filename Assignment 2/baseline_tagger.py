import sys
import os
import hw2_corpus_tool
import pycrfsuite

def parse(data, labelRequired):
    speaker = ""
    first_utterance = True
    features = []
    label = []
    for record in data:
        utterance = []
        if labelRequired:
            label.append(record.act_tag)
        if first_utterance:
            utterance.append("F")
            first_utterance = False
            speaker = record.speaker
        if speaker!=record.speaker:
            utterance.append("S")
        speaker = record.speaker
        if record.pos:
            for word in record.pos:
                utterance.extend(["TOKEN_" + word.token])
                utterance.extend(["POS_" + word.pos])
        else:
            utterance.append("NOWORD")
        features.append(utterance)
    return features,label
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
    featureList=[]
    labelList=[]
    allData=hw2_corpus_tool.get_data(trainDir)
    for data in allData:
        features, labels=parse(data, True)
        featureList.extend(features)
        labelList.extend(labels)
    trainer=pycrfsuite.Trainer(verbose=False)
    trainer.append(featureList, labelList)
    trainer.set_params({
        'c1': 1.0,  
        'c2': 1e-3,  
        'max_iterations': 50,  
        'feature.possible_transitions': True
    })
    trainer.train('model')
    tagger=pycrfsuite.Tagger()
    tagger.open('model')
    testData=hw2_corpus_tool.get_data(devDir)
    total=0
    correct=0
    with(open(outputFile,"w", encoding="latin1"))as writeFilePointer:
        for data in testData:
            features, labels=parse(data, False)
            preditedLabel=tagger.tag(features)
            #writeFilePointer.write("FileName=\""+os.path.basename(file)+"\"\n")
            '''for i in range(0, len(labels)):
                if(labels[i]==preditedLabel[i]):
                    correct=correct+1
                total=total+1'''
            for label in preditedLabel:
                writeFilePointer.write(label+"\n")
            writeFilePointer.write("\n")