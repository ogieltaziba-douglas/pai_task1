# Public Health Data Insights Dashboard

A Python-based data insights tool for researchers analysing COVID-19 vaccination data. Built with Test-Driven Development (TDD) and Object-Oriented Programming (OOP).

## Features

- **Data Loading**: Load CSV data into SQLite database
- **Data Cleaning**: Handle missing values with forward fill (`DataCleaner` class)
- **SQL Filtering**: Filter by country, continent, income group, date range (`DataFilter` class)
- **Summaries**: Calculate statistics, trends, and aggregations
- **Visualizations**: Generate charts (matplotlib) and formatted tables
- **Export**: Export filtered data to CSV
- **Logging**: Track user activities (`ActivityLogger` class)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ogieltaziba-douglas/pai_task1.git
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

## Project Structure

```
pai_task1/
├── main.py                      # Application entry point
├── src/
│   ├── dashboard.py             # Dashboard + DashboardState classes
│   ├── data_loader.py           # CSV loading (load_csv, get_data_info)
│   ├── data_cleaner.py          # DataCleaner class (OOP)
│   ├── filters.py               # DataFilter class (SQL-based, OOP)
│   ├── database.py              # SQLite operations
│   ├── summaries.py             # Statistical functions
│   ├── visualizations.py        # Chart generation
│   ├── menu_handlers.py         # CLI menu handlers
│   ├── logger.py                # ActivityLogger class (OOP)
│   ├── constants.py             # Configuration constants
│   ├── cli.py                   # CLI utilities
│   └── exporter.py              # CSV export
├── tests/                       # 193 tests (pytest)
├── data/                        # Dataset (vaccinations.csv)
├── logs/                        # Activity logs
└── exports/                     # Exported files
```

## OOP Classes

| Class | Module | Purpose |
|-------|--------|---------|
| `Dashboard` | `dashboard.py` | Main application state with encapsulation |
| `DashboardState` | `dashboard.py` | Legacy state holder (backwards compatible) |
| `DataFilter` | `filters.py` | SQL query builder with method chaining |
| `DataCleaner` | `data_cleaner.py` | Data cleaning with method chaining |
| `ActivityLogger` | `logger.py` | Session and file logging |

## Development Approach

- **TDD**: Tests written first, 193 tests passing
- **OOP**: Encapsulation, properties, method chaining
- **SQL**: All filtering uses SQLite queries 

## Git Repository

**Repository**: https://github.com/ogieltaziba-douglas/pai_task1.git

## Author

Ogieltaziba Douglas

## License

This project is for academic purposes.
