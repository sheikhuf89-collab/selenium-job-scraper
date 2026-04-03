# 🕷️ Selenium Job Scraper

A Python-based web scraper built with Selenium that extracts job listings from [Welcome to the Jungle](https://www.welcometothejungle.com) — specifically targeting **US-based Business category jobs**.

---

## 📌 Features

- Scrapes job listings from Welcome to the Jungle automatically
- Filters by **country (US)** and **category (Business)**
- Extracts **10 fields per job listing**
- Saves results to a structured **CSV file**
- Handles dynamic page content using Selenium WebDriver

---

## 📦 Tech Stack

- Python 3.x
- Selenium
- ChromeDriver
- CSV (built-in)

---

## 🗂️ Extracted Fields

Each job listing captures the following data:

| Field | Description |
|---|---|
| Job Title | Title of the job position |
| Company Name | Name of the hiring company |
| Location | Job location |
| Contract Type | Full-time, part-time, contract, etc. |
| Experience Level | Required experience |
| Salary | Salary range (if available) |
| Remote Policy | On-site, hybrid, or remote |
| Date Posted | When the job was posted |
| Job URL | Direct link to the listing |
| Description | Short job description/summary |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/selenium-job-scraper.git
cd selenium-job-scraper
```

### 2. Install dependencies

```bash
pip install selenium
```

### 3. Download ChromeDriver

Download the ChromeDriver version matching your Chrome browser from:
[https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

Place it in your project directory or add it to your system PATH.

### 4. Run the scraper

```bash
python scraper.py
```

---

## 📁 Output

Results are saved as `jobs.csv` in the project root directory.

---

## 📸 Sample Output

```
Job Title        | Company       | Location     | Contract Type
-----------------|---------------|--------------|---------------
Business Analyst | Acme Corp     | New York, US | Full-time
Operations Lead  | TechStart Inc | Austin, US   | Full-time
```

---

## 🚧 Known Limitations

- The site uses a non-standard search bar that requires special Selenium interaction handling
- Scraping speed depends on page load time and network conditions
- Results may vary if the website structure changes

---

## 👨‍💻 Author

**Sheikh Umar Faruk**  
B.Tech Computer Science | Data Analyst  
[GitHub](https://github.com/# 🕷️ Selenium Job Scraper

A Python-based web scraper built with Selenium that extracts job listings from [Welcome to the Jungle](https://www.welcometothejungle.com) — specifically targeting **US-based Business category jobs**.

---

## 📌 Features

- Scrapes job listings from Welcome to the Jungle automatically
- Filters by **country (US)** and **category (Business)**
- Extracts **10 fields per job listing**
- Saves results to a structured **CSV file**
- Handles dynamic page content using Selenium WebDriver

---

## 📦 Tech Stack

- Python 3.x
- Selenium
- ChromeDriver
- CSV (built-in)

---

## 🗂️ Extracted Fields

Each job listing captures the following data:

| Field | Description |
|---|---|
| Job Title | Title of the job position |
| Company Name | Name of the hiring company |
| Location | Job location |
| Contract Type | Full-time, part-time, contract, etc. |
| Experience Level | Required experience |
| Salary | Salary range (if available) |
| Remote Policy | On-site, hybrid, or remote |
| Date Posted | When the job was posted |
| Job URL | Direct link to the listing |
| Description | Short job description/summary |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/selenium-job-scraper.git
cd selenium-job-scraper
```

### 2. Install dependencies

```bash
pip install selenium
```

### 3. Download ChromeDriver

Download the ChromeDriver version matching your Chrome browser from:
[https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

Place it in your project directory or add it to your system PATH.

### 4. Run the scraper

```bash
python scraper.py
```

---

## 📁 Output

Results are saved as `jobs.csv` in the project root directory.

---

## 📸 Sample Output

```
Job Title        | Company       | Location     | Contract Type
-----------------|---------------|--------------|---------------
Business Analyst | Acme Corp     | New York, US | Full-time
Operations Lead  | TechStart Inc | Austin, US   | Full-time
```

---

## 🚧 Known Limitations

- The site uses a non-standard search bar that requires special Selenium interaction handling
- Scraping speed depends on page load time and network conditions
- Results may vary if the website structure changes

---

## 👨‍💻 Author

**Sheikh Umar Faruk**  
B.Tech Computer Science | Data Analyst  
[GitHub](https://github.com/sheikhuf89-collab) • [LinkedIn](https://linkedin.com/in/sheikh-umar-faruk)

---

## 📄 License

This project was built as part of a technical assessment for a Data Extraction Engineer role.  
Feel free to use or modify for learning purposes.) • [LinkedIn](https://linkedin.com/in/sheikh-umar-faruk)

---

## 📄 License

This project was built as part of a technical assessment for a Data Extraction Engineer role.  
Feel free to use or modify for learning purposes.
