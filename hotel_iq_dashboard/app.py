"""
Hotel IQ - Hotel Booking Analytics Dashboard
Run with: streamlit run app.py
"""

import textwrap
import streamlit as st
import streamlit.components.v1 as components
import utils


def _h(html: str) -> str:
    """Collapse a multi-line HTML string to single lines with no leading
    whitespace and no blank lines. Streamlit's markdown parser treats an
    indented line, or a line after a blank line, as a code block instead
    of HTML -- this keeps every block safe to render with unsafe_allow_html.
    """
    lines = [line.strip() for line in textwrap.dedent(html).splitlines()]
    return "".join(line for line in lines if line)

st.set_page_config(
    page_title="Hotel IQ | Booking Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------
df = utils.load_and_clean()
kpi = utils.overview_kpis(df)

# ----------------------------------------------------------------------
# Global CSS (navy glass theme, hover refraction effect, layout)
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .stApp {
        background: #00040c;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
        max-width: 1400px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes drawLine {
        from { stroke-dashoffset: 700; }
        to { stroke-dashoffset: 0; }
    }
    @keyframes growBar {
        from { width: 0; }
        to { width: var(--w); }
    }

    .glass-card {
        --mx: 50%;
        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(16px) saturate(140%);
        -webkit-backdrop-filter: blur(16px) saturate(140%);
        border: 0.5px solid rgba(255,255,255,0.1);
        border-top-color: rgba(255,255,255,0.22);
        border-radius: 14px;
        animation: fadeUp 0.5s ease both;
        transition: backdrop-filter 0.35s ease, border-color 0.35s ease,
                    box-shadow 0.35s ease, transform 0.35s ease;
        position: relative;
        z-index: 1;
        overflow: hidden;
        padding: 16px;
        margin-bottom: 14px;
        height: calc(100% - 14px);
        box-sizing: border-box;
    }

    /* Equal-height cards within the same row */
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch;
    }
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    div[data-testid="column"] > div {
        display: flex;
        flex-direction: column;
        flex: 1;
    }
    div[data-testid="column"] > div > div[data-testid="stMarkdown"] {
        display: flex;
        flex: 1;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: -40%; bottom: -40%;
        left: calc(var(--mx) - 60px);
        width: 60px;
        background: linear-gradient(100deg,
            transparent 0%, rgba(255,255,255,0.32) 45%,
            rgba(255,255,255,0.5) 50%, rgba(255,255,255,0.32) 55%, transparent 100%);
        transform: skewX(-18deg);
        opacity: 0;
        transition: opacity 0.25s ease;
        pointer-events: none;
    }
    .glass-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 14px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.12),
                    inset 0 -1px 0 rgba(255,255,255,0.03);
        pointer-events: none;
    }
    .glass-card:hover {
        backdrop-filter: blur(22px) saturate(170%);
        -webkit-backdrop-filter: blur(22px) saturate(170%);
        border-color: rgba(160,195,255,0.4);
        box-shadow: 0 12px 32px rgba(30,80,200,0.22);
        transform: translateY(-2px);
    }
    .glass-card:hover::before { opacity: 1; }

    .g-label { font-size: 12px; color: #7a8598; margin: 0 0 2px; position: relative; z-index: 1; }
    .g-val { font-size: 22px; font-weight: 600; margin: 0; color: #eef2f8; position: relative; z-index: 1; }
    .g-sub { display: flex; justify-content: space-between; margin-top: 10px;
             font-size: 11px; color: #7a8598; position: relative; z-index: 1; }
    .g-sub b { color: #eef2f8; font-size: 13px; }
    .g-title { font-size: 13px; color: #7a8598; position: relative; z-index: 1; }
    .g-caption { font-size: 11px; color: #7a8598; margin: 2px 0 8px; position: relative; z-index: 1; }

    .bar-row { margin-bottom: 8px; position: relative; z-index: 1; }
    .bar-label-row { display: flex; justify-content: space-between; font-size: 12px;
                      margin-bottom: 3px; color: #eef2f8; }
    .bar-track { height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; }
    .bar-fill { height: 100%; border-radius: 3px; animation: growBar 1s ease forwards; width: 0; }

    .page-header { font-size: 17px; font-weight: 600; color: #eef2f8; margin: 0 0 2px; }
    .page-sub { font-size: 12px; color: #7a8598; margin: 0 0 16px; }

    /* Sidebar nav buttons */
    div[data-testid="stSidebar"] {
        background: #00040c;
        border-right: 0.5px solid rgba(255,255,255,0.08);
    }
    div[data-testid="stSidebar"] .stButton button {
        width: 100%;
        background: transparent;
        border: none;
        text-align: left;
        color: #7a8598;
        font-size: 13px;
        padding: 10px 12px;
        border-radius: 8px;
        transition: background 0.2s ease, color 0.2s ease;
    }
    div[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.06);
        color: #eef2f8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def glass_hover_script():
    """
    st.markdown() inserts raw HTML via innerHTML, and browsers never execute
    <script> tags inserted that way -- so a script placed via st.markdown()
    silently never runs. components.html() renders in a real iframe that
    DOES execute scripts; since it's same-origin, the script can reach into
    window.parent.document to attach the hover effect to the actual page.
    """
    components.html(
        """
        <script>
        function attachGlass() {
            var doc = window.parent.document;
            doc.querySelectorAll('.glass-card').forEach(function(card) {
                if (card.dataset.glassBound) return;
                card.dataset.glassBound = "1";
                card.addEventListener('mousemove', function(e) {
                    var r = card.getBoundingClientRect();
                    var x = ((e.clientX - r.left) / r.width) * 100;
                    card.style.setProperty('--mx', x + '%');
                });
            });
        }
        attachGlass();
        var target = window.parent.document.body;
        new MutationObserver(attachGlass).observe(target, {childList: true, subtree: true});
        </script>
        """,
        height=0,
    )


def kpi_card(label, value, sub_left_label, sub_left_val, sub_right_label, sub_right_val, delay=0.0):
    return _h(f"""
    <div class="glass-card" style="animation-delay:{delay}s;">
        <p class="g-label">{label}</p>
        <p class="g-val">{value}</p>
        <div class="g-sub">
            <span>{sub_left_label}<br><b>{sub_left_val}</b></span>
            <span>{sub_right_label}<br><b>{sub_right_val}</b></span>
        </div>
    </div>
    """)


def bar_chart_card(title, caption, items, color, delay=0.0):
    """items: list of (label, pct) tuples"""
    rows = ""
    for i, (label, pct) in enumerate(items):
        rows += _h(f"""
        <div class="bar-row">
            <div class="bar-label-row"><span>{label}</span><span style="color:#7a8598;">{pct:.1f}%</span></div>
            <div class="bar-track"><div class="bar-fill" style="--w:{pct}%;background:{color};animation-delay:{delay + 0.05*i}s;"></div></div>
        </div>
        """)
    return _h(f"""
    <div class="glass-card" style="animation-delay:{delay}s;">
        <span class="g-title">{title}</span>
        <p class="g-caption">{caption}</p>
        {rows}
    </div>
    """)


# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
NAV_PAGES = ["Overview", "Bookings", "Cancellations", "Guests", "Charts", "Reports"]

if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    st.markdown(
        '<div style="font-size:14px;font-weight:600;color:#7fa8ff;padding:4px 4px 16px;">Hotel IQ</div>',
        unsafe_allow_html=True,
    )
    for page_name in NAV_PAGES:
        if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
            st.session_state.page = page_name

page = st.session_state.page
active_idx = NAV_PAGES.index(page) + 1  # nth-of-type is 1-indexed

st.markdown(
    f"""
    <style>
    div[data-testid="stSidebar"] .stButton:nth-of-type({active_idx}) button {{
        background: rgba(77,139,255,0.16) !important;
        color: #eef2f8 !important;
        border-left: 2px solid #4d8bff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="page-header">Hotel booking analytics</div>'
    f'<div class="page-sub">{len(df):,} cleaned bookings, City and Resort hotels, 2017 to 2019 &mdash; {page}</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# OVERVIEW
# ----------------------------------------------------------------------
if page == "Overview":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(
            "Total bookings", f"{kpi['total_bookings']:,}",
            "City", f"{kpi['city_bookings']:,}", "Resort", f"{kpi['resort_bookings']:,}", 0.05
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            "Cancellation rate", f"{kpi['cancel_rate']:.1f}%",
            "City", f"{kpi['city_cancel_rate']:.1f}%", "Resort", f"{kpi['resort_cancel_rate']:.1f}%", 0.1
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            "Avg daily rate", f"${kpi['avg_adr']:.2f}",
            "Median", f"${kpi['median_adr']:.2f}", "Repeat guests", f"{kpi['repeat_guest_pct']:.1f}%", 0.15
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(
            "Avg lead time", f"{kpi['avg_lead_time']:.0f} days",
            "Peak month", kpi["peak_month"], "Quiet month", kpi["quiet_month"], 0.2
        ), unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])
    with col1:
        monthly = utils.monthly_bookings(df)
        max_v, min_v = monthly.max(), monthly.min()
        pts = []
        for i, v in enumerate(monthly.values):
            x = i * (340 / 11)
            y = 90 - ((v - min_v) / (max_v - min_v)) * 90 if max_v > min_v else 45
            pts.append(f"{x:.0f},{y:.0f}")
        polyline = " ".join(pts)
        peak_idx = int(monthly.values.argmax())
        peak_x = peak_idx * (340 / 11)
        st.markdown(_h(f"""
        <div class="glass-card" style="animation-delay:0.25s;">
            <span class="g-title">Bookings by month</span>
            <p class="g-caption">Peaks in {kpi['peak_month']}, quietest in {kpi['quiet_month']}</p>
            <svg viewBox="0 0 340 100" style="width:100%;height:100px;overflow:visible;position:relative;z-index:1;">
                <polyline points="{polyline}" fill="none" stroke="#4d8bff" stroke-width="2"
                    style="stroke-dasharray:700;animation:drawLine 1.6s ease forwards;" />
                <circle cx="{peak_x:.0f}" cy="{90 - 90:.0f}" r="3" fill="#7fa8ff" />
            </svg>
        </div>
        """), unsafe_allow_html=True)
    with col2:
        city_pct = kpi["city_pct"]
        st.markdown(_h(f"""
        <div class="glass-card" style="animation-delay:0.3s;">
            <span class="g-title">Hotel type split</span>
            <div style="display:flex;align-items:center;gap:14px;margin-top:10px;position:relative;z-index:1;">
                <div style="width:70px;height:70px;border-radius:50%;
                    background:conic-gradient(#4d8bff 0 {city_pct:.0f}%, #5dcaa5 {city_pct:.0f}% 100%);
                    flex-shrink:0;box-shadow:0 0 16px rgba(45,100,220,0.15);position:relative;">
                    <div style="position:absolute;inset:13px;background:rgba(0,4,12,0.9);border-radius:50%;"></div>
                </div>
                <div style="font-size:11px;color:#7a8598;display:flex;flex-direction:column;gap:6px;">
                    <span>City hotel, {kpi['city_pct']:.0f}%</span>
                    <span>Resort hotel, {kpi['resort_pct']:.0f}%</span>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        lt = utils.cancel_rate_by_leadtime(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by lead time",
            "Higher the further ahead a guest books",
            list(lt.items()), "#4d8bff", 0.35
        ), unsafe_allow_html=True)
    with col4:
        sl = utils.cancel_rate_by_stay_length(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by stay length",
            "Longer stays cancel more often",
            list(sl.items()), "#5dcaa5", 0.4
        ), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# BOOKINGS
# ----------------------------------------------------------------------
elif page == "Bookings":
    col1, col2 = st.columns([1.4, 1])
    with col1:
        by_hotel = utils.monthly_bookings_by_hotel(df)
        rows_html = ""
        for month in utils.MONTH_ORDER:
            city_v = int(by_hotel.loc[month, "City Hotel"]) if "City Hotel" in by_hotel.columns else 0
            resort_v = int(by_hotel.loc[month, "Resort Hotel"]) if "Resort Hotel" in by_hotel.columns else 0
            rows_html += _h(f"""
            <div style="display:flex;justify-content:space-between;font-size:12px;padding:4px 0;
                        border-bottom:0.5px solid rgba(255,255,255,0.05);position:relative;z-index:1;">
                <span>{month}</span>
                <span style="color:#7a8598;">City {city_v:,} &nbsp;&middot;&nbsp; Resort {resort_v:,}</span>
            </div>
            """)
        st.markdown(_h(f"""
        <div class="glass-card" style="animation-delay:0.05s;">
            <span class="g-title">Bookings per month by hotel type</span>
            <p class="g-caption">Full monthly breakdown across both hotels</p>
            {rows_html}
        </div>
        """), unsafe_allow_html=True)
    with col2:
        seg = utils.market_segment_breakdown(df)
        st.markdown(bar_chart_card(
            "Market segment", "Share of total bookings",
            list(seg.items()), "#8fbaff", 0.1
        ), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        dep = utils.deposit_type_breakdown(df)
        st.markdown(bar_chart_card(
            "Deposit type", "How bookings were secured",
            list(dep.items()), "#4d8bff", 0.2
        ), unsafe_allow_html=True)
    with col4:
        req = utils.special_requests_breakdown(df)
        st.markdown(bar_chart_card(
            "Special requests", "Share of bookings by request count",
            list(req.items()), "#5dcaa5", 0.25
        ), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# CANCELLATIONS
# ----------------------------------------------------------------------
elif page == "Cancellations":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card(
            "Overall cancellation rate", f"{kpi['cancel_rate']:.1f}%",
            "City", f"{kpi['city_cancel_rate']:.1f}%", "Resort", f"{kpi['resort_cancel_rate']:.1f}%", 0.05
        ), unsafe_allow_html=True)
    with c2:
        prev_cancel_pct = (df["previous_cancellations"] > 0).mean() * 100
        st.markdown(kpi_card(
            "Guests with prior cancellations", f"{prev_cancel_pct:.1f}%",
            "Avg count", f"{df['previous_cancellations'].mean():.2f}",
            "Repeat guests", f"{kpi['repeat_guest_pct']:.1f}%", 0.1
        ), unsafe_allow_html=True)
    with c3:
        no_deposit_cancel = df[df["deposit_type"] == "No Deposit"]["is_canceled"].mean() * 100
        st.markdown(kpi_card(
            "No-deposit cancellation rate", f"{no_deposit_cancel:.1f}%",
            "Avg lead time", f"{kpi['avg_lead_time']:.0f} days",
            "Total bookings", f"{kpi['total_bookings']:,}", 0.15
        ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        lt = utils.cancel_rate_by_leadtime(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by lead time",
            "The gap between booking and arrival date",
            list(lt.items()), "#4d8bff", 0.2
        ), unsafe_allow_html=True)
    with col2:
        sl = utils.cancel_rate_by_stay_length(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by stay length",
            "Total nights booked, weekday and weekend combined",
            list(sl.items()), "#5dcaa5", 0.25
        ), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# GUESTS
# ----------------------------------------------------------------------
elif page == "Guests":
    gc = utils.guest_composition(df)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(
            "Avg adults per booking", f"{gc['avg_adults']:.1f}",
            "With children", f"{gc['pct_with_children']:.1f}%",
            "With babies", f"{gc['pct_with_babies']:.1f}%", 0.05
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            "Repeat guests", f"{gc['repeat_guest_pct']:.1f}%",
            "Avg prior cancels", f"{gc['avg_previous_cancellations']:.2f}",
            "Avg special requests", f"{gc['avg_special_requests']:.2f}", 0.1
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            "Avg daily rate", f"${kpi['avg_adr']:.2f}",
            "Median", f"${kpi['median_adr']:.2f}",
            "Total bookings", f"{kpi['total_bookings']:,}", 0.15
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(
            "Avg lead time", f"{kpi['avg_lead_time']:.0f} days",
            "Peak month", kpi["peak_month"], "Quiet month", kpi["quiet_month"], 0.2
        ), unsafe_allow_html=True)

    req = utils.special_requests_breakdown(df)
    st.markdown(bar_chart_card(
        "Special requests distribution", "Share of bookings by number of special requests made",
        list(req.items()), "#8fbaff", 0.25
    ), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# REPORTS
# ----------------------------------------------------------------------
elif page == "Reports":
    st.markdown(_h(f"""
    <div class="glass-card" style="animation-delay:0.05s;">
        <span class="g-title">Summary</span>
        <p style="font-size:13px;color:#eef2f8;line-height:1.6;position:relative;z-index:1;margin-top:8px;">
            City Hotel accounts for {kpi['city_pct']:.0f}% of all bookings but cancels at a higher rate
            ({kpi['city_cancel_rate']:.1f}%) than Resort Hotel ({kpi['resort_cancel_rate']:.1f}%).
            Cancellations rise steadily with lead time and with stay length, meaning bookings made far
            in advance, or for longer stays, are the least reliable segment of the business.
        </p>
    </div>
    """), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_h(f"""
        <div class="glass-card" style="animation-delay:0.1s;">
            <span class="g-title">Hotel type and seasonality</span>
            <ul style="font-size:12px;color:#eef2f8;line-height:1.7;position:relative;z-index:1;padding-left:18px;margin-top:8px;">
                <li>Promote Resort Hotel more heavily in off-peak months to close the demand gap with City Hotel.</li>
                <li>Increase rates or reduce discounting around {kpi['peak_month']}, the busiest month, since demand is already strong.</li>
            </ul>
        </div>
        """), unsafe_allow_html=True)
    with col2:
        st.markdown(_h(f"""
        <div class="glass-card" style="animation-delay:0.15s;">
            <span class="g-title">Stay duration and cancellations</span>
            <ul style="font-size:12px;color:#eef2f8;line-height:1.7;position:relative;z-index:1;padding-left:18px;margin-top:8px;">
                <li>Introduce stricter cancellation terms or a partial deposit for stays of 6+ nights.</li>
                <li>Offer a small non-refundable discount incentive to encourage rate lock-in on long stays.</li>
            </ul>
        </div>
        """), unsafe_allow_html=True)

    st.markdown(_h(f"""
    <div class="glass-card" style="animation-delay:0.2s;">
        <span class="g-title">Lead time and cancellations</span>
        <ul style="font-size:12px;color:#eef2f8;line-height:1.7;position:relative;z-index:1;padding-left:18px;margin-top:8px;">
            <li>Send a confirmation reminder and a soft deposit request for bookings made 100+ days in advance, the highest-risk group.</li>
            <li>Offer a rescheduling option instead of a full cancellation for early, far-out bookings, to retain revenue.</li>
        </ul>
        <p style="font-size:12px;color:#7a8598;line-height:1.6;position:relative;z-index:1;margin-top:10px;">
            Highest-impact recommendation: targeting long-lead-time bookings (100+ days) with a deposit or reminder
            policy, since this segment has the highest cancellation rate and the largest volume of at-risk revenue.
        </p>
    </div>
    """), unsafe_allow_html=True)

# ----------------------------------------------------------------------
# CHARTS
# ----------------------------------------------------------------------
elif page == "Charts":
    col1, col2 = st.columns(2)
    with col1:
        meal = utils.meal_breakdown(df)
        st.markdown(bar_chart_card(
            "Meal plan breakdown",
            "Share of bookings by meal plan chosen",
            list(meal.items()), "#4d8bff", 0.05
        ), unsafe_allow_html=True)
    with col2:
        ctype = utils.customer_type_breakdown(df)
        st.markdown(bar_chart_card(
            "Customer type",
            "Share of bookings by customer type",
            list(ctype.items()), "#5dcaa5", 0.1
        ), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        seg_cancel = utils.cancel_rate_by_market_segment(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by market segment",
            "Non-Refund deposits cancel far more than any other segment",
            list(seg_cancel.items()), "#8fbaff", 0.15
        ), unsafe_allow_html=True)
    with col4:
        dep_cancel = utils.cancel_rate_by_deposit_type(df)
        st.markdown(bar_chart_card(
            "Cancellation rate by deposit type",
            "Non-Refund bookings cancel at 94.8%, far above No Deposit",
            list(dep_cancel.items()), "#4d8bff", 0.2
        ), unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        cities = utils.top_cities(df)
        st.markdown(bar_chart_card(
            "Top guest cities",
            "Share of bookings by guest's home city, top 5",
            list(cities.items()), "#5dcaa5", 0.25
        ), unsafe_allow_html=True)
    with col6:
        wk = utils.weekend_vs_weekday_nights(df)
        st.markdown(bar_chart_card(
            "Weekend vs weekday nights",
            "Share of bookings by which nights were stayed",
            list(wk.items()), "#8fbaff", 0.3
        ), unsafe_allow_html=True)

glass_hover_script()
