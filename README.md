# Public Health Data Insights Dashboard

A Python-based data insights tool for researchers analysing public health data (vaccination rates, disease outbreaks, mental health reports). Built with Test-Driven Development (TDD) methodology.

## Features

- **Data Access**: Load data from CSV/JSON and store in SQLite database
- **Data Cleaning**: Handle missing values, type conversions, data validation
- **Filtering**: Filter by country, date range, age group, and custom criteria
- **Summaries**: Calculate mean, min, max, counts, and trends over time
- **Visualizations**: Generate charts (matplotlib) and formatted tables (pandas)
- **CRUD Operations**: Create, read, update, delete records in database
- **Export**: Export filtered data and summaries to CSV
- **Logging**: Track all user activities

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pai_task1
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python main.py
```

Run tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Project Structure

```
pai_task1/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── main.py                      # Application entry point
├── src/                         # Source code modules
│   ├── data_loader.py           # Data access and loading
│   ├── database.py              # SQLite operations
│   ├── data_cleaner.py          # Data cleaning functions
│   ├── filters.py               # Filtering operations
│   ├── summaries.py             # Statistical summaries
│   ├── visualizations.py        # Chart generation
│   ├── exporter.py              # CSV export
│   └── logger.py                # Activity logging
├── tests/                       # Test files (TDD)
├── data/                        # Sample datasets
├── logs/                        # Activity logs
└── exports/                     # Exported CSV files
```

## Git Repository

**Repository Link**: [Add your repository link here]

## Development Approach

This project follows **Test-Driven Development (TDD)**:
1. Write failing tests first
2. Implement minimal code to pass tests
3. Refactor while keeping tests green

## Author

[Ogieltaziba Douglas]

## License

This project is for academic purposes.
