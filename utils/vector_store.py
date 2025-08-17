"""
Vector store utilities for Pinecone integration.
Handles embedding generation, index management, and similarity search.
"""

import os
import json
from typing import List, Dict, Any
from openai import AzureOpenAI
from pinecone import Pinecone, ServerlessSpec
from data.products import PRODUCTS

class ProductVectorStore:
    def __init__(self):
        """Initialize the vector store with Pinecone and Azure OpenAI."""
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "product-recommendations")
        

        api_key=os.getenv("AZURE_EMBEDDING_API_KEY"),
        azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
        model=os.getenv("AZURE_EMBEDDING_MODEL")

        # Azure OpenAI configuration
        self.azure_openai_client = AzureOpenAI(
            api_version="2024-07-01-preview",
            api_key=os.getenv("AZURE_EMBEDDING_API_KEY"),
            azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
        )
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        # Get or create index
        self.index = self._get_or_create_index()
    
    def _get_or_create_index(self):
        """Get existing index or create a new one."""
        if self.index_name not in [index["name"] for index in self.pc.list_indexes()]:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            print(f"Created new Pinecone index: {self.index_name}")
        
        return self.pc.Index(self.index_name)
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text using Azure OpenAI."""
        try:
            response = self.azure_openai_client.embeddings.create(
                model=os.getenv("AZURE_EMBEDDING_MODEL"),
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def _create_product_text(self, product: Dict[str, Any]) -> str:
        """Create a comprehensive text representation of a product for embedding."""
        specs_text = " ".join([f"{k}: {v}" for k, v in product["specs"].items()])
        features_text = " ".join(product["features"])
        tags_text = " ".join(product["tags"])
        
        return f"""
        Product: {product['name']}
        Category: {product['category']}
        Brand: {product['brand']}
        Price: ${product['price']}
        Description: {product['description']}
        Specifications: {specs_text}
        Features: {features_text}
        Tags: {tags_text}
        """.strip()
    
    def populate_index(self):
        """Populate the Pinecone index with product embeddings."""
        print("Populating Pinecone index with product data...")
        
        vectors = []
        for product in PRODUCTS:
            # Create text representation
            product_text = self._create_product_text(product)
            
            # Generate embedding
            embedding = self._generate_embedding(product_text)
            
            if embedding:
                # Create metadata
                metadata = {
                    "id": product["id"],
                    "name": product["name"],
                    "category": product["category"],
                    "brand": product["brand"],
                    "price": product["price"],
                    "description": product["description"],
                    "specs": json.dumps(product["specs"]),
                    "features": json.dumps(product["features"]),
                    "tags": json.dumps(product["tags"])
                }
                
                vectors.append((product["id"], embedding, metadata))
        
        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
        
        print(f"Successfully populated index with {len(vectors)} products")
    
    def search_products(self, query: str, top_k: int = 5, filter_dict: Dict = None) -> List[Dict]:
        """
        Search for products based on query and optional filters.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filter_dict: Optional filters (e.g., {"category": "phone", "price": {"$lte": 1000}})
        
        Returns:
            List of product dictionaries with similarity scores
        """
        # Generate embedding for query
        query_embedding = self._generate_embedding(query)
        
        if not query_embedding:
            return []
        
        # Perform similarity search
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            # Format results
            products = []
            for match in results.matches:
                product = {
                    "id": match.metadata["id"],
                    "name": match.metadata["name"],
                    "category": match.metadata["category"],
                    "brand": match.metadata["brand"],
                    "price": match.metadata["price"],
                    "description": match.metadata["description"],
                    "specs": json.loads(match.metadata["specs"]),
                    "features": json.loads(match.metadata["features"]),
                    "tags": json.loads(match.metadata["tags"]),
                    "similarity_score": match.score
                }
                products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def search_by_category(self, category: str, query: str = "", top_k: int = 5) -> List[Dict]:
        """Search for products within a specific category."""
        filter_dict = {"category": category}
        return self.search_products(query, top_k, filter_dict)
    
    def search_by_price_range(self, min_price: float, max_price: float, query: str = "", top_k: int = 5) -> List[Dict]:
        """Search for products within a price range."""
        filter_dict = {
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        }
        return self.search_products(query, top_k, filter_dict)
    
    def search_by_brand(self, brand: str, query: str = "", top_k: int = 5) -> List[Dict]:
        """Search for products by brand."""
        filter_dict = {"brand": brand}
        return self.search_products(query, top_k, filter_dict)
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the Pinecone index."""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            print(f"Error getting index stats: {e}")
            return {}
