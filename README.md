Project description:

Hotel IQ is a hotel booking analytics dashboard built with Python and Streamlit, analyzing a real-world dataset of 119,390 hotel bookings from 2017–2019 across City Hotel and Resort Hotel properties.

What it does:

Cleans the raw dataset (removes ~33,000 duplicate rows, invalid rates, zero-guest bookings, and standardizes missing/undefined values), landing at 85,962 verified records
Answers three core business questions: which hotel type is booked more often, whether longer stays affect cancellation rates, and whether booking lead time affects cancellation rates
Visualizes booking trends by month, cancellation rates by lead time and stay length, market segment breakdown, deposit type risk, guest composition, and more
Ends with a plain-language business recommendations page aimed at a non-technical hotel manager

Design:
A custom dark navy "glass" UI — semi-transparent blurred cards, a mouse-tracked light-refraction hover effect, animated chart transitions, and a left sidebar with six navigable pages (Overview, Bookings, Cancellations, Guests, Charts, Reports).

Tech stack:
Python, Streamlit, pandas, custom embedded HTML/CSS/JS for the visual theme.

