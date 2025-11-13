import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import streamlit as st

st.title("IS–LM Model")

#入力UI
st.sidebar.header("Parameter Settings")
alpha = st.sidebar.slider("Marginal Propensity to Consume (α)", 0.1, 0.9, 0.7, 0.05)
C0 = st.sidebar.slider("Autonomous Consumption (C₀)", 100, 1000, 500, 50)
I0 = st.sidebar.slider("Autonomous Investment (I₀)", 100, 1000, 300, 50)
b = st.sidebar.slider("Interest Sensitivity of Investment (b)", 10, 200, 50, 10)
G = st.sidebar.slider("Government Expenditure (G)", 0, 600, 250, 50)
M = st.sidebar.slider("Nominal Money Supply (M)", 50, 600, 200, 25)
k = st.sidebar.slider("Income Sensitivity of Money Demand (k)", 0.1, 1.0, 0.5, 0.05)
h = st.sidebar.slider("Interest Sensitivity of Money Demand (h)", 1, 30, 10, 1)
P = st.sidebar.slider("Price Level (P)", 0.5, 3.0, 1.0, 0.1)
T = st.sidebar.slider("Tax (T)", 0, 200, 0, 10)

# IS曲線
def IS_curve(alpha, C0, I0, b, G, Y_min, Y_max, T=0):
    Y = np.linspace(Y_min, Y_max, 1500)
    r = (C0 - alpha*T + I0 + G - (1 - alpha)*Y) / b
    return Y, r

# LM曲線
def LM_curve(M, k, h, Y_min, Y_max, P=1):
    # monetary_supply = M / P
    # monetary_demand = k * Y - h * r
    Y = np.linspace(Y_min, Y_max, 1500)
    r = (k * Y - M/P) / h
    return Y, r

# 均衡点探索
def find_equilibrium(alpha, C0, I0, b, G, M, k, h, P=1, T=0):
    def eq(r):
        Y_IS = (C0 - alpha*T + I0 - b*r + G) / (1-alpha)
        Y_LM = (M/P + h*r)/k
        return Y_IS - Y_LM
    r_eq = fsolve(eq, 0.05)[0]
    Y_eq = (C0 - alpha*T + I0 - b*r_eq + G) / (1-alpha)
    return Y_eq, r_eq



if __name__ == "__main__":
    Y_min, Y_max = 0, 4000
    Y_IS, r_IS = IS_curve(alpha, C0, I0, b, G, Y_min, Y_max, T)
    Y_LM, r_LM = LM_curve(M, k, h, Y_min, Y_max, P)
    Y_eq, r_eq = find_equilibrium(alpha, C0, I0, b, G, M, k, h, P, T)

    fig, ax = plt.subplots(figsize=(7,5))
    ax.plot(Y_IS, r_IS, color="red", label="IS curve")
    ax.plot(Y_LM, r_LM, color="blue", label="LM curve")
    ax.scatter(Y_eq, r_eq, color="black", s=60, label=f"Equilibrium: Y={Y_eq:.0f}, r={r_eq:.2f}")
    ax.set_xlabel("Income: Y")
    ax.set_ylabel("Interest rate: r(%)")
    ax.set_title("IS–LM Model")
    ax.legend()
    ax.grid(True)
    ax.set_xlim(left=0, right=3500)
    ax.set_ylim(bottom=-1, top=20)
    st.pyplot(fig)
    st.markdown(f"**Equilibrium Income Y\*** = {Y_eq:.2f},  **Equilibrium Interest Rate r\*** = {r_eq:.3f}")

