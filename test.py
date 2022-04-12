import csv
import math
import random

numberOfClass = 3
class_index = 0
reference_dataset = []



class Node:
    def __init__(self, dataset):
        self.dataset = dataset
        self.left = None
        self.right = None
        self.bestAttr = None
        self.bestVal = None




def getFile():
    filename = open("wine.csv", "r");
    csvreader = csv.reader(filename)

    for row in csvreader:
        reference_dataset.append(row)




def count_class_rows(dataset, nClass):
    class_rows = [0] * nClass
    for row in dataset:
        class_rows[int(row[class_index]) - 1] += 1
    return class_rows


def entropy(dataset, nClass):
    entropy = 0
    totalRows = len(dataset)
    classRows = count_class_rows(dataset, nClass)

    if totalRows <= 0:
        return 0

    for x in classRows:
        prob = float(x / totalRows)
        if (prob > 0):
            entropy -= (prob * math.log(prob))

    return entropy


def Calculate_IG(parent_dataset, left_node_data, right_node_data, numClass):
    p_entropy = entropy(parent_dataset, numClass)
    left_entropy = entropy(left_node_data, numClass)
    right_entropy = entropy(right_node_data, numClass)

    parent_row = len(parent_dataset)
    left_row = len(left_node_data)
    right_row = len(right_node_data)

    infoGain = p_entropy - ((left_row / parent_row) * left_entropy + (right_row / parent_row) * right_entropy)
    return infoGain


def Split(attr, value, dataset):
    left, right = list(), list()

    for row in dataset:
        if float(row[attr]) < float(value):
            left.append(row)
        else:
            right.append(row)

    return left, right


def selectBestAttr(dataset, nClass):
    best_IG = 0.0
    best_val = 0.0
    best_attr = 0
    n_of_Attr = len(dataset[0])

    for row in dataset:
        for col in range(1, n_of_Attr):
            left, right = Split(col, row[col], dataset)
            info_gain = Calculate_IG(dataset, left, right, nClass)

            if info_gain > best_IG:
                best_IG = info_gain
                best_val = row[col]
                best_attr = col

    return best_attr, best_val


def buildTree(dataset, nOfClass):
    bestAttribute, bestValue = selectBestAttr(dataset, nOfClass)
    left, right = Split(bestAttribute, bestValue, dataset)

    leftChild = Node(left)
    rightChild = Node(right)

    if entropy(left, nOfClass) != 0 and len(left) > 1:
        leftChild = buildTree(left, nOfClass)
    if entropy(right, nOfClass) != 0 and len(right) > 1:
        rightChild = buildTree(right, nOfClass)

    node = Node(dataset)
    node.left = leftChild
    node.right = rightChild
    node.bestAttr = bestAttribute
    node.bestVal = bestValue

    return node


def printTree(root, height, nodeName):
    print(nodeName, '--Attribute ', root.bestAttr, ', Best Value ', root.bestVal)

    for i in range(height):
        print(end = ' ')

    if root.left != None:
        printTree(root.left, height + 1, 'Left')
    if root.right != None:
        printTree(root.right, height + 1, 'Right')


def findClass(root, data):
    if root.bestAttr == None:
        return root.dataset[0][0]
    if float(data[root.bestAttr]) < float(root.bestVal):
        return findClass(root.left, data)
    else:
        return findClass(root.right, data)


def test(root, testset):
    rightAns, totalTest = 0, 0
    for row in testset:
        cls_of_trainset = findClass(root, row)
        if cls_of_trainset == row[0]:
            rightAns += 1
        totalTest += 1
    return rightAns, totalTest


def divideDataset(start, end, dataset):
    trainset, testset = [], []
    i = 0
    for row in dataset:
        if i >= start and i < start + (end / 10):
            testset.append(row)
        else:
            trainset.append(row)
        i += 1
    return trainset, testset


def writeOutput(averageAccuracy, totalTest, msg):
    print('Decision Tree Grand Accuracy=' + str(averageAccuracy) + '%', 'Total Tests:' + str(totalTest))
    print([])
    print(msg, 'Testing Complete')



def generateTree():
    getFile()
    random.shuffle(reference_dataset)
    grandTotal, grandRightTotal = 0, 0

    for i in range(10):
        print('Run:', i + 1)
        print('expected', 'found', 'correctness')
        size = len(reference_dataset)
        print('reference size', size)
        trainset, testset = divideDataset(i * (size / 10), size, reference_dataset)
        print('trainset size', len(trainset))
        print('testset size', len(testset))
        root = buildTree(trainset, numberOfClass)
        rightAns, total_test = test(root, testset)
        grandTotal += total_test
        grandRightTotal += rightAns
        accuracy = (rightAns / total_test) * 100
        print('Test ' + str(i + 1) + ' Accuracy: ' + str(accuracy))
        print('Accuracy=' + str(accuracy), 'Samples=' + str(total_test))
        print('Printing Decision Tree for Test', i + 1)
        printTree(root, 0, 'Root')

    grandAccuracy = (grandRightTotal / grandTotal) * 100
    msg = '\nAccuracy: ' + str(grandAccuracy) + '%\n' + 'Total testset size: ' + str(grandTotal)
    print(msg)
    writeOutput(grandAccuracy, grandTotal, msg)


generateTree()
