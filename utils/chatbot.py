"""
Chatbot module using Langchain and Azure OpenAI for product recommendations.
Handles conversation flow and generates contextual responses.
"""

import os
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from utils.vector_store import ProductVectorStore

class ProductRecommendationChatbot:
    def __init__(self):
        """Initialize the chatbot with Azure OpenAI and vector store."""
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7
        )
        
        self.vector_store = ProductVectorStore()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # System prompt for the chatbot
        self.system_prompt = """You are a helpful product recommendation assistant for an electronics store. 
        You help customers find the perfect phone, laptop, or tablet based on their needs and preferences.
        
        Your capabilities:
        - Understand customer requirements and preferences
        - Search through product catalog using semantic similarity
        - Provide detailed product recommendations with explanations
        - Answer questions about product specifications and features
        - Help with price comparisons and budget considerations
        
        Available product categories:
        - Phones: Smartphones from Apple, Samsung, Google, OnePlus
        - Laptops: MacBooks, Windows laptops, gaming laptops, business laptops
        - Tablets: iPads, Android tablets, 2-in-1 devices
        
        Always be helpful, friendly, and provide specific recommendations with reasoning.
        If you don't have enough information, ask clarifying questions.
        """
        
        # Create the conversation chain
        self.conversation_chain = self._create_conversation_chain()
    
    def _create_conversation_chain(self):
        """Create the Langchain conversation chain."""
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
            ("ai", "{output}")
        ])
        
        return LLMChain(
            llm=self.llm,
            prompt=prompt_template,
            memory=self.memory,
            verbose=False
        )
    
    def _extract_search_intent(self, user_message: str) -> Dict[str, Any]:
        """Extract search intent and filters from user message."""
        intent_prompt = f"""
        Analyze the following user message and extract search intent:
        
        User message: "{user_message}"
        
        Extract the following information:
        1. Product category (phone/laptop/tablet or None if not specified)
        2. Price range (min_price, max_price or None if not specified)
        3. Brand preference (specific brand or None if not specified)
        4. Key features or requirements (list of important features)
        5. Search query (the main search terms)
        
        Return as JSON format:
        {{
            "category": "phone/laptop/tablet/None",
            "min_price": null,
            "max_price": null,
            "brand": "brand_name/None",
            "features": ["feature1", "feature2"],
            "search_query": "main search terms"
        }}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=intent_prompt)])
            # Parse the response to extract JSON (simplified for demo)
            # In production, you'd want more robust JSON parsing
            return self._parse_intent_response(response.content)
        except Exception as e:
            print(f"Error extracting intent: {e}")
            return {
                "category": None,
                "min_price": None,
                "max_price": None,
                "brand": None,
                "features": [],
                "search_query": user_message
            }
    
    def _parse_intent_response(self, response: str) -> Dict[str, Any]:
        """Parse the intent extraction response."""
        # Simplified parsing - in production, use proper JSON parsing
        try:
            # Look for JSON-like structure in the response
            if "{" in response and "}" in response:
                # Extract the JSON part
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                
                # Simple parsing for demo purposes
                import json
                return json.loads(json_str)
        except:
            pass
        
        # Fallback parsing
        category = None
        if any(word in response.lower() for word in ["phone", "smartphone", "iphone", "android"]):
            category = "phone"
        elif any(word in response.lower() for word in ["laptop", "computer", "macbook", "notebook"]):
            category = "laptop"
        elif any(word in response.lower() for word in ["tablet", "ipad", "android tablet"]):
            category = "tablet"
        
        return {
            "category": category,
            "min_price": None,
            "max_price": None,
            "brand": None,
            "features": [],
            "search_query": response
        }
    
    def _format_product_recommendations(self, products: List[Dict]) -> str:
        """Format product recommendations into a readable response."""
        if not products:
            return "I couldn't find any products matching your requirements. Could you please provide more details about what you're looking for?"
        
        response = "Here are some great options for you:\n\n"
        
        for i, product in enumerate(products[:3], 1):  # Show top 3
            response += f"**{i}. {product['name']}** (${product['price']})\n"
            response += f"   Brand: {product['brand']}\n"
            response += f"   Description: {product['description']}\n"
            
            # Add key specs
            specs = product['specs']
            if 'screen_size' in specs:
                response += f"   Screen: {specs['screen_size']}\n"
            if 'storage' in specs:
                response += f"   Storage: {specs['storage']}\n"
            if 'processor' in specs:
                response += f"   Processor: {specs['processor']}\n"
            
            # Add key features
            if product['features']:
                response += f"   Key Features: {', '.join(product['features'][:3])}\n"
            
            response += f"   Match Score: {product.get('similarity_score', 0):.2f}\n\n"
        
        if len(products) > 3:
            response += f"... and {len(products) - 3} more options available.\n\n"
        
        response += "Would you like me to provide more details about any of these products or help you narrow down your search?"
        
        return response
    
    def _generate_contextual_response(self, user_message: str, products: List[Dict]) -> str:
        """Generate a contextual response using the LLM."""
        if not products:
            return "I couldn't find any products matching your requirements. Could you please provide more details about what you're looking for?"
        
        # Create context from found products
        product_context = ""
        for product in products[:3]:
            product_context += f"- {product['name']}: {product['description']}\n"
        
        response_prompt = f"""
        User is looking for products and you found these options:
        
        {product_context}
        
        User message: "{user_message}"
        
        Provide a helpful, conversational response that:
        1. Acknowledges their request
        2. Presents the recommendations naturally
        3. Asks follow-up questions to help them decide
        4. Mentions key benefits of the recommended products
        
        Be friendly and helpful, as if you're a knowledgeable sales assistant.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=response_prompt)])
            return response.content
        except Exception as e:
            print(f"Error generating contextual response: {e}")
            return self._format_product_recommendations(products)
    
    def chat(self, user_message: str) -> str:
        """
        Main chat method that processes user input and returns a response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The chatbot's response
        """
        try:
            # Extract search intent
            intent = self._extract_search_intent(user_message)
            
            # Search for products based on intent
            products = []
            if intent["category"]:
                products = self.vector_store.search_by_category(
                    intent["category"], 
                    intent["search_query"]
                )
            elif intent["brand"]:
                products = self.vector_store.search_by_brand(
                    intent["brand"], 
                    intent["search_query"]
                )
            elif intent["min_price"] is not None and intent["max_price"] is not None:
                products = self.vector_store.search_by_price_range(
                    intent["min_price"], 
                    intent["max_price"], 
                    intent["search_query"]
                )
            else:
                # General search
                products = self.vector_store.search_products(intent["search_query"])
            
            # Generate response
            if products:
                response = self._generate_contextual_response(user_message, products)
            else:
                response = "I couldn't find any products matching your requirements. Could you please provide more details about what you're looking for? For example:\n- What type of device (phone, laptop, tablet)?\n- What's your budget range?\n- Any specific features you need?\n- Preferred brand?"
            
            return response
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again or rephrase your question."
    
    def get_chat_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.memory.chat_memory.messages
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
