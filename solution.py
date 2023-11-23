import numpy as np #(működik a Moodle-ben is)


def get_entropy(n_cat1, n_cat2):
    if n_cat1 == 0 or n_cat2 == 0:
        return 0.0
    else:
        total = n_cat1 + n_cat2
        one_probability = n_cat1 / total
        zero_probability = n_cat2 / total
        return -(one_probability * np.log2(one_probability) + zero_probability * np.log2(zero_probability))


def get_best_separation(features, labels):
    best_separation_feature = 0
    best_separation_value = 0
    my_features = list(zip(features, labels))
    number_of_ones = sum(1 for label in labels if label == 1)
    start_entropy = get_entropy(number_of_ones, len(labels) - number_of_ones)
    best_information_gain = -1.0
    for feature in my_features:
        for index, value in enumerate(feature[0]):
            smaller_ones = [label for feature_values, label in my_features if feature_values[index] <= value and label == 1]
            smaller_zeros = [label for feature_values, label in my_features if feature_values[index] <= value and label == 0]
            smoler = smaller_ones + smaller_zeros
            bigger_ones = [label for feature_values, label in my_features if feature_values[index] > value and label == 1]
            bigger_zeros = [label for feature_values, label in my_features if feature_values[index] > value and label == 0]
            bigger = bigger_ones + bigger_zeros
            
            smaller_entropy = get_entropy(len(smaller_ones),  len(smaller_zeros))
            bigger_entropy = get_entropy(len(bigger_ones), len(bigger_zeros))
            
            this_information_gain = start_entropy - ((len(smoler) * smaller_entropy + len(bigger) * bigger_entropy) / len(my_features))

            if this_information_gain > best_information_gain:
                best_information_gain = this_information_gain
                best_separation_value = value
                best_separation_feature = index

    return best_separation_feature, best_separation_value

def rec(features, labels):
    myFeatures = list(zip(features, labels))
    best_sep = get_best_separation(features, labels)
    
    left = list(filter(lambda x: x[0][best_sep[0]] <= best_sep[1], myFeatures))
    right = list(filter(lambda x: x[0][best_sep[0]] > best_sep[1], myFeatures))
    if len(left) == 0 or len(right) == 0:
        return labels[0]
    return node(best_sep, rec(list(map(lambda x: x[0], left)), list(map(lambda x: x[1], left))), rec(list(map(lambda x: x[0], right)), list(map(lambda x: x[1], right))))
    
class node:
    def __init__(self, sep, left, right):
        self.sep = sep
        self.left = left
        self.right = right
        
    def traverse(self, haus):
        if(haus[self.sep[0]] <= self.sep[1]):
            if(isinstance(self.left, int)):
                return self.left
            else:
                return self.left.traverse(haus)
        else:
            if(isinstance(self.right, int)):
                return self.right
            else:
                return self.right.traverse(haus)

################### 3. feladat, döntési fa implementációja ####################
def main():
    
    trainData = []
    with open("train.csv", "r") as f:
        for line in f.readlines():
            trainData.append([int(x) for x in line.split(",")])

    features = [row[:-1] for row in trainData]
    labels = [row[-1] for row in trainData]
    
    testData = []
    with open("test.csv", "r") as f:
        for line in f.readlines():
            testData.append([int(x) for x in line.split(",")])
            
    tree = rec(features, labels)
    
    res = open("results.csv", "w")
    for h in testData:
        res.write(str(tree.traverse(h)))
        res.write("\n")
    
    res.close()
        
    
    
    
    return 0
    
if __name__ == "__main__":
    main()

