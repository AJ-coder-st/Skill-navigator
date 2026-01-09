"""
HTTP-based LLM Service - Production Ready
Works with Python 3.8+
Dynamically discovers available Gemini models
Graceful error handling with fallbacks
"""

import os
import json
import re
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from core.config import settings

class LLMServiceHTTP:
    """HTTP-based Gemini API client with dynamic model discovery"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.LLM_MODEL
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self._available_models = None
        self._selected_model = None
        
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not set in .env")
            print(f"Debug: Tried to load from {os.path.abspath('.env')}")
            print(f"Debug: Current working directory: {os.getcwd()}")
        else:
            print(f"Info: GEMINI_API_KEY loaded successfully (length: {len(self.api_key)})")
    
    async def _discover_models(self) -> List[str]:
        """Dynamically discover available Gemini models"""
        if self._available_models is not None:
            return self._available_models
        
        if not self.api_key:
            raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY in .env")
        
        try:
            url = f"{self.base_url}/models"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    url,
                    params={"key": self.api_key}
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract models that support generateContent
                available = []
                if "models" in result:
                    for model in result["models"]:
                        model_name = model.get("name", "")
                        # Check if model supports generateContent
                        supported_methods = model.get("supportedGenerationMethods", [])
                        if "generateContent" in supported_methods:
                            # Remove 'models/' prefix if present
                            clean_name = model_name.replace("models/", "")
                            available.append(clean_name)
                
                self._available_models = available
                return available
                
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_json = e.response.json()
                error_detail = error_json.get("error", {}).get("message", str(e))
            except:
                error_detail = str(e)
            
            if "API key" in error_detail or "authentication" in error_detail.lower():
                raise ValueError("Invalid or missing Gemini API key. Please check GEMINI_API_KEY in .env")
            else:
                raise ValueError(f"Failed to discover models: {error_detail}")
        except Exception as e:
            raise ValueError(f"Model discovery failed: {str(e)}")
    
    async def _select_model(self) -> str:
        """Select the best available model"""
        if self._selected_model:
            return self._selected_model
        
        # Discover available models
        available = await self._discover_models()
        
        if not available:
            raise ValueError("No Gemini models available. Check your API key and quota.")
        
        # Priority order: prefer flash (faster), then pro (more capable)
        preferred_models = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro",
            "gemini-1.5-pro-latest",
            "gemini-pro",
            "gemini-pro-vision",
        ]
        
        # Try preferred models first
        for preferred in preferred_models:
            if preferred in available:
                self._selected_model = preferred
                print(f"Selected Gemini model: {preferred}")
                return preferred
        
        # Fallback to first available model
        self._selected_model = available[0]
        print(f"Selected Gemini model: {available[0]} (fallback)")
        return available[0]
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """Generate text using Gemini API via HTTP with dynamic model selection"""
        if not self.api_key:
            raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY in .env")
        
        # Select model dynamically
        model_name = await self._select_model()
        
        # Combine prompts
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Prepare request - use model name without 'models/' prefix in URL
        url = f"{self.base_url}/models/{model_name}:generateContent"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params={"key": self.api_key},
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract text from response
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            return parts[0]["text"]
                
                # Check for safety filters
                if "promptFeedback" in result:
                    feedback = result["promptFeedback"]
                    if feedback.get("blockReason"):
                        raise ValueError(f"Content blocked by safety filters: {feedback.get('blockReason')}")
                
                # Fallback: try to extract any text
                raise ValueError(f"Unexpected API response format: {json.dumps(result)[:200]}")
                
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_json = e.response.json()
                error_detail = error_json.get("error", {}).get("message", str(e))
            except:
                error_detail = str(e)
            
            # Handle specific errors
            if "API key" in error_detail or "authentication" in error_detail.lower() or "401" in str(e.response.status_code):
                raise ValueError("Invalid or missing Gemini API key. Please check GEMINI_API_KEY in .env")
            elif "quota" in error_detail.lower() or "rate limit" in error_detail.lower() or "429" in str(e.response.status_code):
                raise ValueError("Gemini API quota exceeded or rate limited. Please try again later.")
            elif "safety" in error_detail.lower() or "blocked" in error_detail.lower():
                raise ValueError("Content was blocked by safety filters. Please modify your prompt.")
            elif "not found" in error_detail.lower() or "404" in str(e.response.status_code):
                # Model not found - try to reselect
                self._selected_model = None
                raise ValueError(f"Model '{model_name}' not available. Attempting to discover available models...")
            else:
                raise ValueError(f"Gemini API error: {error_detail}")
        except httpx.RequestError as e:
            raise ValueError(f"Network error connecting to Gemini API: {str(e)}")
        except ValueError:
            # Re-raise ValueError as-is (these are user-friendly messages)
            raise
        except Exception as e:
            raise ValueError(f"LLM generation failed: {str(e)}")
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate JSON response from LLM with robust error handling"""
        json_prompt = f"""{prompt}

IMPORTANT: Respond with ONLY valid JSON. Do not include any markdown code blocks, explanations, or additional text. Return pure JSON that can be parsed directly.

Make sure to include all requested fields, especially the "reasoning" field with a detailed explanation."""
        
        try:
            response = await self.generate(json_prompt, system_prompt, temperature=0.3)
        except Exception as e:
            # Return error in JSON format instead of raising
            print(f"LLM generate_json error: {str(e)}")
            return {
                "error": True,
                "message": str(e),
                "reason": "LLM generation failed"
            }
        
        # Clean response
        cleaned_response = response.strip()
        
        # Remove markdown code blocks
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        cleaned_response = cleaned_response.strip()
        
        # Try to parse JSON
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            # Fallback: try to extract JSON from response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned_response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            return {
                "error": True,
                "message": f"Failed to parse JSON from LLM response",
                "raw_response": cleaned_response[:500],
                "parse_error": str(e)
            }

# Auto-select service based on Python version
# Only print message when actually used, not at import time
import sys

def _get_llm_service():
    """Get appropriate LLM service based on Python version"""
    if sys.version_info < (3, 9):
        # Python 3.8 - use HTTP service
        service = LLMServiceHTTP()
        print("Using HTTP-based LLM service (Python 3.8 compatibility mode)")
        return service
    else:
        # Python 3.9+ - use package-based service
        try:
            from core.llm_service import LLMService
            service = LLMService()
            print("Using package-based LLM service (Python 3.9+)")
            return service
        except Exception as e:
            # Fallback to HTTP if package service fails
            service = LLMServiceHTTP()
            print(f"Fell back to HTTP-based LLM service: {str(e)}")
            return service

# Create service instance (but don't print during import)
llm_service = _get_llm_service()
