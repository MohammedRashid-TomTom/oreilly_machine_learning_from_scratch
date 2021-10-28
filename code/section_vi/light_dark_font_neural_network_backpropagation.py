# Helpful resource: https://www.kaggle.com/wwsalmon/simple-mnist-nn-from-scratch-numpy-no-tf-keras/
import numpy as np
import pandas as pd

training_data = pd.read_csv("https://tinyurl.com/y2qmhfsr")
row_ct, col_ct = training_data.shape

# Learning rate controls how slowly we approach a solution
# Make it too small, it will take too long to run.
# Make it too big, it will likely overshoot and miss the solution.
L = 0.1
sample_size = 100

# Extract the input columns, scale down by 255
training_inputs = (training_data.iloc[:, 0:3].values / 255.0)
training_outputs = training_data.iloc[:, -1].values

# Build neural network with weights and biases
hidden_w = np.random.rand(3, 3)
output_w = np.random.rand(1, 3)

hidden_b = np.random.rand(3, 1)
output_b = np.random.rand(1, 1)

# Activation functions
# softplus = lambda x: np.log(1 + np.exp(x))
relu = lambda x: np.maximum(x, 0)
logistic = lambda x: 1 / (1 + np.exp(-x))
# softmax = lambda x: np.exp(x) / sum(np.exp(x))

# Derivatives of Activation functions
# d_softplus = lambda x:  np.exp(x)/(np.exp(x) + 1)
d_relu = lambda x: x > 0
d_logistic = lambda x: np.exp(-x)/(1 + np.exp(-x))**2

# Stochastic Gradient descent
def forward_prop(X):
    Z1 = hidden_w @ X + hidden_b
    A1 = relu(Z1)
    Z2 = output_w @ A1 + output_b
    A2 = logistic(Z2)
    return Z1, A1, Z2, A2

def backward_prop(Z1, A1, Z2, A2, X, Y):
    dZ2 = A2 - Y
    dW2 = 1 / row_ct * dZ2 @ A1.T
    db2 = 1 / row_ct * np.sum(dZ2)
    dZ1 = output_w.T @ dZ2 * d_relu(Z1)
    dW1 = 1 / row_ct * dZ1 @ X.T
    db1 = 1 / row_ct * np.sum(dZ1)
    return dW1, db1, dW2, db2

for i in range(100_000):

    idx = np.random.choice(row_ct, sample_size, replace=False)
    X = training_inputs[idx].transpose()
    Y = training_outputs[idx]

    Z1, A1, Z2, A2 = forward_prop(X)
    dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, X, Y)

    hidden_w -= L * dW1
    hidden_b -= L * db1
    output_w -= L * dW2
    output_b -= L * db2


# Interact and test with new colors
def predict_probability(r, g, b):
    X = np.array([[r, g, b]]).transpose() / 255
    Z1, A1, Z2, A2 = forward_prop(X)
    return A2


def predict_font_shade(r, g, b):
    output_values = predict_probability(r, g, b)
    if output_values > .5:
        return "DARK"
    else:
        return "LIGHT"


while True:
    col_ct = input("Predict light or dark font. Input values R,G,B: ")
    (r, g, b) = col_ct.split(",")
    print(predict_font_shade(int(r), int(g), int(b)))