# Digital Platform for Direct Market Access for Farmers

## About the Project

The **Digital Platform for Direct Market Access for Farmers** is a web-based application designed to connect farmers directly with buyers. It aims to simplify agricultural product discovery and support direct interaction between farmers and buyers, reducing reliance on intermediaries.

The platform provides a marketplace where users can explore agricultural products, manage their shopping cart, place orders, and negotiate prices.

## Objectives

- Enable direct interaction between farmers and buyers.
- Provide a digital marketplace for agricultural products.
- Support product browsing and order management.
- Facilitate price negotiation between farmers and buyers.
- Maintain user and product data using a database.

## Features

- **User Registration:** Separate registration for farmers and buyers.
- **Product Marketplace:** Browse available agricultural products and their prices.
- **Shopping Cart:** Add and manage selected products.
- **Order Management:** Support the ordering process.
- **Price Negotiation:** Facilitate negotiation between buyers and farmers.
- **Database Integration:** Store and retrieve application data using Oracle Database.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** Oracle Database
- **Database Connectivity:** Python `oracledb` driver
- **Development Environment:** Visual Studio Code / local development environment
- **Version Control:** Git and GitHub

## Database

The project uses Oracle Database to manage application data. The database schema includes tables for:

- Farmers
- Buyers
- Categories
- Products
- Orders
- Order items
- Negotiations
- Negotiation offers
- Deliveries
- Reviews

## Getting Started

### Prerequisites

Install or configure the following:

- Python 3
- Oracle Database with the project schema
- Git (optional for cloning the repository)

### Installation

1. Clone the repository:

   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   ```

2. Navigate to the project directory:

   ```bash
   cd FarmerDigitalPlatform
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. Install the required Python packages:

   ```bash
   pip install flask oracledb
   ```

5. Configure your Oracle database connection using your local database credentials. Do not commit passwords or other sensitive credentials to GitHub.

6. Start the Flask application using your project's entry-point file:

   ```bash
   python app.py
   ```

7. Open the local application in your browser at:

   ```text
   http://127.0.0.1:5000/
   ```

## Project Structure

```text
FarmerDigitalPlatform/
├── app.py
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

*The structure above is illustrative. Additional files and folders may be present in the actual project.*

## Future Improvements

- Secure authentication and password hashing.
- Dedicated farmer and buyer dashboards.
- Improved product and inventory management.
- Enhanced order tracking and delivery management.
- Deployment to a publicly accessible hosting environment.

## Project Status

**Status:** Under Development

This project is being developed as an academic software project to explore web application development, database integration, and digital solutions for agricultural market access.

## Contributors

S. Raajvee 
Mohitha Shruthi.B
Afsinaa Fathima.A
S.Naga Sri Lasya
Samiksha
---

*Digital Platform for Direct Market Access for Farmers — connecting farmers and buyers through technology.*
