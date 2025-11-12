# IS–LM Model Simulation

This Python script implements an interactive IS–LM macroeconomic model using **Streamlit** and **Matplotlib**.  

## Features
- Visualizes the **IS curve** and **LM curve** for a closed economy.
- Calculates and displays the **equilibrium income (Y\*)** and **interest rate (r\*)**.
- Provides a **sidebar interface** for adjusting key parameters:
  - Marginal propensity to consume (α)
  - Autonomous consumption (C₀)
  - Autonomous investment (I₀)
  - Interest sensitivity of investment (b)
  - Government expenditure (G)
  - Nominal money supply (M)
  - Income sensitivity of money demand (k)
  - Interest sensitivity of money demand (h)
  - Price level (P)
  - Taxes (T)

## Usage
Run the script with Streamlit:
```bash
**streamlit run "ISLM Analysis/ISLM.py"**
or
**cd "ISLM Analysis"
streamlit run ISLM.py**
