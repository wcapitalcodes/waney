import streamlit as st

st.set_page_config(page_title="Malaysian Tax Calculator", page_icon="💼")
st.sidebar.header("💼 Malaysian Tax Calculator")
st.sidebar.write("Calculate how much tax you will need to pay based on your income.")
gradient_text_html = """
<style>
 .st-emotion-cache-1c7y2kd {
                flex-direction: row-reverse;
                text-align: right;
            }
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, #8e1246, #047481);
    background: linear-gradient(to right, #8e1246, #047481);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div style="display: flex;align-items:center;margin-bottom:30px;"><h5 style="font-size:50px">💼</h5><div class="flex flex-col"><h5 class="gradient-text">Malaysian Tax Calculator</h5><h6>Let's calculate how much tax you will need to pay based on your income.</h6></div></div>
"""
st.markdown(gradient_text_html, unsafe_allow_html=True)
# Define the Malaysian tax brackets for 2023
tax_brackets = [
    (5000, 0.01),  # 1% for income up to RM 5,000
    (20000, 0.03),  # 3% for income up to RM 20,000
    (35000, 0.08),  # 8% for income up to RM 35,000
    (50000, 0.14),  # 14% for income up to RM 50,000
    (70000, 0.21),  # 21% for income up to RM 70,000
    (100000, 0.24),  # 24% for income up to RM 100,000
    (250000, 0.25),  # 25% for income up to RM 250,000
    (400000, 0.28),  # 28% for income up to RM 400,000
    (float("inf"), 0.30),  # 30% for income over RM 400,000
]
@st.experimental_dialog("What is Effective Tax Rate?")
def show_dialog():
    st.markdown(
        """
The effective tax rate is the average rate at which an individual or a corporation is taxed on their taxable income. It is calculated by dividing the total tax paid by the total taxable income. This rate provides a more accurate representation of the actual tax burden compared to marginal tax rates, which only apply to the last dollar of income.

#### Example
If an individual has a total taxable income of RM 100,000 and they pay RM 15,000 in taxes, their effective tax rate would be:


$$ {Effective Tax Rate} = \\frac{15,000}{100,000} = 0.15 \\text{ or }15 \\text{ percent} $$

#### Normal Range of Effective Tax Rates

- **Low-Income Earners**: Typically 0% to 10%
- **Middle-Income Earners**: Typically 10% to 25%
- **High-Income Earners**: Typically 25% to 40%

For corporations:
- **Small Businesses**: Typically 10% to 20%
- **Large Corporations**: Typically 20% to 30%

Factors influencing effective tax rates include tax deductions and credits, tax-advantaged accounts, income composition, and geographic location.
        """
    )

def calculate_tax(income):
    tax = 0
    previous_bracket_limit = 0

    for limit, rate in tax_brackets:
        if income > limit:
            tax += (limit - previous_bracket_limit) * rate
            previous_bracket_limit = limit
        else:
            tax += (income - previous_bracket_limit) * rate
            break

    return tax

if st.button("What is Effective Tax Rate?"):
    show_dialog()

with st.form(key="my_form"):
# Input fields for user to enter their annual income
    annual_income = st.number_input(
    "Enter your annual taxable income (RM):", min_value=0.0, step=1000.0
)
    submitted = st.form_submit_button("Calculate", use_container_width=True)

    def calculate_effective_tax_rate(tax, annual_income):
        """
        Calculates the effective tax rate as a percentage.

        Args:
            tax (float): The amount of tax paid.
            annual_income (float): The annual income.

        Returns:
            float: The effective tax rate as a percentage.
        """
        if annual_income > 0:
            effective_tax_rate = (tax / annual_income) * 100
        else:
            effective_tax_rate = ''

        return effective_tax_rate
    
    if annual_income:
        # Calculate the tax based on the input income
        tax = calculate_tax(annual_income)
        effective_tax_rate= calculate_effective_tax_rate(tax,annual_income)
        st.success(f"Your estimated tax is: RM {tax:,.2f}\n\n Your effective tax rate is: {effective_tax_rate:.2f}%")
        
        
        
