import numpy as np
import matplotlib.pyplot as plt

def estimate_co_eff(x,y):


    # number of observations/points
    n = np.size(x)

    #mean of x and y
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # calculating cross-deviation
    SS_xy = np.sum(y*x) - n*mean_x*mean_y

    # calculating deviation about x
    SS_xx = np.sum(x*x) - n*mean_x*mean_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = mean_y - b_1 * mean_x

    #print("b1 result is : {}".format(b_1))
    #print("b0 result is : {}".format(b_0))
    return b_0,b_1

def plot_regression_line(x,y,b):
    # plotting the actual points as scatter plot
    plt.scatter(x,y,color='m',edgecolors='blue')

    # predicted response vector
    y_pred = b[0]+b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()


def main():
    # observations/points
    # x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    # y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])

    x = np.array([0, 1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1, 0])

    b = estimate_co_eff(x,y)
    print(b)

    plot_regression_line(x,y,b)

if __name__ == "__main__":
    main()