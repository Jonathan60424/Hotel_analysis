# Hotel IQ

Hotel booking analytics dashboard, built on a real 2017 to 2019 booking dataset covering City Hotel and Resort Hotel.

Python 3.8+ | Streamlit 1.28+ | Pandas | Dataset: 85,962 cleaned bookings

## Project Overview

Hotel IQ is a data analytics dashboard that investigates hotel booking and cancellation behaviour. It answers three core business questions:

- Which hotel type do customers book most often?
- Does length of stay affect the cancellation rate?
- Does lead time (the gap between booking and arrival) affect the cancellation rate?

## Data Cleaning

The raw dataset (119,390 rows) is cleaned automatically on load:

- Removed 33,261 duplicate rows
- Removed 165 bookings with zero total guests
- Removed invalid `adr` values (negative, or extreme outliers over $1,000)
- Filled missing `children`, `city`, `agent`, and `company` values
- Recategorised "Undefined" meal entries as "No Meal"
- Added a `total_nights` column (weekend nights + weekday nights)

Final cleaned dataset: 85,962 rows, 0 missing values.

## Pages

- **Overview** — key metrics, monthly booking trend, hotel type split, cancellation by lead time and stay length
- **Bookings** — monthly breakdown by hotel type, market segment, deposit type, special requests
- **Cancellations** — deep dive into cancellation drivers (lead time, stay length, deposit type, repeat guests)
- **Guests** — guest composition, repeat guest rate, special requests
- **Reports** — plain-language summary and business recommendations
- **Chat** — leave a note or question about the dashboard

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
hotel_dashboard/
├── app.py              # Main Streamlit app (UI, pages, navigation)
├── utils.py             # Data loading, cleaning, and metric computation
├── data/
│   └── hotel_bookings_data.csv   # Raw dataset (cleaned automatically on load)
├── requirements.txt
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Author

**ubai756**

- GitHub: [@ubai756](https://github.com/ubai756)
