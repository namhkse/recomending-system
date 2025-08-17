# 🛍️ TechStore Assistant - AI Product Recommendation Chatbot

A sophisticated AI-powered chatbot that helps customers find the perfect phones, laptops, and tablets using natural language processing, vector search, and intelligent recommendations.

## ✨ Features

- **🤖 AI-Powered Conversations**: Natural language understanding using Azure OpenAI
- **🔍 Semantic Product Search**: Vector-based similarity search with Pinecone
- **📱 Multi-Category Support**: Phones, laptops, and tablets with detailed specifications
- **💬 Conversational Interface**: Modern Streamlit chat interface with conversation memory
- **🎯 Intelligent Recommendations**: Context-aware product suggestions based on user preferences
- **📊 Real-time Database**: Live product catalog with embedding-based search
- **🎨 Beautiful UI**: Modern, responsive design with intuitive navigation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Langchain     │    │   Azure OpenAI  │
│   Frontend      │◄──►│   Orchestration │◄──►│   LLM & Embed   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Product Data  │    │   Vector Store  │    │   Conversation  │
│   Management    │    │   (Pinecone)    │    │   Memory        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure OpenAI account with API access
- Pinecone account with API key
- Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd recomending_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Copy `env_example.txt` to `.env` and fill in your API keys:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` with your credentials:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2023-12-01-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

   # Pinecone Configuration
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment
   PINECONE_INDEX_NAME=product-recommendations
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Initialize the database**
   - Open the application in your browser
   - Go to the sidebar and click "🔄 Populate Database"
   - Wait for the confirmation message

## 📱 Product Catalog

The system includes a comprehensive catalog of 12 products across three categories:

### 📱 Smartphones
- **iPhone 15 Pro** - Premium Apple flagship with A17 Pro chip
- **Samsung Galaxy S24 Ultra** - Android flagship with S Pen
- **Google Pixel 8** - AI-powered camera phone
- **OnePlus 12** - Performance-focused Android device

### 💻 Laptops
- **MacBook Pro 14-inch** - Professional Apple laptop with M3 Pro
- **Dell XPS 13 Plus** - Premium Windows ultrabook
- **Lenovo ThinkPad X1 Carbon** - Business-focused laptop
- **ASUS ROG Zephyrus G14** - Gaming laptop with AMD Ryzen

### 📱 Tablets
- **iPad Pro 12.9-inch** - Professional tablet with M2 chip
- **Samsung Galaxy Tab S9 Ultra** - Large Android tablet
- **Microsoft Surface Pro 9** - 2-in-1 Windows tablet
- **Amazon Fire HD 10** - Budget entertainment tablet

## 🎯 Usage Examples

### Basic Queries
- "I need a new phone for photography"
- "Show me laptops under $1500"
- "What's the best tablet for drawing?"

### Advanced Queries
- "I want a gaming laptop with good battery life"
- "Find me an iPhone alternative with similar features"
- "Recommend a tablet for business use"

### Filtered Searches
- "Apple laptops for video editing"
- "Android phones with wireless charging"
- "Budget tablets under $200"

## 🛠️ Technical Details

### Core Components

1. **Product Vector Store** (`utils/vector_store.py`)
   - Manages Pinecone vector database
   - Handles embedding generation and similarity search
   - Supports filtering by category, price, and brand

2. **Chatbot Engine** (`utils/chatbot.py`)
   - Langchain-based conversation management
   - Intent extraction and contextual responses
   - Conversation memory and history

3. **Product Catalog** (`data/products.py`)
   - Comprehensive product database
   - Detailed specifications and features
   - Category and brand organization

4. **Streamlit Interface** (`app.py`)
   - Modern, responsive web interface
   - Real-time chat functionality
   - Product browsing and management

### Key Technologies

- **Streamlit**: Web application framework
- **Azure OpenAI**: Language model and embeddings
- **Pinecone**: Vector database for similarity search
- **Langchain**: Conversation orchestration
- **Python-dotenv**: Environment variable management

## 🔧 Configuration

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in the Azure portal
2. Deploy a GPT model (e.g., gpt-35-turbo)
3. Deploy an embedding model (text-embedding-ada-002)
4. Get your API key and endpoint URL

### Pinecone Setup

1. Create a Pinecone account
2. Create a new index with dimension 1536
3. Get your API key and environment name
4. Configure the index name in your environment variables

## 📊 Performance

- **Response Time**: < 3 seconds for typical queries
- **Search Accuracy**: High relevance through semantic similarity
- **Scalability**: Supports thousands of products
- **Memory Usage**: Efficient conversation management

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. Set up environment variables on your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`
4. Configure reverse proxy if needed

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the environment variables are correctly set
2. Ensure all dependencies are installed
3. Verify your Azure OpenAI and Pinecone accounts are active
4. Check the console for error messages

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Product image integration
- [ ] Advanced filtering options
- [ ] User preference learning
- [ ] Integration with e-commerce platforms
- [ ] Voice interface support
- [ ] Mobile app version

---

**Built with ❤️ using Streamlit, Azure OpenAI, Pinecone, and Langchain**
