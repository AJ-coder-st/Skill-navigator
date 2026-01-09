"""
LLM Service - Handles all LLM interactions
Uses Google Gemini 1.5 models (flash or pro)
Modern API with proper error handling
"""

import os
import json
import re
import asyncio
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from core.config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.LLM_MODEL
        self._model = None  # Lazy initialization
        self._configured = False
        
        # Configure API if key is available
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self._configured = True
            except Exception as e:
                print(f"Warning: Failed to configure Gemini API: {str(e)}")
                self._configured = False
        else:
            print("Warning: GEMINI_API_KEY not set in .env")
    
    def _get_model(self):
        """Lazy initialization of model - only create when needed"""
        if not self._configured:
            raise ValueError("Gemini API not configured. Please set GEMINI_API_KEY in .env")
        
        if self._model is None:
            try:
                # Use modern Gemini 1.5 models
                # Default to flash (faster, cheaper) if model name contains 'pro' but API fails
                model_name = self.model_name
                
                # Normalize model name
                if model_name.startswith('models/'):
                    model_name = model_name.replace('models/', '')
                
                # Map old model names to new ones
                model_mapping = {
                    'gemini-pro': 'gemini-1.5-flash',
                    'gemini-pro-vision': 'gemini-1.5-flash',
                    'text-bison-001': 'gemini-1.5-flash',
                    'chat-bison-001': 'gemini-1.5-flash',
                }
                
                if model_name.lower() in model_mapping:
                    model_name = model_mapping[model_name.lower()]
                
                # Try to create model
                try:
                    self._model = genai.GenerativeModel(model_name)
                except Exception as e:
                    # Fallback to flash if specified model fails
                    if 'flash' not in model_name.lower():
                        print(f"Warning: Model {model_name} not available, falling back to gemini-1.5-flash")
                        self._model = genai.GenerativeModel('gemini-1.5-flash')
                    else:
                        raise e
                        
            except Exception as e:
                error_msg = str(e)
                if "API key" in error_msg.lower() or "authentication" in error_msg.lower():
                    raise ValueError("Invalid or missing Gemini API key. Please check GEMINI_API_KEY in .env")
                elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
                    raise ValueError(f"Model '{model_name}' not available. Try 'gemini-1.5-flash' or 'gemini-1.5-pro'")
                else:
                    raise ValueError(f"Failed to initialize Gemini model: {error_msg}")
        
        return self._model
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """Generate text using Gemini 1.5 - modern API with proper error handling"""
        if not self.api_key:
            raise ValueError("Gemini API key not configured. Please set GEMINI_API_KEY in .env")
        
        # Combine system prompt and user prompt
        # For Gemini, system instructions can be passed in generation_config
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            model = self._get_model()
            loop = asyncio.get_event_loop()
            
            # Modern Gemini API with generation config
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
            )
            
            # Generate content asynchronously
            def _generate():
                try:
                    response = model.generate_content(
                        full_prompt,
                        generation_config=generation_config
                    )
                    return response.text
                except Exception as e:
                    error_msg = str(e)
                    # Handle specific API errors
                    if "API key" in error_msg or "authentication" in error_msg.lower():
                        raise ValueError("Invalid Gemini API key. Please verify GEMINI_API_KEY in .env")
                    elif "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                        raise ValueError("Gemini API quota exceeded or rate limited. Please try again later.")
                    elif "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                        raise ValueError("Content was blocked by safety filters. Please modify your prompt.")
                    else:
                        raise ValueError(f"Gemini API error: {error_msg}")
            
            response_text = await loop.run_in_executor(None, _generate)
            return response_text
            
        except ValueError:
            # Re-raise ValueError as-is (these are user-friendly messages)
            raise
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error messages
            if "API key" in error_msg or "authentication" in error_msg.lower():
                raise ValueError(f"Gemini API authentication failed. Check your GEMINI_API_KEY in .env file.")
            elif "model" in error_msg.lower() and ("not found" in error_msg.lower() or "not available" in error_msg.lower()):
                raise ValueError(f"Model '{self.model_name}' not available. Available models: gemini-1.5-flash, gemini-1.5-pro")
            else:
                raise ValueError(f"LLM generation failed: {error_msg}")
    
    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate JSON response from LLM with robust parsing"""
        # Enhanced prompt for JSON generation
        json_prompt = f"""{prompt}

IMPORTANT: Respond with ONLY valid JSON. Do not include any markdown code blocks, explanations, or additional text. Return pure JSON that can be parsed directly."""
        
        try:
            response = await self.generate(json_prompt, system_prompt, temperature=0.3)
        except Exception as e:
            # If generation fails, return error in JSON format
            return {
                "error": True,
                "message": str(e),
                "reason": "LLM generation failed"
            }
        
        # Clean response (remove markdown code blocks if present)
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
            
            # If all parsing fails, return error response
            return {
                "error": True,
                "message": f"Failed to parse JSON from LLM response",
                "raw_response": cleaned_response[:500],  # First 500 chars for debugging
                "parse_error": str(e)
            }

# Only create service if Python >= 3.9
import sys
if sys.version_info >= (3, 9):
    llm_service = LLMService()
else:
    # Python 3.8 - will use HTTP service from llm_service_http
    llm_service = None
