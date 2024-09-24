######## A Healthcare Domain Chatbot to simulate the predictions of a General Physician ########
######## A pragmatic Approach for Diagnosis ############

# Importing the necessary libraries for the chatbot and machine learning
from sklearn.tree import _tree, DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

# Importing the dataset containing symptoms and their associated diseases
training_dataset = pd.read_csv(r'E:\medecro-healthhack-project\Testing.csv')
# Same data is used for testing for simplicity
test_dataset = pd.read_csv(r'E:\medecro-healthhack-project\Testing.csv')

# Slicing the dataset to separate symptoms (X) and diseases (y)
# Features: Symptoms from the dataset
X = training_dataset.iloc[:, 0:132].values
y = training_dataset.iloc[:, -1].values     # Target: The prognosis/disease

# Grouping the dataset to remove redundant information by taking the max of each symptom per disease
dimensionality_reduction = training_dataset.groupby(
    training_dataset['prognosis']).max()

# Encoding the string values of diseases to integer constants for easier processing by the classifier
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(y)

# Splitting the dataset into training and testing sets (75% training, 25% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)

# Training a Decision Tree Classifier on the symptom-disease dataset
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving column names for feature importance and question formulation later
cols = training_dataset.columns[:-1]

# Checking the importance of each symptom to help determine which symptoms contribute most to a diagnosis
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]  # Sorting symptoms by importance
features = cols  # Storing the symptoms as features

# Function to simulate the chatbot interaction


def execute_bot():
    print("Please reply with yes/Yes or no/No for the following symptoms")

    # Function to print the disease based on the decision tree node value
    def print_disease(node):
        node = node[0]
        val = node.nonzero()  # Find non-zero values indicating the disease
        # Decode disease from numerical label to string
        disease = labelencoder.inverse_transform(val[0])
        return disease

    # Function to traverse the decision tree and ask symptom-based questions
    def tree_to_code(tree, feature_names):
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature
        ]  # Getting feature names from the decision tree
        symptoms_present = []  # To track symptoms that the user has

        # Recursive function to traverse the tree
        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:  # If the node is not a leaf
                name = feature_name[node]
                threshold = tree_.threshold[node]
                print(name + " ?")  # Asking the user about a symptom
                ans = input().lower()  # Collecting user input (yes/no)
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if val <= threshold:
                    # Go left in the tree if symptom absent
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    # Record the symptom as present
                    symptoms_present.append(name)
                    # Go right in the tree if symptom present
                    recurse(tree_.children_right[node], depth + 1)
            else:
                # If the node is a leaf, diagnose the disease
                present_disease = print_disease(tree_.value[node])
                print("You may have " + present_disease[0])

                # Retrieve expected symptoms of the diagnosed disease
                red_cols = dimensionality_reduction.columns
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero(
                )]

                # Output symptoms and confidence level of the diagnosis
                print("Symptoms present: " + str(list(symptoms_present)))
                print("Expected symptoms: " + str(list(symptoms_given)))
                confidence_level = (
                    1.0 * len(symptoms_present)) / len(symptoms_given)
                print("Confidence level: " + str(confidence_level))

                # Suggest a doctor based on the diagnosed disease
                print('The model suggests:')
                row = doctors[doctors['disease'] == present_disease[0]]
                print('Consult: ', str(row['name'].values))
                print('Visit: ', str(row['link'].values))

        recurse(0, 1)  # Start the tree traversal from the root

    tree_to_code(classifier, cols)


# Loading a dataset of doctors for disease consultation
doc_dataset = pd.read_csv(
    r'E:\medecro-healthhack-project\doctors_dataset.csv', names=['Name', 'Description'])

# Creating a DataFrame to store doctor names and links based on disease
diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']
doctors['disease'] = diseases['prognosis']

# Example of querying the doctor database for AIDS
record = doctors[doctors['disease'] == 'AIDS']
record['name']  # Doctor's name for AIDS
record['link']  # Link for consultation for AIDS

# Run the chatbot to simulate the prediction process
execute_bot()
