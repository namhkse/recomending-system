"""
Demo script for the Product Recommendation Chatbot.
This script demonstrates the system functionality without requiring external API keys.
"""

import json
from data.products import PRODUCTS, get_products_by_category, get_products_by_price_range

def simple_search(query, products):
    """Simple keyword-based search for demo purposes."""
    query_lower = query.lower()
    results = []
    
    for product in products:
        # Check if query matches product name, description, or features
        if (query_lower in product['name'].lower() or
            query_lower in product['description'].lower() or
            any(query_lower in feature.lower() for feature in product['features']) or
            any(query_lower in tag.lower() for tag in product['tags'])):
            results.append(product)
    
    return results

def format_product_display(product):
    """Format a product for display."""
    return f"""
📱 {product['name']} (${product['price']})
   Brand: {product['brand']}
   Description: {product['description']}
   Key Features: {', '.join(product['features'][:3])}
   Category: {product['category'].title()}
"""

def demo_chat():
    """Interactive demo chat interface."""
    print("🛍️ Welcome to TechStore Assistant Demo!")
    print("=" * 50)
    print("This is a demo version that shows how the system works.")
    print("You can ask about phones, laptops, and tablets.")
    print("Type 'quit' to exit, 'help' for examples.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Thanks for trying the demo! Goodbye!")
            break
        
        if user_input.lower() == 'help':
            print("\n💡 Example queries:")
            print("- 'I need a phone for photography'")
            print("- 'Show me laptops under $1500'")
            print("- 'What tablets do you have?'")
            print("- 'Apple products'")
            print("- 'gaming laptop'")
            print("- 'budget options'")
            print()
            continue
        
        if not user_input:
            continue
        
        # Simple intent detection
        query_lower = user_input.lower()
        
        # Category detection
        category = None
        if any(word in query_lower for word in ['phone', 'smartphone', 'iphone', 'android']):
            category = 'phone'
        elif any(word in query_lower for word in ['laptop', 'computer', 'macbook', 'notebook']):
            category = 'laptop'
        elif any(word in query_lower for word in ['tablet', 'ipad']):
            category = 'tablet'
        
        # Brand detection
        brand = None
        if 'apple' in query_lower:
            brand = 'Apple'
        elif 'samsung' in query_lower:
            brand = 'Samsung'
        elif 'google' in query_lower:
            brand = 'Google'
        elif 'oneplus' in query_lower:
            brand = 'OnePlus'
        elif 'dell' in query_lower:
            brand = 'Dell'
        elif 'lenovo' in query_lower:
            brand = 'Lenovo'
        elif 'asus' in query_lower:
            brand = 'ASUS'
        elif 'microsoft' in query_lower:
            brand = 'Microsoft'
        elif 'amazon' in query_lower:
            brand = 'Amazon'
        
        # Price detection (simple)
        price_filter = None
        if 'under' in query_lower and '$' in query_lower:
            # Extract price after "under"
            try:
                price_text = query_lower.split('under')[-1].strip()
                price = int(''.join(filter(str.isdigit, price_text)))
                price_filter = (0, price)
            except:
                pass
        
        # Search logic
        results = []
        
        if category:
            category_products = get_products_by_category(category)
            results = simple_search(user_input, category_products)
        elif brand:
            brand_products = [p for p in PRODUCTS if p['brand'].lower() == brand.lower()]
            results = simple_search(user_input, brand_products)
        elif price_filter:
            price_products = get_products_by_price_range(price_filter[0], price_filter[1])
            results = simple_search(user_input, price_products)
        else:
            results = simple_search(user_input, PRODUCTS)
        
        # Generate response
        if results:
            print(f"\n🤖 Assistant: I found {len(results)} product(s) that match your request:")
            for product in results[:3]:  # Show top 3
                print(format_product_display(product))
            
            if len(results) > 3:
                print(f"... and {len(results) - 3} more options available.")
            
            print("\nWould you like me to provide more details about any of these products?")
        else:
            print("\n🤖 Assistant: I couldn't find any products matching your request.")
            print("Try being more specific, for example:")
            print("- 'I need a phone for photography'")
            print("- 'Show me laptops under $1500'")
            print("- 'What tablets do you have?'")
        
        print()

def show_product_catalog():
    """Display the full product catalog."""
    print("📋 Full Product Catalog")
    print("=" * 50)
    
    categories = ['phone', 'laptop', 'tablet']
    category_names = {'phone': '📱 Smartphones', 'laptop': '💻 Laptops', 'tablet': '📱 Tablets'}
    
    for category in categories:
        products = get_products_by_category(category)
        print(f"\n{category_names[category]} ({len(products)} products):")
        print("-" * 30)
        
        for product in products:
            print(f"• {product['name']} - ${product['price']} ({product['brand']})")

def main():
    """Main demo function."""
    print("🛍️ TechStore Assistant - Demo Mode")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Start chat demo")
        print("2. View product catalog")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            demo_chat()
        elif choice == '2':
            show_product_catalog()
        elif choice == '3':
            print("👋 Thanks for trying the demo!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
