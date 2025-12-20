# 📚 Book Haven

A comprehensive library management system with data analytics, business intelligence capabilities, and a desktop GUI application. This project includes database design, data generation, ETL processes, interactive Power BI dashboards, and a role-based GUI for library operations.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Data Pipeline](#data-pipeline)
- [GUI Application](#gui-application)
- [Power BI Analytics](#power-bi-analytics)

## 🎯 Overview

Book Haven is a complete library management and analytics solution that demonstrates end-to-end data engineering and business intelligence workflows. The project encompasses:

- Library database design with normalized schema
- Automated data generation for realistic library operations
- ETL processes for data integration
- Desktop GUI application with role-based access control
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
├── GUI/
│   ├── library_app.py                # Desktop GUI application
│   ├── requirements.txt              # Python dependencies for GUI
│   └── venv/                         # Virtual environment
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

### Desktop GUI Application
- **User Authentication**: Secure login system for library staff
- **Role-Based Access Control**: Four user roles with specific permissions:
  - **Manager**: Full access to all tables and operations
  - **Librarian**: Manage books, authors, categories, and members
  - **Assistant**: Handle member registration and reservations
  - **Technician**: Manage book copy maintenance and status
- **CRUD Operations**: Create, Read, Update, Delete functionality for all entities
- **Search Functionality**: Dynamic search across multiple fields
- **Intuitive Interface**: User-friendly design with Tkinter

### Analytics & Visualization
- **Power BI Dashboard**: Interactive visualizations for library insights
- **Operational Metrics**: Track reservations, inventory, and member activity
- **Business Intelligence**: Data-driven decision support

## 🛠 Technologies Used

- **Database**: SQL Server (with ODBC Driver 17)
- **Backend**: Python 3.8+
- **GUI Framework**: Tkinter
- **Database Connectivity**: pyodbc
- **Data Processing**: Pandas, NumPy
- **Analysis Tools**: Jupyter Notebook
- **Visualization**: Power BI Desktop
- **Data Sources**: Kaggle Datasets
- **Version Control**: Git & GitHub

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- SQL Server or SQL Server Express
- ODBC Driver 17 for SQL Server
- Jupyter Notebook
- Power BI Desktop
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kindahard/Book_haven.git
cd Book_haven
```

2. **Set up the database**
```bash
# Run the DDL script to create the database schema
# Execute Database scripts/Book_haven_ddl.sql in SQL Server Management Studio or your SQL client
```

3. **Configure database connection**
```bash
# Update database credentials in GUI/library_app.py:
# - server: Your SQL Server instance (default: .\SQLEXPRESS)
# - database: book_haven
# - username: Your database username
# - password: Your database password
```

4. **Install Python dependencies for data generation**
```bash
pip install pandas numpy jupyter sqlalchemy python-dotenv
```

5. **Set up environment variables (optional)**
```bash
# Create .env file in the app/ directory
DB_HOST=localhost
DB_NAME=book_haven
DB_USER=your_username
DB_PASSWORD=your_password
```

6. **Generate and load data**
```bash
# Open Jupyter Notebook
jupyter notebook

# Run notebooks in order:
# 1. Notebooks/generate_library_data.ipynb
# 2. Notebooks/insert_data.ipynb
```

7. **Set up GUI application**
```bash
cd GUI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install GUI dependencies
pip install -r requirements.txt
```

8. **Run the GUI application**
```bash
python library_app.py
```

## 🗄 Database Schema

The library management system uses a normalized relational database with the following key entities:

- **Book**: Core book information and catalog
- **Author**: Author details and bibliographic data
- **Category**: Book classification and genres
- **Book_Copy**: Physical inventory tracking
- **Member**: Library member records
- **Staff**: Employee information with authentication
- **Reservation**: Borrowing and reservation system
- **Reservation_Details**: Line items for each reservation
- **Description**: Extended book metadata
- **Book_Author**: Many-to-many relationship between books and authors
- **Book_Category**: Many-to-many relationship between books and categories

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

## 🖥 GUI Application

### Features

#### Authentication & Security
- Secure login system with email and password
- Session management for logged-in users
- Role-based access control enforced at the UI level

#### User Roles & Permissions

**Manager**
- Access: All tables and operations
- Can add, edit, and delete all records
- Full system administration capabilities

**Librarian**
- Access: Authors, Books, Book Copies, Categories, Descriptions, Members, Book-Author relationships, Book-Category relationships
- Can add, edit books, authors, and categories
- Can delete book copies and relationship records
- Cannot modify staff or reservations

**Assistant**
- Access: Members, Reservations, Reservation Details
- Can add members and create reservations
- Can edit reservation details
- Limited to customer-facing operations

**Technician**
- Access: Book Copies only
- Can edit book copy status and maintenance records
- Cannot add or delete records
- Focused on physical inventory management

#### Core Functionality

**Table Management**
- View all accessible tables based on role
- Dynamic column display with horizontal/vertical scrolling
- Real-time data refresh

**Search & Filter**
- Dynamic search across multiple fields
- Intelligent field selection (IDs, names, emails, ISBNs)
- Clear search results with one click

**CRUD Operations**
- **Create**: Add new records with form validation
- **Read**: View all records in sortable tables
- **Update**: Edit existing records with pre-filled forms
- **Delete**: Remove records with confirmation dialogs

**User Interface**
- Clean, modern design with color-coded actions
- Scrollable forms for tables with many columns
- Responsive layout that adapts to content
- Identity columns automatically disabled in edit mode
- Professional color scheme (green for add, orange for edit, red for delete, blue for refresh)

### Running the GUI

```bash
cd GUI
python library_app.py
```

**Default Test Credentials:**
You can create test staff accounts in the database with different roles to explore various permission levels.

### GUI Technical Details

**Database Connection**
- Uses pyodbc for SQL Server connectivity
- Connection pooling for performance
- Automatic error handling and user feedback

**Security Features**
- Password fields masked with asterisks
- SQL injection prevention through parameterized queries
- Session-based authentication

**Data Handling**
- Automatic detection of identity columns (auto-increment)
- Support for text fields with multi-line input
- Proper handling of NULL values
- String trimming to prevent whitespace issues

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

## 🔧 Troubleshooting

### GUI Issues

**Cannot connect to database:**
- Verify SQL Server is running
- Check connection credentials in `library_app.py`
- Ensure ODBC Driver 17 is installed
- Confirm database name is correct

**Login fails:**
- Verify staff records exist in the database
- Check email and password are correct
- Ensure staff table has been populated

**Permission errors:**
- Verify your user role in the staff table
- Check that role name matches exactly (case-sensitive)
- Ensure permissions are properly configured

### Data Pipeline Issues

**Import errors in notebooks:**
```bash
pip install pandas numpy jupyter sqlalchemy python-dotenv
```

**Database connection fails:**
- Update connection string in notebooks
- Verify .env file configuration
- Check SQL Server authentication mode

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on [GitHub](https://github.com/kindahard/Book_haven/issues)
- Repository: [https://github.com/kindahard/Book_haven](https://github.com/kindahard/Book_haven)

## 🙏 Acknowledgments

- Kaggle for providing the book datasets
- The open-source community for the tools and libraries used
- Python Tkinter community for GUI development resources

## 📝 Future Enhancements

- Web-based interface using Flask/Django
- Mobile application for members
- Barcode scanning for book copies
- Email notifications for due dates
- Advanced reporting features
- API for third-party integrations

---

**Note**: Before running the project, ensure you review the `ERD.png` and `mapping.png` files to understand the database structure and data relationships. For the GUI application, make sure to configure the database connection parameters in `library_app.py` before running.