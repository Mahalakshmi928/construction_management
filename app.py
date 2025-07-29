# ✅ Imports
import streamlit as st
import pandas as pd
import json
from datetime import datetime, date, timedelta
import os
import base64

# ✅ Database imports
from db_handler import (
    init_db, create_extra_tables, create_tables,
    insert_material, fetch_materials, get_all_materials,
    update_delivery, insert_delivery, get_all_deliveries,
    get_all_cash, get_all_receivables, get_all_payables
)

# ✅ Initialize database tables
init_db()
create_extra_tables()


# ✅ Ensure all session variables are initialized in a single, clear block
if "suppliers" not in st.session_state:
    st.session_state.suppliers = [
        {'id': 'kitchen_solutions', 'name': 'Kitchen Solutions', 'contact': '+960 444-5678'},
        {'id': 'electric_supply', 'name': 'Electric Supply Maldives', 'contact': '+960 333-9999'}
    ]

if "locations" not in st.session_state:
    st.session_state.locations = [
        {'id': 'vahmaafushi', 'name': 'Vahmaafushi', 'icon': '🏝️', 'description': 'Picnic Island Project'},
        {'id': 'keyodhoo', 'name': 'Keyodhoo', 'icon': '🏨', 'description': 'Guest House Project'},
        {'id': 'male', 'name': 'Male', 'icon': '🏪', 'description': 'Godown & Storage'},
        {'id': 'hulhumale', 'name': 'Hulhumale', 'icon': '🏢', 'description': 'Airbnb 10 Floor Project'}
    ]

if "project_areas" not in st.session_state:
    st.session_state.project_areas = {
        'vahmaafushi': ['General', 'Jetty', 'Beach'],
        'keyodhoo': ['Guesthouse Block A', 'Block B'],
        'male': ['Warehouse 1', 'Warehouse 2'],
        'hulhumale': ['Tower 1', 'Tower 2']
    }

if "cash_categories" not in st.session_state:
    st.session_state.cash_categories = [
        'Material Purchase', 'Transportation', 'Labor Payment', 'Equipment Rental',
        'Fuel & Utilities', 'Food & Accommodation', 'Client Payment', 'Project Advance',
        'Insurance', 'Permits & Licenses', 'Others'
    ]

if "payment_methods" not in st.session_state:
    st.session_state.payment_methods = [
        'Cash', 'Bank Transfer', 'Mobile Payment (BML)', 'Cheque', 'Credit Card'
    ]

if "cash_transactions" not in st.session_state:
    st.session_state.cash_transactions = []

if "materials" not in st.session_state:
    st.session_state.materials = []

if "deliveries" not in st.session_state:
    st.session_state.deliveries = []

if "categories" not in st.session_state:
    st.session_state.categories = [
        'Construction Materials', 'Furniture & Fixtures', 'Kitchen Equipment',
        'Electrical Items', 'Safety Equipment', 'Tools & Equipment', 'Plumbing Materials'
    ]

# ✅ Page Configuration
st.set_page_config(
    page_title="Multi-Location Project Management System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance and mobile responsiveness
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1, .main-header h2, .main-header p {
        color: white !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .location-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .success-box {
        background: #d4edda;
        border: 2px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .info-box {
        background: #e7f3ff;
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #004085 !important;
    }
    
    .info-box * {
        color: #004085 !important;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    
    .feature-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        color: #212529 !important;
    }
    
    .feature-card * {
        color: #212529 !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        color: #212529 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #212529 !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        color: #212529 !important;
    }
    
    /* Fix input field text visibility */
    input[type="text"], input[type="password"], input[type="number"] {
        color: #212529 !important;
        background-color: #f8f9fa !important;
    }
    
    /* Fix dropdown text visibility */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #212529 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] span {
        color: #212529 !important;
    }
    
    .delivery-note {
        background: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
        white-space: pre-line;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem;
        }
        .main-header p {
            font-size: 0.9rem;
        }
        .metric-card {
            margin: 0.25rem 0;
            padding: 1rem;
        }
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Global text color fixes */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #212529 !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label {
        color: #212529 !important;
    }
    
    .stButton button {
        color: white !important;
    }
    
    .stRadio label, .stCheckbox label {
        color: #212529 !important;
    }
    
    .stExpander .streamlit-expanderHeader {
        color: #212529 !important;
    }
    
    .stTab button {
        color: #212529 !important;
    }
    
    .stMetric label {
        color: #212529 !important;
    }
    
    /* Success box text */
    .success-box * {
        color: #155724 !important;
    }
    
    /* Warning box text */
    .warning-box * {
        color: #856404 !important;
    }
    
    /* Additional input field fixes */
    .stTextInput input, .stPasswordInput input, .stNumberInput input {
        color: #212529 !important;
        background-color: white !important;
    }
    
    /* Radio button text */
    .stRadio > div > div > div > label {
        color: #212529 !important;
    }
    
    /* Dropdown menu options */
    .stSelectbox ul {
        color: #212529 !important;
    }
    
    .stSelectbox li {
        color: #212529 !important;
    }
    
    /* Make sure text is visible in all input states */
    .stTextInput > div > div > input:focus {
        color: #212529 !important;
    }
    
    .stSelectbox > div > div:focus {
        color: #212529 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with all required data
def init_session_state():
    defaults = {
        'materials': [],
        'deliveries': [],
        'cash_transactions': [],
        'invoices': [],
        'usage_records': [],
        'receivables': [],
        'payables': [],
        'locations': [
            {'id': 'vahmaafushi', 'name': 'Vahmaafushi', 'icon': '🏝️', 'description': 'Picnic Island Project'},
            {'id': 'keyodhoo', 'name': 'Keyodhoo', 'icon': '🏨', 'description': 'Guest House Project'},
            {'id': 'male', 'name': "Male'", 'icon': '🏪', 'description': 'Godown & Storage'},
            {'id': 'hulhumale', 'name': "Hulhumale'", 'icon': '🏢', 'description': 'Airbnb 10 Floor Project'}
        ],
        'categories': [
            'Construction Materials', 'Furniture & Fixtures', 'Kitchen Equipment', 
            'Electrical Items', 'Safety Equipment', 'Tools & Equipment', 'Plumbing Materials'
        ],
        'suppliers': [
            {'id': 'local_hardware', 'name': 'Local Hardware Co.', 'contact': '+960 123-4567'},
            {'id': 'steel_industries', 'name': 'Steel Industries Pvt Ltd', 'contact': '+960 987-6543'},
            {'id': 'furniture_plus', 'name': 'Furniture Plus', 'contact': '+960 555-1234'},
            {'id': 'kitchen_solutions', 'name': 'Kitchen Solutions', 'contact': '+960 444-5678'},
            {'id': 'electric_supply', 'name': 'Electric Supply Maldives', 'contact': '+960 333-9999'}
        ],
        'project_areas': {
            'Vahmaafushi': ['Temporary Building', 'Zip Line Tower', 'Beach Facilities', 'Electrical Infrastructure', 'Parking Area', 'Entrance Gate'],
            'Keyodhoo': ['Guest Rooms', 'Reception Area', 'Restaurant', 'Common Areas', 'Kitchen', 'Staff Quarters'],
            'Male\'': ['Storage & Warehouse', 'Material Distribution', 'Transfer Coordination', 'Office Area'],
            'Hulhumale\'': ['Apartment Units (Floor 1-3)', 'Apartment Units (Floor 4-6)', 'Apartment Units (Floor 7-10)', 'Common Facilities', 'Parking & Utilities', 'Reception']
        },
        'payment_methods': ['Cash', 'Bank Transfer', 'Mobile Payment (BML)', 'Cheque', 'Credit Card'],
        'cash_categories': [
            'Material Purchase', 'Transportation', 'Labor Payment', 'Equipment Rental', 
            'Fuel & Utilities', 'Food & Accommodation', 'Client Payment', 'Project Advance', 
            'Insurance', 'Permits & Licenses', 'Others'
        ]
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    from db_handler import get_all_materials


    # Load existing materials from the database only if session_state is empty
    if not st.session_state.materials:
        st.session_state.materials = get_all_materials()


#init_session_state()

# Utility Functions
def get_location_icon(location_name):
    """Get icon for a location"""
    for loc in st.session_state.locations:
        if loc['name'] == location_name:
            return loc['icon']
    return '📍'

def format_currency(amount):
    """Format amount in MVR currency"""
    return f"MVR {amount:,.2f}"

def save_to_file(content, filename):
    """Save content to file for download"""
    return base64.b64encode(content.encode()).decode()

def calculate_material_status(material):
    """Calculate material delivery status"""
    delivered = material.get('delivered', 0)
    total_ordered = material.get('total_ordered', 0)
    
    if delivered == 0:
        return "Pending Delivery"
    elif delivered < total_ordered:
        return "Partially Delivered"
    else:
        return "Fully Delivered"

# Main Application Header
st.markdown("""
<div class="main-header">
    <h1>🏗️ Multi-Location Project Management System</h1>
    <p>Comprehensive project management for multiple construction sites</p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
st.markdown("### 🛠 Complete System Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h4>📦 Materials</h4>
    <p>Track inventory, deliveries & usage across all locations</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h4>🚚 Deliveries</h4>
    <p>Monitor delivery schedules and tracking information</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h4>💰 Finances</h4>
    <p>Manage cash flow, invoices & payment tracking</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
    <h4>📊 Reports</h4>
    <p>Generate detailed reports and analytics</p>
    </div>
    """, unsafe_allow_html=True)

# Location Overview
st.markdown("---")
st.markdown("### 🏗️ Project Locations")

location_cols = st.columns(len(st.session_state.locations))
for i, location in enumerate(st.session_state.locations):
    with location_cols[i]:
        st.markdown(f"""
        <div class="location-card">
            <h3>{location['icon']} {location['name']}</h3>
            <p>{location['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# Main Navigation
st.markdown("---")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📦 Materials Management", 
    "🚚 Delivery Tracking", 
    "💰 Financial Management", 
    "📋 Usage Records", 
    "📊 Reports & Analytics",
    "⚙️ System Settings"
])

# Materials Management Tab
with tab1:
    st.header("📦 Materials Management")
    
    # Sub-tabs for materials
    materials_tab1, materials_tab2, materials_tab3 = st.tabs([
        "➕ Add New Material", 
        "📋 View Materials", 
        "🔄 Update Stock"
    ])
    
    with materials_tab1:
        st.subheader("Add New Material")
        
        col1, col2 = st.columns(2)
        
        with col1:
            material_name = st.text_input("Material Name")
            category = st.selectbox("Category", st.session_state.categories, key="add_material_category")
            supplier_options = [f"{s['name']} ({s['contact']})" for s in st.session_state.suppliers]
            supplier = st.selectbox("Supplier", supplier_options, key="add_material_supplier")
            location = st.selectbox("Location", [loc['name'] for loc in st.session_state.locations], key="add_material_location")
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            unit_price = st.number_input("Unit Price (MVR)", min_value=0.0, value=0.0, step=0.01)
            total_cost = quantity * unit_price
            st.metric("Total Cost", format_currency(total_cost))
            order_date = st.date_input("Order Date", value=date.today())
        
        project_area = st.selectbox(
            "Project Area", 
            st.session_state.project_areas.get(location, ['General']),
            key="add_material_project_area"
        )
        
        notes = st.text_area("Notes/Description")
        
        if st.button("➕ Add Material", key="add_material"):
            if material_name and category and supplier and location:
                new_material = {
                    'id': len(st.session_state.materials) + 1,
                    'name': material_name,
                    'category': category,
                    'supplier': supplier,
                    'location': location,
                    'project_area': project_area,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_cost': total_cost,
                    'order_date': order_date.strftime('%Y-%m-%d'),
                    'delivered': 0,
                    'total_ordered': quantity,
                    'status': 'Pending Delivery',
                    'notes': notes,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                st.session_state.materials.append(new_material)
                insert_material((
    material_name, category, supplier, location, project_area,
    quantity, unit_price, total_cost, order_date.strftime('%Y-%m-%d'),
    0, notes
))

                st.success(f"✅ Material '{material_name}' added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields")
    
    with materials_tab2:
        st.subheader("Materials Inventory")
        
        if st.session_state.materials:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                location_filter = st.selectbox(
                    "Filter by Location", 
                    ["All"] + [loc['name'] for loc in st.session_state.locations],
                    key="view_materials_location_filter"
                )
            
            with col2:
                category_filter = st.selectbox(
                    "Filter by Category", 
                    ["All"] + st.session_state.categories,
                    key="view_materials_category_filter"
                )
            
            with col3:
                status_filter = st.selectbox(
                    "Filter by Status", 
                    ["All", "Pending Delivery", "Partially Delivered", "Fully Delivered"],
                    key="view_materials_status_filter"
                )
            
            # Filter materials
            filtered_materials = st.session_state.materials.copy()
            
            if location_filter != "All":
                filtered_materials = [m for m in filtered_materials if m['location'] == location_filter]
            
            if category_filter != "All":
                filtered_materials = [m for m in filtered_materials if m['category'] == category_filter]
            
            if status_filter != "All":
                filtered_materials = [m for m in filtered_materials if calculate_material_status(m) == status_filter]
            
            # Display materials
            if filtered_materials:
                materials_df = pd.DataFrame(filtered_materials)
                
                # Add calculated status column
                materials_df['delivery_status'] = materials_df.apply(calculate_material_status, axis=1)
                
                # Display columns
                display_columns = [
                    'name', 'category', 'location', 'project_area', 'quantity', 
                    'unit_price', 'total_cost', 'delivered', 'delivery_status', 'order_date'
                ]
                
                st.dataframe(
                    materials_df[display_columns],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Summary metrics
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_materials = len(filtered_materials)
                    st.metric("Total Materials", total_materials)
                
                with col2:
                    total_cost = sum(m['total_cost'] for m in filtered_materials)
                    st.metric("Total Value", format_currency(total_cost))
                
                with col3:
                    pending_count = len([m for m in filtered_materials if calculate_material_status(m) == "Pending Delivery"])
                    st.metric("Pending Deliveries", pending_count)
                
                with col4:
                    delivered_count = len([m for m in filtered_materials if calculate_material_status(m) == "Fully Delivered"])
                    st.metric("Fully Delivered", delivered_count)
            else:
                st.info("No materials found matching the selected filters.")
        else:
            st.info("No materials added yet. Use the 'Add New Material' tab to get started.")
    
    with materials_tab3:
        st.subheader("Update Material Stock")
        
        if st.session_state.materials:
            # Select material to update
            material_options = [f"{m['name']} - {m['location']} (ID: {m['id']})" for m in st.session_state.materials]
            selected_material_option = st.selectbox("Select Material to Update", material_options, key="update_stock_material_select")
            
            if selected_material_option:
                # Extract material ID
                material_id = int(selected_material_option.split("ID: ")[1].split(")")[0])
                selected_material = next((m for m in st.session_state.materials if m['id'] == material_id), None)
                
                if selected_material:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Material:** {selected_material['name']}")
                        st.write(f"**Location:** {selected_material['location']}")
                        st.write(f"**Total Ordered:** {selected_material['total_ordered']}")
                        st.write(f"**Already Delivered:** {selected_material['delivered']}")
                        remaining = selected_material['total_ordered'] - selected_material['delivered']
                        st.write(f"**Remaining:** {remaining}")
                    
                    with col2:
                        delivery_amount = st.number_input(
                            "Delivery Amount", 
                            min_value=1, 
                            max_value=remaining,
                            value=min(remaining, 1) if remaining > 0 else 0
                        )
                        delivery_date = st.date_input("Delivery Date", value=date.today())
                        delivery_notes = st.text_area("Delivery Notes")
                    
                    if st.button("✅ Update Delivery", key="update_delivery"):
                        if delivery_amount > 0:
                            # Update material in session
                            selected_material['delivered'] += delivery_amount

                            # ✅ Save update to DB
                            update_delivery(selected_material['id'], delivery_amount) 

                            # Create delivery record
                            delivery_record = {
                                'id': len(st.session_state.deliveries) + 1,
                                'material_id': selected_material['id'],
                                'material_name': selected_material['name'],
                                'location': selected_material['location'],
                                'quantity_delivered': delivery_amount,
                                'delivery_date': delivery_date.strftime('%Y-%m-%d'),
                                'notes': delivery_notes,
                                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            st.session_state.deliveries.append(delivery_record)
                            from db_handler import insert_delivery
                            insert_delivery(delivery_record)

                            st.success(f"✅ Delivery updated: {delivery_amount} units of {selected_material['name']}")
                            st.rerun()
                        else:
                            st.error("❌ Please enter a delivery amount greater than 0")
        else:
            st.info("No materials available to update. Add materials first.")

# Delivery Tracking Tab
with tab2:
    st.header("🚚 Delivery Tracking")
    
    delivery_tab1, delivery_tab2 = st.tabs(["📋 View Deliveries", "📊 Delivery Analytics"])
    
    with delivery_tab1:
        st.subheader("Delivery Records")
        
        if st.session_state.deliveries:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                location_filter = st.selectbox(
                    "Filter by Location", 
                    ["All"] + [loc['name'] for loc in st.session_state.locations],
                    key="delivery_tracking_location_filter"
                )
            
            with col2:
                date_range = st.selectbox(
                    "Date Range", 
                    ["All Time", "Last 7 Days", "Last 30 Days", "This Month"],
                    key="delivery_tracking_date_filter"
                )
            
            # Filter deliveries
            filtered_deliveries = st.session_state.deliveries.copy()
            
            if location_filter != "All":
                filtered_deliveries = [d for d in filtered_deliveries if d['location'] == location_filter]
            
            # Apply date filter
            if date_range != "All Time":
                today = datetime.now().date()
                if date_range == "Last 7 Days":
                    cutoff_date = today - timedelta(days=7)
                elif date_range == "Last 30 Days":
                    cutoff_date = today - timedelta(days=30)
                elif date_range == "This Month":
                    cutoff_date = today.replace(day=1)
                else:
                    cutoff_date = today
                
                filtered_deliveries = [
                    d for d in filtered_deliveries 
                    if datetime.strptime(d['delivery_date'], '%Y-%m-%d').date() >= cutoff_date
                ]
            
            if filtered_deliveries:
                deliveries_df = pd.DataFrame(filtered_deliveries)
                
                display_columns = [
                    'material_name', 'location', 'quantity_delivered', 
                    'delivery_date', 'notes'
                ]
                
                st.dataframe(
                    deliveries_df[display_columns],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Summary
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_deliveries = len(filtered_deliveries)
                    st.metric("Total Deliveries", total_deliveries)
                
                with col2:
                    total_items = sum(d['quantity_delivered'] for d in filtered_deliveries)
                    st.metric("Total Items Delivered", total_items)
                
                with col3:
                    unique_materials = len(set(d['material_name'] for d in filtered_deliveries))
                    st.metric("Unique Materials", unique_materials)
            else:
                st.info("No deliveries found matching the selected filters.")
        else:
            st.info("No delivery records available. Deliveries are created when you update material stock.")
    
    with delivery_tab2:
        st.subheader("Delivery Analytics")
        
        if st.session_state.deliveries:
            # Delivery trends
            st.markdown("#### 📈 Delivery Trends")
            
            deliveries_df = pd.DataFrame(st.session_state.deliveries)
            deliveries_df['delivery_date'] = pd.to_datetime(deliveries_df['delivery_date'])
            
            # Group by date
            daily_deliveries = deliveries_df.groupby('delivery_date')['quantity_delivered'].sum()
            
            if len(daily_deliveries) > 1:
                st.line_chart(daily_deliveries)
            else:
                st.info("Not enough data for trend analysis")
        else:
            st.info("No delivery data available for analytics.")

# Financial Management Tab
with tab3:
    st.header("💰 Financial Management")
    
    finance_tab1, finance_tab2, finance_tab3, finance_tab4 = st.tabs([
        "💸 Cash Transactions", 
        "🧾 Invoices", 
        "📥 Receivables", 
        "📤 Payables"
    ])
    
    with finance_tab1:
        st.subheader("Cash Transaction Management")
        
        cash_sub_tab1, cash_sub_tab2 = st.tabs(["➕ New Transaction", "📋 View Transactions"])
        
        with cash_sub_tab1:
            st.subheader("Record New Cash Transaction")
            
            col1, col2 = st.columns(2)
            
            with col1:
                transaction_type = st.radio("Transaction Type", ["Income", "Expense"])
                amount = st.number_input("Amount (MVR)", min_value=0.0, value=0.0, step=0.01)
                category = st.selectbox("Category", st.session_state.cash_categories, key="cash_transaction_category")
                location = st.selectbox("Location", [loc['name'] for loc in st.session_state.locations], key="cash_transaction_location")
            
            with col2:
                payment_method = st.selectbox("Payment Method", st.session_state.payment_methods, key="cash_transaction_payment_method")
                transaction_date = st.date_input("Transaction Date", value=date.today())
                reference = st.text_input("Reference/Receipt No.")
            
            description = st.text_area("Description")
            
            if st.button("💰 Record Transaction", key="add_cash_transaction"):
                if amount > 0 and category and description:
                    new_transaction = {
                        'id': len(st.session_state.cash_transactions) + 1,
                        'type': transaction_type,
                        'amount': amount,
                        'category': category,
                        'location': location,
                        'payment_method': payment_method,
                        'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                        'reference': reference,
                        'description': description,
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    st.session_state.cash_transactions.append(new_transaction)
                    st.success(f"✅ {transaction_type} transaction recorded: {format_currency(amount)}")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields")
        
        with cash_sub_tab2:
            st.subheader("Cash Transaction History")
            
            if st.session_state.cash_transactions:
                # Filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    type_filter = st.selectbox(
                        "Filter by Type", 
                        ["All", "Income", "Expense"],
                        key="cash_type_filter"
                    )
                
                with col2:
                    location_filter = st.selectbox(
                        "Filter by Location", 
                        ["All"] + [loc['name'] for loc in st.session_state.locations],
                        key="cash_location_filter"
                    )
                
                with col3:
                    category_filter = st.selectbox(
                        "Filter by Category", 
                        ["All"] + st.session_state.cash_categories,
                        key="cash_category_filter"
                    )
                
                # Apply filters
                filtered_transactions = st.session_state.cash_transactions.copy()
                
                if type_filter != "All":
                    filtered_transactions = [t for t in filtered_transactions if t['type'] == type_filter]
                
                if location_filter != "All":
                    filtered_transactions = [t for t in filtered_transactions if t['location'] == location_filter]
                
                if category_filter != "All":
                    filtered_transactions = [t for t in filtered_transactions if t['category'] == category_filter]
                
                if filtered_transactions:
                    df = pd.DataFrame(filtered_transactions)
                    st.dataframe(df, use_container_width=True, hide_index=True)

                    # Summary
                    total_income = sum(t['amount'] for t in filtered_transactions if t['type'] == "Income")
                    total_expense = sum(t['amount'] for t in filtered_transactions if t['type'] == "Expense")
                    net = total_income - total_expense

                    col1, col2, col3 = st.columns(3)
                    with col1: st.metric("Total Income", format_currency(total_income))
                    with col2: st.metric("Total Expense", format_currency(total_expense))
                    with col3: st.metric("Net Cash Flow", format_currency(net))

# -------------------- Invoices Tab --------------------
with finance_tab2:
    st.subheader("🧾 Invoice Management")
    st.write("Coming soon: Create, view, and manage invoices here.")

# -------------------- Receivables Tab --------------------
with finance_tab3:
    st.subheader("📥 Accounts Receivable")
    st.write("Coming soon: Track outstanding client payments here.")

# -------------------- Payables Tab --------------------
with finance_tab4:
    st.subheader("📤 Accounts Payable")
    st.write("Coming soon: Manage supplier/vendor payments here.")

# -------------------- Usage Records Tab --------------------
with tab4:
    st.header("📋 Usage Records")
    st.write("Feature under development: You will record and track material usage here.")

# -------------------- Reports & Analytics Tab --------------------
with tab5:
    st.header("📊 Reports & Analytics")
    st.write("Feature under development: Generate reports and analytics here.")

# -------------------- System Settings Tab --------------------
with tab6:
    st.header("⚙️ System Settings")
    st.write("Feature under development: Manage system preferences and configurations here.")

                
 