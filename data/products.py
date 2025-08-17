"""
Product catalog with sample data for phones, laptops, and tablets.
Each product includes detailed specifications for better recommendation matching.
"""

PRODUCTS = [
    # Smartphones
    {
        "id": "phone_001",
        "name": "iPhone 15 Pro",
        "category": "phone",
        "brand": "Apple",
        "price": 999,
        "description": "Latest iPhone with A17 Pro chip, titanium design, and advanced camera system",
        "specs": {
            "screen_size": "6.1 inches",
            "storage": "128GB",
            "ram": "8GB",
            "processor": "A17 Pro",
            "camera": "48MP main + 12MP ultra-wide + 12MP telephoto",
            "battery": "3274mAh",
            "os": "iOS 17"
        },
        "features": ["5G", "Face ID", "Wireless charging", "Water resistant", "Titanium frame"],
        "tags": ["premium", "camera", "gaming", "business", "photography"]
    },
    {
        "id": "phone_002",
        "name": "Samsung Galaxy S24 Ultra",
        "category": "phone",
        "brand": "Samsung",
        "price": 1299,
        "description": "Premium Android flagship with S Pen, advanced AI features, and exceptional camera",
        "specs": {
            "screen_size": "6.8 inches",
            "storage": "256GB",
            "ram": "12GB",
            "processor": "Snapdragon 8 Gen 3",
            "camera": "200MP main + 12MP ultra-wide + 50MP telephoto + 10MP telephoto",
            "battery": "5000mAh",
            "os": "Android 14"
        },
        "features": ["5G", "S Pen", "Wireless charging", "Water resistant", "AI features"],
        "tags": ["premium", "camera", "productivity", "business", "creativity"]
    },
    {
        "id": "phone_003",
        "name": "Google Pixel 8",
        "category": "phone",
        "brand": "Google",
        "price": 699,
        "description": "AI-powered smartphone with exceptional camera and clean Android experience",
        "specs": {
            "screen_size": "6.2 inches",
            "storage": "128GB",
            "ram": "8GB",
            "processor": "Google Tensor G3",
            "camera": "50MP main + 12MP ultra-wide",
            "battery": "4575mAh",
            "os": "Android 14"
        },
        "features": ["5G", "AI camera", "Wireless charging", "Water resistant", "Google Assistant"],
        "tags": ["camera", "AI", "mid-range", "photography", "clean UI"]
    },
    {
        "id": "phone_004",
        "name": "OnePlus 12",
        "category": "phone",
        "brand": "OnePlus",
        "price": 799,
        "description": "Fast performance with Hasselblad camera system and rapid charging",
        "specs": {
            "screen_size": "6.82 inches",
            "storage": "256GB",
            "ram": "16GB",
            "processor": "Snapdragon 8 Gen 3",
            "camera": "50MP main + 48MP ultra-wide + 64MP telephoto",
            "battery": "5400mAh",
            "os": "Android 14"
        },
        "features": ["5G", "100W charging", "Wireless charging", "Water resistant", "Hasselblad camera"],
        "tags": ["performance", "fast charging", "camera", "gaming", "value"]
    },
    
    # Laptops
    {
        "id": "laptop_001",
        "name": "MacBook Pro 14-inch",
        "category": "laptop",
        "brand": "Apple",
        "price": 1999,
        "description": "Professional laptop with M3 Pro chip, perfect for creative work and development",
        "specs": {
            "screen_size": "14.2 inches",
            "storage": "512GB SSD",
            "ram": "18GB",
            "processor": "M3 Pro",
            "gpu": "Integrated",
            "battery": "Up to 22 hours",
            "os": "macOS Sonoma"
        },
        "features": ["Retina display", "Touch Bar", "Thunderbolt 4", "Backlit keyboard", "Force Touch trackpad"],
        "tags": ["premium", "creative", "development", "business", "portable"]
    },
    {
        "id": "laptop_002",
        "name": "Dell XPS 13 Plus",
        "category": "laptop",
        "brand": "Dell",
        "price": 1499,
        "description": "Ultra-slim premium Windows laptop with excellent performance and design",
        "specs": {
            "screen_size": "13.4 inches",
            "storage": "512GB SSD",
            "ram": "16GB",
            "processor": "Intel Core i7-1360P",
            "gpu": "Intel Iris Xe",
            "battery": "Up to 12 hours",
            "os": "Windows 11"
        },
        "features": ["InfinityEdge display", "Backlit keyboard", "Thunderbolt 4", "Fingerprint reader", "Premium build"],
        "tags": ["premium", "business", "portable", "design", "professional"]
    },
    {
        "id": "laptop_003",
        "name": "Lenovo ThinkPad X1 Carbon",
        "category": "laptop",
        "brand": "Lenovo",
        "price": 1699,
        "description": "Business-focused laptop with legendary ThinkPad reliability and security",
        "specs": {
            "screen_size": "14 inches",
            "storage": "1TB SSD",
            "ram": "16GB",
            "processor": "Intel Core i7-1355U",
            "gpu": "Intel Iris Xe",
            "battery": "Up to 15 hours",
            "os": "Windows 11 Pro"
        },
        "features": ["ThinkPad keyboard", "Fingerprint reader", "IR camera", "Thunderbolt 4", "Military-grade durability"],
        "tags": ["business", "reliable", "security", "professional", "durable"]
    },
    {
        "id": "laptop_004",
        "name": "ASUS ROG Zephyrus G14",
        "category": "laptop",
        "brand": "ASUS",
        "price": 1299,
        "description": "Gaming laptop with AMD Ryzen processor and dedicated graphics for gaming and content creation",
        "specs": {
            "screen_size": "14 inches",
            "storage": "512GB SSD",
            "ram": "16GB",
            "processor": "AMD Ryzen 7 7735HS",
            "gpu": "NVIDIA RTX 4050",
            "battery": "Up to 8 hours",
            "os": "Windows 11"
        },
        "features": ["144Hz display", "RGB keyboard", "Gaming performance", "Anime Matrix", "Portable gaming"],
        "tags": ["gaming", "performance", "content creation", "portable", "RGB"]
    },
    
    # Tablets
    {
        "id": "tablet_001",
        "name": "iPad Pro 12.9-inch",
        "category": "tablet",
        "brand": "Apple",
        "price": 1099,
        "description": "Professional tablet with M2 chip, perfect for creative work and productivity",
        "specs": {
            "screen_size": "12.9 inches",
            "storage": "128GB",
            "ram": "8GB",
            "processor": "M2",
            "camera": "12MP wide + 10MP ultra-wide",
            "battery": "Up to 10 hours",
            "os": "iPadOS 17"
        },
        "features": ["Liquid Retina XDR display", "Apple Pencil support", "Magic Keyboard", "5G optional", "Face ID"],
        "tags": ["premium", "creative", "productivity", "professional", "large screen"]
    },
    {
        "id": "tablet_002",
        "name": "Samsung Galaxy Tab S9 Ultra",
        "category": "tablet",
        "brand": "Samsung",
        "price": 1199,
        "description": "Large Android tablet with S Pen and exceptional multimedia experience",
        "specs": {
            "screen_size": "14.6 inches",
            "storage": "256GB",
            "ram": "12GB",
            "processor": "Snapdragon 8 Gen 2",
            "camera": "13MP + 8MP dual",
            "battery": "11200mAh",
            "os": "Android 13"
        },
        "features": ["AMOLED display", "S Pen included", "5G optional", "Multi-window", "DeX mode"],
        "tags": ["large screen", "multimedia", "productivity", "S Pen", "entertainment"]
    },
    {
        "id": "tablet_003",
        "name": "Microsoft Surface Pro 9",
        "category": "tablet",
        "brand": "Microsoft",
        "price": 999,
        "description": "2-in-1 tablet that transforms into a laptop with full Windows experience",
        "specs": {
            "screen_size": "13 inches",
            "storage": "256GB SSD",
            "ram": "16GB",
            "processor": "Intel Core i5-1235U",
            "camera": "10MP rear + 5MP front",
            "battery": "Up to 15.5 hours",
            "os": "Windows 11"
        },
        "features": ["2-in-1 design", "Surface Pen", "Type Cover", "Kickstand", "Full Windows"],
        "tags": ["2-in-1", "productivity", "business", "versatile", "Windows"]
    },
    {
        "id": "tablet_004",
        "name": "Amazon Fire HD 10",
        "category": "tablet",
        "brand": "Amazon",
        "price": 149,
        "description": "Affordable tablet perfect for entertainment, reading, and basic tasks",
        "specs": {
            "screen_size": "10.1 inches",
            "storage": "32GB",
            "ram": "3GB",
            "processor": "Octa-core",
            "camera": "5MP rear + 2MP front",
            "battery": "Up to 12 hours",
            "os": "Fire OS"
        },
        "features": ["HD display", "Alexa integration", "Expandable storage", "Kid-friendly", "Affordable"],
        "tags": ["budget", "entertainment", "reading", "kids", "value"]
    }
]

def get_products_by_category(category=None):
    """Get products filtered by category."""
    if category:
        return [product for product in PRODUCTS if product["category"] == category]
    return PRODUCTS

def get_product_by_id(product_id):
    """Get a specific product by ID."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None

def get_products_by_price_range(min_price=0, max_price=float('inf')):
    """Get products within a price range."""
    return [product for product in PRODUCTS if min_price <= product["price"] <= max_price]

def get_products_by_brand(brand):
    """Get products by brand."""
    return [product for product in PRODUCTS if product["brand"].lower() == brand.lower()]
