# Computational intelligence and machine learning Assignment
2024 sem1 COMP7404

To remember the time I stayed up late writing code :).

**Introduction**

This assignment uses python 3. Do not use python 2.

## Assignment 1

**Problem 1: DFS-GSA**

**Problem 2: BFS-GSA**

**Problem 3: UCS-GSA**

**Problem 4: Greedy**

**Problem 5: A\***

**Problem 6: 8 Queens Local Search - Number of Attacks**

**Problem 7: 8 Queens Local Search - Get a Better Board**

## Assignment 2

**Problem 1: Random Pacman play against a single random Ghost**

You can expect the following characters in the file.

‘%’: Wall

‘W’: Ghost

‘P’: Pacman

‘.’: Food

‘ ’: empty Square

**Problem 2: Pacman play against a single random Ghost**

**Problem 3: Random Pacman play against up to 4 random Ghost**

**Problem 4: Pacman play against up to 4 random Ghost**

**Problem 5: Minimax Pacman play against up to 4 minimax Ghosts**

**Problem 6: Expectimax Pacman play against up to 4 random Ghosts**

<img width="953" alt="a2_evaluation standard_v3" src="https://github.com/user-attachments/assets/e46324a5-e5af-4210-89a0-de000333f097" />


## Assignment 3

**Problem 1: An MDP Episode**

**Problem 2: Policy Evaluation**

**Problem 3: Value Iteration**

**Problem 4: Q-Value TD Learning**

## Assignment 4

### **Part A: Conceptual Questions**

#### A1

Consider a Perceptron with 2 inputs and 1 output. Let the weights of the Perceptron be 𝑤1=1 and 𝑤2=1 and let the bias be 𝑤0=−1.5. 

Calculate the output of the following inputs: (0, 0), (1, 0), (0, 1), (1, 1)

#### A2

Define a perceptron for the following logical functions: AND, NOT, NAND, NOR

#### A3

The parity problem returns 1 if the number of inputs that are 1 is even, and 0 otherwise. Can a perceptron learn this problem for 3 inputs?

#### A4

Suppose that the following are a set of point in two classes:

- Class1: (1,1),(1,2),(2,1)

- Class2: (0,0),(1,0),(0,1)

Plot them and find the optimal separating line. What are the support vectors, and what is the meaning?

#### A5

Suppose that the probability of five events are 𝑃(𝑓𝑖𝑟𝑠𝑡) = 0.5, 𝑃(𝑠𝑒𝑐𝑜𝑛𝑑) = 𝑃(𝑡ℎ𝑖𝑟𝑑) = 𝑃(𝑓𝑜𝑢𝑟𝑡ℎ) = 𝑃(𝑓𝑖𝑓𝑡ℎ) = 0.125. Calculate the entropy and write down in words what this means.

#### A6

Design a decision tree that computes the logical AND function. How does it compare to the Perceptron solution?

| Height |  Hair  | Eyes  | Attractive? |
| :----: | :----: | :---: | :---------: |
| Small  | Blonde | Brown |     No      |
|  Tall  |  Dark  | Brown |     No      |
|  Tall  | Blonde | Blue  |     Yes     |
|  Tall  |  Dark  | Blue  |     No      |
| Small  |  Dark  | Blue  |     No      |
|  Tall  |  Red   | Blue  |     Yes     |
|  Tall  | Blonde | Brown |     No      |
| Small  | Blonde | Blue  |     Yes     |

#### A7

Turn the following politically incorrect data into a decision tree to classify which attributes make a person attractive, and then extract the rules. Use the Gini Impurity.HeightHairEyesAttractive?

#### A8

Suppose we collect data for a group of students in a postgraduate machine learning class with features 𝑥1 = hours studies, 𝑥2 = undergraduate GPA and label 𝑦 = receive an A. We fit a logistic regression and produce estimated weights as follows: 𝑤0=−6, 𝑤1=0.05, 𝑤2=1.

1. Estimate the probability that a student who studies for 40h and has an undergraduate GPA of 3.5 gets an A in the class

2. How many hours would the student in part 1. need to study to have a 50% chance of getting an A in the class?

#### A9

Suppose that we take a data set, divide it into equally-sized training and test sets, and then try out two different classification procedures. First we use logistic regression and get an error rate of 20% on the training data and 30% on the test data. Next we use 1-nearest neighbors (i.e., K=1) and get an average error rate (averaged over both test and training data sets) of 18%. Based on these results, which method should we prefer to use for classification of new observations? Why?

#### A10

Suppose the features in your training set have very different scales. Which algorithms discussed in class might suffer from this, and how? What can you do about it?

#### A11

If your AdaBoost ensemble underfits the training data, which hyperparameters should you tweak and how?

#### A12

What is the benefit of out-of-bag evaluation?

#### A13

What is the difference between hard and soft voting classifiers?

### Part B: Applied Questions

Solve the following questions by implementing solutions in code.

#### B1

Consider the following Perceptron code.

#### B2

In class we applied different scikit-learn classifers for the Iris data set.

In this question, we will apply the same set of classifiers over a different data set: hand-written digits.
Please write down the code for different classifiers, choose their hyper-parameters, and compare their performance via the accuracy score as in the Iris dataset.
Which classifier(s) perform(s) the best and worst, and why?

The classifiers include:

* perceptron
* logistic regression
* SVM
* decision tree
* random forest
* KNN

The dataset is available as part of scikit learn, as follows.

#### B3

Build a spam classifier:

*   Download examples of spam and ham from Apache SpamAssassin’s public datasets.
*   Unzip the datasets and familiarize yourself with the data format.
*   Split the datasets into a training set and a test set.
*   Write a data preparation pipeline to convert each email into a feature vector. Your preparation pipeline should transform an email into a (sparse) vector that indicates the presence or absence of each possible word. For example, if all emails only ever contain four words, “Hello,” “how,” “are,” “you,” then the email “Hello you Hello Hello you” would be converted into a vector [1, 0, 0, 1] (meaning [“Hello” is present, “how” is absent, “are” is absent, “you” is present]), or [3, 0, 0, 2] if you prefer to count the number of occurrences of each word.
*   You may want to add hyperparameters to your preparation pipeline to control whether or not to strip off email headers, convert each email to lowercase, remove punctuation, replace all URLs with “URL,” replace all numbers with “NUMBER,” or even perform stemming (i.e., trim off word endings; there are Python libraries available to do this).

*   Finally, try out several classifiers and see if you can build a great spam classifier, with both high recall and high precision.
