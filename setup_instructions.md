# Multi-Location Construction Project Management System
## Complete Application Setup Guide

### Overview
This is a comprehensive construction project management system built with Streamlit, designed to manage materials, deliveries, and finances across multiple construction sites.

### Features
- **Multi-Location Support**: Manage 4 project sites (Vahmaafushi, Keyodhoo, Male', Hulhumale')
- **Complete CRUD Operations**: Add, edit, delete across all modules
- **User Authentication**: Admin and team member roles
- **Materials Management**: Track materials, categories, suppliers
- **Delivery Tracking**: Record and monitor deliveries with quantity sync
- **Cash Management**: Track expenses and transactions
- **Accounting System**: Financial reporting and analysis
- **Usage Tracking**: Monitor material consumption
- **Reports & Analytics**: Comprehensive reporting system

### Files Included
1. `complete_construction_app.py` - Main application file
2. `setup_instructions.md` - This setup guide
3. `.streamlit/config.toml` - Streamlit configuration

### Installation Steps

#### 1. Install Dependencies
```bash
pip install streamlit pandas
```

#### 2. Create Project Directory
```bash
mkdir construction_management
cd construction_management
```

#### 3. Copy Application Files
- Copy `complete_construction_app.py` to your project directory
- Rename it to `app.py` or keep the original name

#### 4. Create Streamlit Configuration
Create a `.streamlit` folder and add `config.toml`:
```bash
mkdir .streamlit
```

Create `.streamlit/config.toml` with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

#### 5. Run the Application
```bash
streamlit run complete_construction_app.py
```
Or if renamed:
```bash
streamlit run app.py
```

### Default Login Credentials
- **Admin**: Username: `admin`, Password: `admin123`
- **Team Member**: Username: `team`, Password: `team123`

### System Structure

#### Main Modules
1. **Dashboard** - Overview and quick stats
2. **Materials Management** - Complete material lifecycle
3. **Delivery Management** - Delivery tracking and notes
4. **Cash Management** - Financial transactions
5. **Accounting System** - Financial reporting (Admin only)
6. **Usage Tracking** - Material consumption monitoring
7. **Reports & Analytics** - Comprehensive reporting

#### Data Storage
- All data is stored in Streamlit session state
- No external database required
- Data persists during session

### Customization Options

#### Adding New Locations
Edit the `initialize_data()` function to add new project locations:
```python
st.session_state.locations = [
    {'name': 'Your Location', 'icon': '🏗️', 'description': 'Description'},
    # Add more locations here
]
```

#### Adding New Categories/Suppliers
Use the "Manage Fields" tab in Materials Management to add:
- Material categories
- Suppliers
- Project areas

#### User Management
Modify the `authenticate()` function to add new users or change passwords.

### Deployment Options

#### Local Development
- Run with `streamlit run app.py`
- Access at `http://localhost:5000`

#### Cloud Deployment
1. **Streamlit Cloud**: Upload to GitHub and deploy
2. **Heroku**: Add `Procfile` and deploy
3. **Replit**: Import project and run

### Technical Details

#### Key Functions
- `initialize_data()` - Sets up default data and configurations
- `authenticate()` - Handles user login
- `materials_management()` - Complete materials CRUD
- `delivery_management()` - Delivery tracking system
- `cash_management()` - Financial transaction management

#### Data Relationships
- Materials link to deliveries via material_id
- Deliveries update material quantities automatically
- Cash transactions can be linked to materials/deliveries
- Usage records track material consumption

### Troubleshooting

#### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Port Issues**: Change port in config.toml if needed
3. **Data Loss**: Data resets when app restarts (session-based)

#### Performance Tips
- Data is stored in memory, suitable for small to medium datasets
- For production use, consider adding database integration
- Use filters to manage large datasets

### Support and Maintenance

#### Regular Maintenance
- Clear browser cache if experiencing issues
- Update dependencies periodically
- Backup important data before major changes

#### Extending the System
- Add new modules by creating functions and adding to navigation
- Extend data models by modifying session state initialization
- Add new reports by extending the analytics functions

This system provides a complete foundation for construction project management across multiple locations with full CRUD capabilities and comprehensive reporting.

