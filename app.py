"""
Main Streamlit application for the Product Recommendation Chatbot.
Provides a modern, user-friendly interface for product discovery.
"""

import streamlit as st
import os
from dotenv import load_dotenv
import time
from utils.chatbot import ProductRecommendationChatbot
from utils.vector_store import ProductVectorStore
from data.products import PRODUCTS, get_products_by_category

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TechStore Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e9ecef;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: right;
    }
    
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        text-align: left;
    }
    
    .product-card {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot with caching."""
    try:
        return ProductRecommendationChatbot()
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        return None

@st.cache_resource
def initialize_vector_store():
    """Initialize the vector store with caching."""
    try:
        vector_store = ProductVectorStore()
        return vector_store
    except Exception as e:
        st.error(f"Error initializing vector store: {e}")
        return None

def display_product_card(product):
    """Display a product card with formatted information."""
    with st.container():
        st.markdown(f"""
        <div class="product-card">
            <h4>{product['name']}</h4>
            <p><strong>Brand:</strong> {product['brand']} | <strong>Price:</strong> ${product['price']}</p>
            <p>{product['description']}</p>
            <p><strong>Key Features:</strong> {', '.join(product['features'][:3])}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🛍️ TechStore Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered shopping companion for phones, laptops, and tablets</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Setup & Configuration")
        
        # Check environment variables
        required_vars = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT", 
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "PINECONE_API_KEY",
            "PINECONE_ENVIRONMENT"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            st.error("⚠️ Missing environment variables:")
            for var in missing_vars:
                st.write(f"- {var}")
            st.info("Please check the env_example.txt file and set up your .env file")
            return
        
        st.success("✅ Environment variables configured")
        
        # Initialize components
        chatbot = initialize_chatbot()
        vector_store = initialize_vector_store()
        
        if not chatbot or not vector_store:
            st.error("Failed to initialize components. Please check your configuration.")
            return
        
        # Database status
        st.markdown("### 📊 Database Status")
        stats = vector_store.get_index_stats()
        if stats:
            st.write(f"**Total Products:** {stats.get('total_vector_count', 0)}")
            st.write(f"**Index Dimension:** {stats.get('dimension', 0)}")
        else:
            st.warning("Database stats not available")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Populate Database"):
            with st.spinner("Populating database with product data..."):
                vector_store.populate_index()
                st.success("Database populated successfully!")
                st.rerun()
        
        if st.button("🗑️ Clear Chat History"):
            chatbot.clear_memory()
            st.success("Chat history cleared!")
            st.rerun()
        
        # Product categories
        st.markdown("### 📱 Browse Products")
        category = st.selectbox(
            "Select Category:",
            ["All", "Phones", "Laptops", "Tablets"]
        )
        
        if category != "All":
            category_map = {"Phones": "phone", "Laptops": "laptop", "Tablets": "tablet"}
            products = get_products_by_category(category_map[category])
        else:
            products = PRODUCTS
        
        st.write(f"**{len(products)} products available**")
        
        # Show sample products
        if st.checkbox("Show sample products"):
            for product in products[:3]:
                display_product_card(product)
    
    # Main chat interface
    st.markdown("### 💬 Chat with AI Assistant")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about products, features, or recommendations..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot.chat(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # TODO: Quick suggestions
    # st.markdown("### 💡 Quick Suggestions")
    # col1, col2, col3 = st.columns(3)
    
    # TODO: Not supported yet
    # with col1:
    #     if st.button("📱 Find a phone"):
    #         st.session_state.messages.append({"role": "user", "content": "I'm looking for a new smartphone. Can you recommend some options?"})
    #         st.rerun()
    
    # with col2:
    #     if st.button("💻 Find a laptop"):
    #         st.session_state.messages.append({"role": "user", "content": "I need a laptop for work and productivity. What would you recommend?"})
    #         st.rerun()
    
    # with col3:
    #     if st.button("📱 Find a tablet"):
    #         st.session_state.messages.append({"role": "user", "content": "I want a tablet for entertainment and productivity. Any suggestions?"})
    #         st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Powered by 5AI</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
