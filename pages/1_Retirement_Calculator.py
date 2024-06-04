import streamlit as st
st.set_page_config(page_title="Retirement Calculator", page_icon="🧘🏼")
st.sidebar.header("🧘🏼 Retirement Calculator")
st.sidebar.write("Calculate how much how much you will need to have a comfy retirement.")
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
<div style="display: flex;align-items:center;margin-bottom:30px;"><h5 style="font-size:50px">🧘🏼</h5><div class="flex flex-col"><h5 class="gradient-text">Retirement Calculator</h5><h6>Let's calculate how much you will need to have a comfy retirement.</h6></div></div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)

with st.form(key="my_form"):
    col1, col2 = st.columns(2)

    with col1:
        current_age = st.number_input(
            "What is your current age?", min_value=20, max_value=80, value=20
        )
        retire_age = st.number_input(
            "At what age do you wish to retire?",
            min_value=40,
            max_value=80,
            value=55,
        )
        live_age = st.number_input(
            "How long do you wish to live?", min_value=70, max_value=100, value=80
        )
        retire_income = st.number_input(
            "What monthly income do you hope to have when you retire? Enter the value in Ringgit Malaysia.",
            min_value=5000.00,
            value=5000.00,
            step=500.00,
        )

    with col2:
        inflation_rate_input = st.number_input(
            "Inflation rate (%)?",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
        )
        annual_roi = st.number_input(
            "What is the annual rate of return of your investment? (%)",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
        )

    submitted = st.form_submit_button("Submit", use_container_width=True)

    if submitted:
        if all(
            value != 0
            for value in [
                current_age,
                retire_age,
                live_age,
                retire_income,
                inflation_rate_input,
            ]
        ):
            years_to_retire = retire_age - current_age
            years_of_retire = live_age - retire_age
            inflation_rate = inflation_rate_input
            retire_monthly_income = (
                retire_income * (1 + inflation_rate / 100) ** years_to_retire
            )
            total_savings_needed = 0
            for year in range(1, years_of_retire + 1):
                yearly_expenditure = (
                    retire_monthly_income
                    * 12
                    * (1 + inflation_rate / 100) ** (year - 1)
                )
                total_savings_needed += yearly_expenditure

            with st.spinner(text="In progress"):
                st.success(
                    f"Based on inflation rate of {inflation_rate}%, your monthly expenditure at {retire_age} years old will be RM {retire_monthly_income:,.2f}.\n\n By the age of {retire_age} years old, you'll need to have RM {total_savings_needed:,.2f} to enjoy your retirement until {live_age} years old."
                )
        else:
            st.error("Nilai tidak boleh nol")
