import uuid
import streamlit as st
from mixpanel import Mixpanel

st.set_page_config(page_title="Financial Goal Calculator", page_icon="💹")
st.sidebar.header("💹 Financial Goal Calculator")
st.sidebar.write("Calculate how much how much you will need to achieve your goal.")
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
<div style="display: flex;align-items:center;margin-bottom:30px;"><h5 style="font-size:50px">💹</h5><div class="flex flex-col"><h5 class="gradient-text">Financial Goal Calculator</h5><h6>Let's calculate how much you will need to reach your goal.</h6></div></div>
"""

mp = Mixpanel(st.secrets['mixpanel']['token'])

user_id = str(uuid.uuid4())

# Track a page view
mp.track(user_id, 'Page View', {
    'page': 'Financial Goal Calculator'
})

st.markdown(gradient_text_html, unsafe_allow_html=True)

with st.form(key="my_form"):
    col1, col2 = st.columns(2)

    with col1:
        goal_value = st.number_input(
            "How much is your current goal valued at? Enter the value in Ringgit Malaysia",
            min_value=10000,
            value=200000,
        )
        current_savings = st.number_input(
            "How much do you already have saved up for this? Enter the value in Ringgit Malaysia.",
            min_value=0,
            value=5500,
        )
        timeframe = st.number_input(
            "What is your timeframe for achieving this goal? Enter the value in months.",
            min_value=1,
            value=12,
        )
        interest_rate = st.number_input(
            "Interest rate (%)?",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
        )

    with col2:
        monthly_contribution = st.number_input(
            "How much do you contribute to this goal monthly? Enter the value in Ringgit Malaysia.",
            min_value=0,
            value=3000,
        )

    submitted = st.form_submit_button("Submit", use_container_width=True)

    if submitted:
        if all(
            value != 0
            for value in [
                goal_value,
                current_savings,
                timeframe,
                interest_rate,
                monthly_contribution,
            ]
        ):
            required_monthly_savings = (goal_value - current_savings * (1 + interest_rate / 12) ** timeframe) / timeframe
            total_savings_needed = required_monthly_savings - monthly_contribution

            with st.spinner(text="In progress"):
                st.success(
                    f"Based on interest rate of {interest_rate}% and current savings of RM {current_savings}, to reach your goal valued at RM {goal_value} in {timeframe} months, it would take RM {required_monthly_savings:,.5g} per month saved. Accounting for your current monthly contributions, you only need to save RM {total_savings_needed:,.5g} more per month."
                )
        else:
            st.error("Nilai tidak boleh nol")
