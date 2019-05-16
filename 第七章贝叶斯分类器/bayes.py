import numpy as np

def loaddata():
    X = np.array([[1,'S'],[1,'M'],[1,'M'],[1,'S'],
            [1,'S'],[2,'S'],[2,'M'],[2,'M'],
            [2,'L'],[2,'L'],[3,'L'],[3,'M'],
            [3,'M'],[3,'L'],[3,'L']])
    y = np.array([-1,-1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1])
    return X,y

def Train(trainset,train_labels):
    m  = trainset.shape[0] # 数据量
    n =  trainset.shape[1] # 特征数
    prior_probability = {} # 先验概率 key是类别值，value是类别的概率值
    conditional_probability = {} # 条件概率key的构造；类别，特征，特征值
    labels = set(train_labels)
    # 计算先验概率(此时没有除以总数数据量n)
    for label in labels:
        prior_probability[label] = len(train_labels[train_labels == label]) + 1
    
    # 计算条件概率
    for i in range(m):
        for j in range(n):
            # key的构造：类别，特征，特征值
            key = "{},{},{}".format(str(train_labels[i]),str(j),str(trainset[i][j]))
            if key in conditional_probability:
                conditional_probability[key] +=1
            else:
                conditional_probability[key] = 1
    conditional_probability_final = {} #因字典在循环式不能改变，固定义新字典保存值
    for key in conditional_probability:
        label = key.split(',')[0]
        conditional_probability[key]+=1
        key1 = int(key.split(',')[1])
        Ni = len(set(trainset[:,key1]))
        conditional_probability_final[key] = conditional_probability[key]/(prior_probability[int(label)]+Ni) #条件概率修正
    
    #最终的先验概率(此时除以总数据量m)
    for label in labels:
        prior_probability[label] = prior_probability[label]/(m+len(labels))
    return prior_probability,conditional_probability_final,labels

def predict(data,prior_probability,conditional_probability_final,labels):
    result = {}
    for label in labels:
        temp = 1.0
        for j in range(len(data)):
            key = "{},{},{}".format(str(label),str(j),str(data[j]))
            temp = temp*conditional_probability_final[key]
        result[label] = temp*prior_probability[label]
    return sorted(result.items(),key=lambda x: x[1],reverse=True)[0][0]
if __name__ == "__main__":
    train_x,train_y = loaddata()
    prior_probability,conditional_probability_final,labels = Train(train_x,train_y)
    y_hat = predict([2,'S'],prior_probability,conditional_probability_final,labels)
    print('y_hat = ',y_hat)