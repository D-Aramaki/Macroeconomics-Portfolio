import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import streamlit as st

st.title("AD–AS Model")

# 入力UI
st.sidebar.header("Parameter Settings")
st.sidebar.header("AD Curve Parameter")
st.sidebar.header("Y = C₀ + α(Y - T) + I₀ - br + G")
C0 = st.sidebar.slider("Autonomous Consumption (C₀)", 100, 1000, 350, 50)
alpha = st.sidebar.slider("Marginal Propensity to Consume (α)", 0.1, 0.9, 0.7, 0.05)
I0 = st.sidebar.slider("Autonomous Investment (I₀)", 100, 1000, 600, 50)
b = st.sidebar.slider("Interest Sensitivity of Investment (b)", 10, 200, 30, 10)
G = st.sidebar.slider("Government Expenditure (G)", 0, 600, 250, 50)
T = st.sidebar.slider("Tax (T)", 0, 200, 0, 10)
st.sidebar.header("M/P = kY + hr")
M = st.sidebar.slider("Nominal Money Supply (M)", 50, 600, 200, 25)
k = st.sidebar.slider("Income Sensitivity of Money Demand (k)", 0.1, 1.0, 0.5, 0.05)
h = st.sidebar.slider("Interest Sensitivity of Money Demand (h)", 1, 30, 10, 1)
st.sidebar.header("AS Curve Parameter")
Y_bar = st.sidebar.slider("Potential Output (Ȳ)", 1000, 5000, 3000, 100)
alpha_as = st.sidebar.slider("Price Sensitivity (αᵃˢ)", 100, 1000, 500, 50)
P_e = st.sidebar.slider("Expected Price Level (Pₑ)", 1.0, 10.0, 5.0, 0.5)

# Y Range
st.sidebar.header("Plot Range: 500 ~ ")
Y_min = 500
Y_max = st.sidebar.number_input("Maximum Income (Y)", value=2500, step=100)
Y = np.linspace(Y_min, Y_max, 500)

# AD curve
def AD_P(Y, alpha, C0, I0, b, G, M, k, h, T):
    P = (M * b) / ((b*k + h * (1 - alpha)) * Y - h * C0 + alpha * h * T - h * I0 - h * G)
    P[P < 0] = np.nan
    return P

# AS curve
def AS_P(Y, Y_bar, alpha_as, P_e):
    P = P_e + (Y - Y_bar)/alpha_as
    return P

# 均衡点探索
def find_equilibrium(alpha, C0, I0, b, G, M, k, h, T, Y_bar, alpha_as, P_e, Y_min, Y_max):
    def diff(Y):
        P_ad = (M * b) / ((b*k + h * (1 - alpha)) * Y - h * C0 + alpha * h * T - h * I0 - h * G)
        P_as = P_e + (Y - Y_bar)/alpha_as
        return P_ad - P_as

    Y_guess = (Y_min + Y_max) / 2
    Y_star = fsolve(diff, Y_guess)[0]

    if Y_star < Y_min or Y_star > Y_max:
        Y_star = np.nan
        P_star = np.nan
    else:
        P_star = (M * b) / ((b*k + h * (1 - alpha)) * Y_star - h * C0 + alpha * h * T - h * I0 - h * G)
        if P_star < 0:
            P_star = np.nan

    return Y_star, P_star

# plot
def plot_ADAS(Y, alpha, C0, I0, b, G, M, k, h, T, Y_bar, alpha_as, P_e):
    P_AD = AD_P(Y, alpha, C0, I0, b, G, M, k, h, T)
    P_AS = AS_P(Y, Y_bar, alpha_as, P_e)
    Y_star, P_star = find_equilibrium(alpha, C0, I0, b, G, M, k, h, T, 
                                  Y_bar, alpha_as, P_e, Y_min, Y_max)
    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(Y, P_AD, color="orange", label="AD curve")
    ax.plot(Y, P_AS, color="cornflowerblue", label="AS curve")
    ax.scatter(Y_star, P_star, color="black", s=60, label=f"Equilibrium: Y={Y_star:.0f}, P={P_star:.2f}")
    ax.set_xlabel("Income / Output: Y")
    ax.set_ylabel("Price Level: P")
    ax.set_ylim(0, 10)
    ax.set_title("ADAS Model")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    st.markdown(f"**Equilibrium Income Y\*** = {Y_star:.2f},  **Equilibrium Price Rate P\*** = {P_star:.3f}")

if __name__ == "__main__":
  plot_ADAS(Y, alpha, C0, I0, b, G, M, k, h, T, Y_bar, alpha_as, P_e)
