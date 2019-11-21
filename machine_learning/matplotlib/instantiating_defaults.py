import numpy as np
import matplotlib.pyplot as plt

# Create a figure of size 8x6 inches, 80 dots per inch

plt.figure(figsize=(10, 10), dpi=25)

X = np.linspace(-np.pi,np.pi,256, endpoint=True)
C, S = np.cos(X), np.sin(X)

plt.plot(X, C, color="blue", linewidth=5.0, linestyle="--")
#plt.suptitle("dfgfd")
plt.title("Sine and Cos waves")
plt.plot(X, S, color="red", linewidth=5.0, linestyle="-")
plt.show()
