"""
RAG Service - Retrieval Augmented Generation
Uses sentence-transformers for embeddings and similarity search
"""

from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from core.config import settings
from core.database import get_database
import asyncio

class RAGService:
    def __init__(self):
        self._embedding_model = None  # Lazy initialization
        self.top_k = settings.TOP_K_RESULTS
    
    @property
    def embedding_model(self):
        """Lazy load embedding model - only load when first used"""
        if self._embedding_model is None:
            print("Loading embedding model (first use)...")
            self._embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            print("Embedding model loaded.")
        return self._embedding_model
    
    def _embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a text"""
        return self.embedding_model.encode(text, convert_to_numpy=True)
    
    async def retrieve_courses(self, skill: str, role: str = None) -> List[Dict[str, Any]]:
        """Retrieve relevant courses for a skill using semantic search"""
        database = get_database()
        courses_collection = database["courses"]
        
        # Get all courses
        all_courses = await courses_collection.find({}).to_list(length=1000)
        
        if not all_courses:
            return []
        
        # Create query embedding
        query_text = f"{skill} {role}" if role else skill
        query_embedding = self._embed_text(query_text)
        
        # Calculate similarities
        similarities = []
        for course in all_courses:
            # Create course text for embedding
            course_text = f"{course.get('skill', '')} {course.get('resource_name', '')} {course.get('description', '')}"
            course_embedding = self._embed_text(course_text)
            
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, course_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(course_embedding)
            )
            
            similarities.append((similarity, course))
        
        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_courses = [course for _, course in similarities[:self.top_k]]
        
        return top_courses
    
    async def retrieve_job_samples(self, role: str) -> List[Dict[str, Any]]:
        """Retrieve similar job descriptions for a role"""
        database = get_database()
        jd_collection = database["job_descriptions"]
        
        # Get all job descriptions
        all_jds = await jd_collection.find({}).to_list(length=1000)
        
        if not all_jds:
            return []
        
        # Create query embedding
        query_embedding = self._embed_text(role)
        
        # Calculate similarities
        similarities = []
        for jd in all_jds:
            jd_text = f"{jd.get('role', '')} {jd.get('description', '')}"
            jd_embedding = self._embed_text(jd_text)
            
            similarity = np.dot(query_embedding, jd_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(jd_embedding)
            )
            
            similarities.append((similarity, jd))
        
        # Sort and return top K
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_jds = [jd for _, jd in similarities[:self.top_k]]
        
        return top_jds

# Lazy initialization - only create instance, don't load model yet
rag_service = RAGService()
