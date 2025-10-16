
# Real-Estate-Sentiment-Analysis: Constructing China's Real Estate Public Sentiment Index

### Project Overview

This project investigates the impact of government real estate policies on Chinese public sentiment and the overall market prosperity. By combining web scraping, Natural Language Processing (NLP) techniques, and time-series econometrics, a quantifiable **Public Sentiment Index (PI)** is constructed and used in an Event Study Model to assess the effect of the Q1 2024 policy changes.

- **Primary Metric:** Public Sentiment Index (PI), defined as the Positive Sentiment Ratio.
- **Data Period:** January 2022 to June 2024.
- **Methodology:** Dynamic Panel Model (for benchmark fitting) and Event Study Model (for policy evaluation).

---

### Technical Implementation & Data

#### 1. Data Collection and Processing

- **Sources:** Bilibili pop-ups (45,701 entries) and Xiaohongshu comments (25,049 entries).
- **Keywords:** Focused on highly relevant terms like "real estate," "buying a house," and "down payment".
- **Technology:** Python web scraping using `requests` and `BeautifulSoup` for XML/HTML parsing.

#### 2. Chinese Sentiment Analysis (NLP)

- **Tool:** The `SnowNLP` library was used for Chinese text sentiment scoring.
- **Index Definition (PI):** The PI is the **positive sentiment ratio** derived from all comments and pop-ups.
- **Classification Logic:** A sentiment score less than 0.5 is classified as Negative, greater than 0.5 as Positive, and equal to 0.5 as Neutral.

#### 3. Econometric Data Sources

- **National Housing Prosperity Index (NHPI):** Collected monthly from the CSMAR database.
- **Year-on-year Sales Growth (S):** Collected from the National Bureau of Statistics (NBS).

---

### Key Findings and Research Contribution

The constructed PI time series serves as the dependent variable for the econometric analysis.

1.  **Policy Impact vs. Market Reality (Core Finding):**
    * **Short-Term Policy Effect:** The introduction of favorable policies in Q1 2024 resulted in a **Cumulative Abnormal Return (CAR) significantly greater than zero** ($CAR = 0.2509$). This demonstrates a clear **positive market reaction** and a **short-term boost** to public sentiment.
    * **Long-Term Market Dominance:** The analysis shows that sentiment eventually **reverts to the normal return pattern over time**. This suggests that **long-term public sentiment** is ultimately determined by the **actual performance of the domestic real estate market** (e.g., the NHPI) rather than sustained policy optimism.
2.  **Index Validation:** The current period PI shows a relatively strong time-series correlation of **74.47%** with the year-on-year growth in sales of commercial residential housing in the **previous period** ($S_{t-1}$), validating the index's utility as a leading indicator.
3.  **Lagged Effects and Inertia:** The empirical model confirmed that while prior period sentiment ($PI_{t-1}$) indicates **optimistic inertia**, the **pre-previous** national prosperity index ($NHPI_{t-2}$) has a **negative** effect, highlighting a longer **memory effect for past negative market performance**.

---

### Repository Structure & Execution

| File | Description |
| :--- | :--- |
| `sentiment_processor.py` | The core Python script containing the functions for data collection (simulated), sentiment analysis (SnowNLP), and calculation of the final monthly PI series. |
| `Real-estate-pop-ups.csv` | Simulated raw data output file from the crawler. |
| `market_metrics.csv` | Input file containing the National Housing Prosperity Index (NHPI) and Sales Growth (S) time series. |

#### Instructions to Run:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[Your_Username]/Real-Estate-Sentiment-Analysis.git
    cd Real-Estate-Sentiment-Analysis
    ```

2.  **Install Dependencies:**
    ```bash
    pip install pandas requests beautifulsoup4 snownlp jieba
    ```

3.  **Execute the Script:**
    ```bash
    python sentiment_processor.py
    ```
    *(The script will output the calculated monthly PI series ready for econometric analysis.)*
