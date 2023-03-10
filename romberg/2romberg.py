import numpy as np

def trapez(f, a, b, n):

    h = (b - a) /2
    x = a

    In = f(a)
    for k in range(1, n):
        x  = x + h
        In += 2*f(x)

    return (In + f(b))*h*0.5

def romberg(f, a, b, p):
    """
    a:  lower bound of integration
    b:  upper bound
    p:  number of rows in the Romberg table
    """

    I = np.zeros((p, p))
    for k in range(0, p):

        I[k, 0] = trapez(f, a, b, 2**k)

        for j in range(0, k):
            I[k, j+1] = (4**(j+1) * I[k, j] - I[k-1, j]) / (4**(j+1) - 1)

        print(I[k,0:k+1])

    return I

"""Put the values of semi-major and semi-minor axes of the ellipse 
as a=0.04 b=0.03
Write the constants in the "func" so as not to confuse the above-mentioned upper
and lower bounds of integration
"""
if __name__ == '__main__':
    def func(x):
        return x**4 + 1/x

    p_rows = 3
    I = romberg(func, 1, 5, p_rows)
    solution = I[p_rows-1, p_rows-1]
    print(solution)

"""integrals of the second column of the table (I(1)) with a steps h/4 h/2 h/8"""
i_1_h4=I[p_rows-2][p_rows-3]
i_1_h2=I[p_rows-3][p_rows-3]
i_1_h8=I[p_rows-1][p_rows-3]

"""determination of the order of accuracy of the integrals of the second column of the table (I(1))"""
order_of_accuracy = np.log2((i_1_h4 - i_1_h2)/(i_1_h8 - i_1_h4))
print(order_of_accuracy)
