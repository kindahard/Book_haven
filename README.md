# 📚 Book Haven

A comprehensive library management system with data analytics and business intelligence capabilities. This project includes database design, data generation, ETL processes, and interactive Power BI dashboards for library operations analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Data Pipeline](#data-pipeline)
- [Power BI Analytics](#power-bi-analytics)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Book Haven is a complete library management and analytics solution that demonstrates end-to-end data engineering and business intelligence workflows. The project encompasses:

- Library database design with normalized schema
- Automated data generation for realistic library operations
- ETL processes for data integration
- Interactive Power BI dashboards for operational insights

## 📁 Project Structure

```
Book_haven/
├── app/
│   └── .env                          # Environment configuration
├── Data/
│   ├── Database/
│   │   └── book_haven                # Database files
│   └── Kaggle datasets/
│       ├── books1.csv                # External book dataset 1
│       ├── books2.csv                # External book dataset 2
│       └── users.csv                 # User/member data
├── Database scripts/
│   └── Book_haven_ddl.sql            # Database schema definition
├── Notebooks/
│   ├── generate_library_data.ipynb   # Data generation notebook
│   ├── insert_data.ipynb             # Data insertion pipeline
│   └── data/
│       ├── author.csv                # Generated author data
│       ├── book.csv                  # Book catalog data
│       ├── book_author.csv           # Book-author relationships
│       ├── book_category.csv         # Book categorization
│       ├── book_copy.csv             # Physical book copies
│       ├── category.csv              # Category master data
│       ├── description.csv           # Book descriptions
│       ├── member.csv                # Library members
│       ├── reservation.csv           # Reservation records
│       ├── reservation_details.csv   # Reservation line items
│       └── staff.csv                 # Staff information
├── power bi/
│   └── book_haven.pbix               # Power BI dashboard
├── ERD.png                            # Entity Relationship Diagram
└── mapping.png                        # Data mapping documentation
```

## ✨ Features

### Database Management
- **Normalized Schema**: Fully normalized database design for library operations
- **DDL Scripts**: Complete database definition with tables, relationships, and constraints
- **Entity Relationships**: Comprehensive ERD documentation

### Data Generation & ETL
- **Synthetic Data Generation**: Automated creation of realistic library data
- **External Data Integration**: Integration of Kaggle book datasets
- **Data Insertion Pipeline**: Automated ETL process for populating the database

### Analytics & Visualization
- **Power BI Dashboard**: Interactive visualizations for library insights
- **Operational Metrics**: Track reservations, inventory, and member activity
- **Business Intelligence**: Data-driven decision support

## 🛠 Technologies Used

- **Database**: SQL (DDL/DML)
- **Data Processing**: Python, Pandas
- **Analysis Tools**: Jupyter Notebook
- **Visualization**: Power BI Desktop
- **Data Sources**: Kaggle Datasets
- **Version Control**: Git & GitHub

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook
- SQL Server or compatible database engine
- Power BI Desktop
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kindahard/Book_haven.git
cd Book_haven
```

2. **Install Python dependencies**
```bash
pip install pandas numpy jupyter sqlalchemy python-dotenv
```

3. **Set up environment variables**
```bash
# Create .env file in the app/ directory
# Add your database connection string
DB_HOST=localhost
DB_NAME=book_haven
DB_USER=your_username
DB_PASSWORD=your_password
```

4. **Create the database**
```bash
# Run the DDL script to create the database schema
# Execute Database scripts/Book_haven_ddl.sql in your SQL client
```

5. **Generate and load data**
```bash
# Open Jupyter Notebook
jupyter notebook

# Run notebooks in order:
# 1. Notebooks/generate_library_data.ipynb
# 2. Notebooks/insert_data.ipynb
```

## 🗄 Database Schema

The library management system uses a normalized relational database with the following key entities:

- **Book**: Core book information and catalog
- **Author**: Author details and bibliographic data
- **Category**: Book classification and genres
- **Book_Copy**: Physical inventory tracking
- **Member**: Library member records
- **Staff**: Employee information
- **Reservation**: Borrowing and reservation system
- **Description**: Extended book metadata

Refer to `ERD.png` for the complete entity relationship diagram showing all tables, columns, and relationships.

## 📊 Data Pipeline

### 1. Data Generation
The `generate_library_data.ipynb` notebook creates realistic library data including:
- Random but consistent member profiles
- Staff records with roles and departments
- Book copies with availability status
- Reservation history with realistic patterns

### 2. Data Integration
External datasets from Kaggle are integrated to enrich the book catalog with:
- Comprehensive book metadata
- Author information
- Genre classifications
- Book descriptions

### 3. Data Loading
The `insert_data.ipynb` notebook handles:
- Data validation and cleaning
- Relationship integrity checks
- Bulk insertion into the database
- Error handling and logging

## 📈 Power BI Analytics

The `book_haven.pbix` dashboard provides insights into:

- **Library Operations**
  - Active reservations and returns
  - Book availability and circulation
  - Peak usage times and patterns

- **Collection Management**
  - Popular books and categories
  - Inventory status and gaps
  - Author and genre distribution

- **Member Analytics**
  - Membership trends and demographics
  - Borrowing patterns and preferences
  - Member engagement metrics

### Opening the Dashboard
```bash
# Open Power BI Desktop
# File > Open > Navigate to power bi/book_haven.pbix
# Update data source connections if needed
```

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on [GitHub](https://github.com/kindahard/Book_haven/issues)
- Repository: [https://github.com/kindahard/Book_haven](https://github.com/kindahard/Book_haven)

## 🙏 Acknowledgments

- Kaggle for providing the book datasets
- The open-source community for the tools and libraries used

---

**Note**: Before running the project, ensure you review the `ERD.png` and `mapping.png` files to understand the database structure and data relationships.
