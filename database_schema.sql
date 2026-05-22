-- Sanket's Computers & Sales - Complete Database Schema
-- Host: localhost
-- Database: computersales_db

-- ============================================
-- USERS & AUTHENTICATION TABLES
-- ============================================

-- Admin Users Table
CREATE TABLE IF NOT EXISTS tbl_adminsign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    confirm_password VARCHAR(255) NOT NULL,
    profile_image VARCHAR(255) DEFAULT NULL,
    is_super_admin TINYINT(1) DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Customer Users Table
CREATE TABLE IF NOT EXISTS tbl_usersign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    confirm_password VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    profile_image VARCHAR(255) DEFAULT NULL,
    is_active TINYINT(1) DEFAULT 1,
    is_verified TINYINT(1) DEFAULT 0,
    google_id VARCHAR(100) DEFAULT NULL,
    loyalty_points INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- OTP Verification Table
CREATE TABLE IF NOT EXISTS tbl_otp_verification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    otp_code VARCHAR(10) NOT NULL,
    otp_type ENUM('email', 'phone', 'reset') DEFAULT 'email',
    is_used TINYINT(1) DEFAULT 0,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Delivery Boy Table
CREATE TABLE IF NOT EXISTS tbl_delivery_boy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    vehicle_number VARCHAR(20),
    aadhar_number VARCHAR(20),
    profile_image VARCHAR(255) DEFAULT NULL,
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    is_available TINYINT(1) DEFAULT 1,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- PRODUCT CATALOG TABLES
-- ============================================

-- Categories Table
CREATE TABLE IF NOT EXISTS tbl_addcategory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_image VARCHAR(255) NOT NULL,
    description TEXT,
    parent_id INT DEFAULT NULL,
    is_active TINYINT(1) DEFAULT 1,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES tbl_addcategory(id) ON DELETE SET NULL
);

-- Products Table
CREATE TABLE IF NOT EXISTS tbl_addproduct (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2) DEFAULT NULL,
    quantity INT DEFAULT 0,
    description TEXT,
    specifications TEXT,
    category INT NOT NULL,
    product_image VARCHAR(255) NOT NULL,
    gallery_images TEXT,
    is_active TINYINT(1) DEFAULT 1,
    is_featured TINYINT(1) DEFAULT 0,
    is_new_arrival TINYINT(1) DEFAULT 0,
    is_flash_sale TINYINT(1) DEFAULT 0,
    flash_sale_price DECIMAL(10, 2) DEFAULT NULL,
    flash_sale_end DATETIME DEFAULT NULL,
    warranty_months INT DEFAULT 12,
    return_days INT DEFAULT 7,
    rating DECIMAL(3, 2) DEFAULT 0,
    total_reviews INT DEFAULT 0,
    views INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category) REFERENCES tbl_addcategory(id)
);

-- Product Reviews Table
CREATE TABLE IF NOT EXISTS tbl_product_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    review_text TEXT,
    is_verified_purchase TINYINT(1) DEFAULT 0,
    is_approved TINYINT(1) DEFAULT 1,
    helpful_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE CASCADE
);

-- Product Compare Table
CREATE TABLE IF NOT EXISTS tbl_product_compare (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    user_id INT DEFAULT NULL,
    product_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE CASCADE
);

-- ============================================
-- E-COMMERCE TABLES
-- ============================================

-- Wishlist Table
CREATE TABLE IF NOT EXISTS tbl_wishlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE CASCADE,
    UNIQUE KEY unique_wishlist (user_id, product_id)
);

-- Coupons Table
CREATE TABLE IF NOT EXISTS tbl_coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coupon_code VARCHAR(50) UNIQUE NOT NULL,
    coupon_type ENUM('percentage', 'fixed') NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2) DEFAULT NULL,
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    usage_limit INT DEFAULT NULL,
    usage_count INT DEFAULT 0,
    per_user_limit INT DEFAULT 1,
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User Coupon Usage Table
CREATE TABLE IF NOT EXISTS tbl_user_coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    coupon_id INT NOT NULL,
    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE CASCADE,
    FOREIGN KEY (coupon_id) REFERENCES tbl_coupons(id) ON DELETE CASCADE
);

-- Loyalty Points Transactions
CREATE TABLE IF NOT EXISTS tbl_loyalty_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    points INT NOT NULL,
    transaction_type ENUM('earn', 'redeem', 'expire', 'bonus') NOT NULL,
    description VARCHAR(255),
    order_id INT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE CASCADE
);

-- Cart Table
CREATE TABLE IF NOT EXISTS tbl_cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    user_id INT DEFAULT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE CASCADE
);

-- ============================================
-- ORDERS & PAYMENT TABLES
-- ============================================

-- Orders Table
CREATE TABLE IF NOT EXISTS tbl_booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    shipping_address TEXT,
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_pincode VARCHAR(10),
    billing_address TEXT,
    enter_product VARCHAR(200) NOT NULL,
    product_id INT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    coupon_discount DECIMAL(10, 2) DEFAULT 0,
    loyalty_discount DECIMAL(10, 2) DEFAULT 0,
    shipping_charge DECIMAL(10, 2) DEFAULT 0,
    gst_amount DECIMAL(10, 2) DEFAULT 0,
    final_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    payment_date DATETIME DEFAULT NULL,
    transaction_id VARCHAR(100) DEFAULT NULL,
    booking_status ENUM('Pending', 'Confirmed', 'Packed', 'Shipped', 'Out for Delivery', 'Delivered', 'Canceled', 'Returned') DEFAULT 'Pending',
    is_canceled TINYINT(1) DEFAULT 0,
    cancellation_date DATETIME DEFAULT NULL,
    cancellation_reason TEXT,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATETIME DEFAULT NULL,
    estimated_delivery_date DATETIME,
    delivery_otp VARCHAR(6) DEFAULT NULL,
    delivery_boy_id INT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id),
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id),
    FOREIGN KEY (delivery_boy_id) REFERENCES tbl_delivery_boy(id)
);

-- Order Items Table (for multiple items per order)
CREATE TABLE IF NOT EXISTS tbl_order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    brand VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id)
);

-- Order Status History
CREATE TABLE IF NOT EXISTS tbl_order_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    notes TEXT,
    updated_by INT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id) ON DELETE CASCADE
);

-- Payment Transactions
CREATE TABLE IF NOT EXISTS tbl_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_id VARCHAR(100),
    payment_status ENUM('pending', 'success', 'failed', 'refunded') DEFAULT 'pending',
    response_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id) ON DELETE CASCADE
);

-- GST Invoices Table
CREATE TABLE IF NOT EXISTS tbl_gst_invoice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    gstin VARCHAR(15),
    billing_name VARCHAR(100),
    billing_address TEXT,
    billing_state VARCHAR(100),
    billing_gstin VARCHAR(15),
    cgst_rate DECIMAL(5, 2) DEFAULT 0,
    sgst_rate DECIMAL(5, 2) DEFAULT 0,
    igst_rate DECIMAL(5, 2) DEFAULT 0,
    cgst_amount DECIMAL(10, 2) DEFAULT 0,
    sgst_amount DECIMAL(10, 2) DEFAULT 0,
    igst_amount DECIMAL(10, 2) DEFAULT 0,
    total_gst DECIMAL(10, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id)
);

-- Returns & Refunds Table
CREATE TABLE IF NOT EXISTS tbl_returns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    return_reason TEXT NOT NULL,
    return_type ENUM('refund', 'exchange', 'repair') DEFAULT 'refund',
    status ENUM('pending', 'approved', 'rejected', 'processed') DEFAULT 'pending',
    refund_amount DECIMAL(10, 2),
    admin_notes TEXT,
    processed_at DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id),
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id)
);

-- ============================================
-- DELIVERY & TRACKING TABLES
-- ============================================

-- Delivery Boy Orders Assignment
CREATE TABLE IF NOT EXISTS tbl_delivery_assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_boy_id INT NOT NULL,
    pickup_address TEXT,
    delivery_address TEXT,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    picked_up_at DATETIME DEFAULT NULL,
    delivered_at DATETIME DEFAULT NULL,
    status ENUM('assigned', 'picked_up', 'in_transit', 'delivered', 'failed') DEFAULT 'assigned',
    delivery_notes TEXT,
    FOREIGN KEY (order_id) REFERENCES tbl_booking(id),
    FOREIGN KEY (delivery_boy_id) REFERENCES tbl_delivery_boy(id)
);

-- Delivery Location History
CREATE TABLE IF NOT EXISTS tbl_delivery_location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    delivery_boy_id INT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (delivery_boy_id) REFERENCES tbl_delivery_boy(id)
);

-- ============================================
-- COMMUNICATION TABLES
-- ============================================

-- Feedback Table
CREATE TABLE IF NOT EXISTS tbl_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email_address VARCHAR(100),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    your_feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Complaints Table
CREATE TABLE IF NOT EXISTS tbl_complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    number VARCHAR(20),
    complaint_type VARCHAR(100),
    complaint_descrip TEXT,
    status ENUM('pending', 'resolved', 'in_progress') DEFAULT 'pending',
    admin_response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME DEFAULT NULL
);

-- Notifications Table
CREATE TABLE IF NOT EXISTS tbl_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type ENUM('order', 'payment', 'delivery', 'promotion', 'system') DEFAULT 'system',
    is_read TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE CASCADE
);

-- Chat Messages (AI Chatbot & Support)
CREATE TABLE IF NOT EXISTS tbl_chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    user_id INT DEFAULT NULL,
    message_text TEXT NOT NULL,
    message_type ENUM('user', 'bot') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AI & ANALYTICS TABLES
-- ============================================

-- Product Recommendations (AI)
CREATE TABLE IF NOT EXISTS tbl_product_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT NOT NULL,
    recommendation_type ENUM('similar', 'frequently_bought', 'trending', 'personalized') NOT NULL,
    score DECIMAL(5, 4),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE CASCADE
);

-- Search History
CREATE TABLE IF NOT EXISTS tbl_search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    session_id VARCHAR(100),
    search_query VARCHAR(255) NOT NULL,
    results_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES tbl_usersign(id) ON DELETE SET NULL
);

-- Page Views Analytics
CREATE TABLE IF NOT EXISTS tbl_page_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    page_url VARCHAR(255) NOT NULL,
    user_id INT DEFAULT NULL,
    session_id VARCHAR(100),
    viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tbl_addproduct(id) ON DELETE SET NULL
);

-- ============================================
-- SETTINGS & CONFIGURATION TABLES
-- ============================================

-- Website Settings
CREATE TABLE IF NOT EXISTS tbl_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Banner Management
CREATE TABLE IF NOT EXISTS tbl_banners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    banner_type ENUM('main', 'deal', 'flash_sale', 'category', 'popup') NOT NULL,
    title VARCHAR(200),
    subtitle VARCHAR(200),
    banner_image VARCHAR(255) NOT NULL,
    link_url VARCHAR(255),
    is_active TINYINT(1) DEFAULT 1,
    sort_order INT DEFAULT 0,
    start_date DATETIME,
    end_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Settings
INSERT INTO tbl_settings (setting_key, setting_value) VALUES
('site_name', 'Sanket''s Computers & Sales'),
('site_email', 'sankettippe9766@gmail.com'),
('site_phone', '+91 9766575428'),
('site_address', 'Computer Sales & Service Center'),
('upi_id', 'sankettippe9766@oksbi'),
('razorpay_key_id', ''),
('razorpay_key_secret', ''),
('free_shipping_threshold', '1000'),
('shipping_charge', '100'),
('tax_rate', '18'),
('loyalty_points_ratio', '1'), -- 1 point per Rs 10
('max_cart_items', '100'),
('default_return_days', '7'),
('default_warranty_months', '12'),
('google_client_id', ''),
('google_client_secret', ''),
('facebook_app_id', ''),
('facebook_app_secret', ''),
('email_from', 'noreply@sanketscomputers.com'),
('email_username', ''),
('email_password', ''),
('sms_api_key', ''),
('sms_sender_id', '');

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_products_category ON tbl_addproduct(category);
CREATE INDEX idx_products_active ON tbl_addproduct(is_active);
CREATE INDEX idx_products_rating ON tbl_addproduct(rating DESC);
CREATE INDEX idx_orders_user ON tbl_booking(user_id);
CREATE INDEX idx_orders_status ON tbl_booking(booking_status);
CREATE INDEX idx_orders_date ON tbl_booking(booking_date DESC);
CREATE INDEX idx_cart_session ON tbl_cart(session_id);
CREATE INDEX idx_cart_user ON tbl_cart(user_id);
CREATE INDEX idx_wishlist_user ON tbl_wishlist(user_id);
CREATE INDEX idx_notifications_user ON tbl_notifications(user_id);
CREATE INDEX idx_recommendations_user ON tbl_product_recommendations(user_id);