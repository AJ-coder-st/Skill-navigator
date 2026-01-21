"""
Resume Analyzer Agent - Deterministic, hallucination-safe parser
Implements multi-pass cleaning, section detection, normalization, and confidence tagging.
"""

from typing import Dict, Any, List
import re


class ResumeAnalyzerAgent:
    """Deterministic resume parser with confidence tagging"""

    async def analyze(self, resume_text: str) -> Dict[str, Any]:
        cleaned = self._clean_text(resume_text)
        sections = self._detect_sections(cleaned)
        extracted = self._extract_fields(sections, cleaned)
        normalized = self._normalize(extracted)
        validated = self._validate(normalized, cleaned)
        return validated

    # Pass 1 — Raw text cleaning
    def _clean_text(self, text: str) -> str:
        lines = text.splitlines()
        deco_pattern = r"[│■●▪•◦◉◆□▫▶►▸▹▻◾◼•·●★☆✓✔✦✧❖❯➤➔➜➣➢■◆○●●○●]"
        cleaned = []
        for line in lines:
            line = re.sub(deco_pattern, " ", line)
            line = re.sub(r"\s{2,}", " ", line).strip()
            # skip page numbers and pure numbers
            if re.fullmatch(r"\d+\s*/\s*\d+|\d+", line):
                continue
            if re.search(r"page\s+\d+", line, re.IGNORECASE):
                continue
            cleaned.append(line)
        merged: List[str] = []
        for line in cleaned:
            if merged and (merged[-1].endswith(("-", "–")) or (len(merged[-1]) < 48 and not merged[-1].endswith("."))):
                merged[-1] = (merged[-1] + " " + line).strip()
            else:
                merged.append(line)
        return "\n".join(merged).strip()

    # Pass 2 — Section detection
    def _detect_sections(self, text: str) -> Dict[str, List[str]]:
        headers = {
            "education": ["education", "academic background", "qualification"],
            "experience": ["experience", "work experience", "internship", "professional experience"],
            "projects": ["projects", "academic projects", "personal projects"],
            "skills": ["skills", "technical skills", "tools & technologies", "tech stack"],
            "certifications": ["certifications", "courses", "licenses"],
        }
        sections: Dict[str, List[str]] = {k: [] for k in headers}
        current = None
        for line in text.splitlines():
            lower = line.lower()
            found = None
            for key, aliases in headers.items():
                if any(lower.startswith(a) for a in aliases):
                    found = key
                    break
            if found:
                current = found
                continue
            if current:
                sections[current].append(line)
        return sections

    # Pass 3 — Field extraction (explicit, conservative)
    def _extract_fields(self, sections: Dict[str, List[str]], full_text: str) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "location": ""
            },
            "education": [],
            "experience": [],
            "projects": [],
            "skills": {
                "technical": [],
                "tools": [],
                "soft": []
            },
            "certifications": []
        }

        # Personal info
        data["personal_info"]["email"] = self._first_match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", full_text)
        data["personal_info"]["phone"] = self._first_match(r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}", full_text)
        data["personal_info"]["name"] = self._extract_name(full_text, data["personal_info"]["email"], data["personal_info"]["phone"])

        # Education
        for line in sections.get("education", []):
            if not line.strip():
                continue
            tokens = [t.strip() for t in re.split(r"[|,-]", line) if t.strip()]
            entry = {
                "degree": tokens[0] if tokens else "",
                "field": "",
                "institution": tokens[1] if len(tokens) > 1 else "",
                "year": self._first_match(r"(20\d{2}|19\d{2})", line) or "",
                "confidence": "explicit"
            }
            data["education"].append(entry)

        # Experience
        for line in sections.get("experience", []):
            if not line.strip():
                continue
            tokens = [t.strip() for t in re.split(r"[|,-]", line) if t.strip()]
            entry = {
                "title": tokens[0] if tokens else "",
                "organization": tokens[1] if len(tokens) > 1 else "",
                "duration": self._first_match(r"(\b\d+\s*(months?|years?|yrs?)\b)", line, flags=re.IGNORECASE) or "unknown",
                "responsibilities": [],
                "confidence": "explicit"
            }
            data["experience"].append(entry)

        # Projects
        for line in sections.get("projects", []):
            if not line.strip():
                continue
            tokens = [t.strip() for t in re.split(r"[|,-]", line) if t.strip()]
            tech_tokens = re.findall(r"\b[A-Za-z\+\#\.]{2,}\b", line)
            entry = {
                "name": tokens[0] if tokens else "",
                "technologies": tech_tokens if tech_tokens else [],
                "description": tokens[1] if len(tokens) > 1 else "",
                "confidence": "explicit"
            }
            data["projects"].append(entry)

        # Certifications
        for line in sections.get("certifications", []):
            if line.strip():
                data["certifications"].append({"name": line.strip(), "confidence": "explicit"})

        # Skills (flat list, conservative)
        skills_raw = sections.get("skills", [])
        skills_set = set()
        for line in skills_raw:
            for tok in re.split(r"[;,/|]", line):
                tok = tok.strip()
                if tok:
                    skills_set.add(tok)
        data["skills"]["technical"] = sorted(skills_set)

        return data

    # Pass 4 — Normalization (safe, no hallucination)
    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        norm_map = {
            "js": "JavaScript",
            "javascript": "JavaScript",
            "fast api": "FastAPI",
            "rest api": "REST APIs",
            "restful api": "REST APIs",
        }
        stack_map = {
            "mern": ["MongoDB", "Express", "React", "Node.js"],
            "mean": ["MongoDB", "Express", "Angular", "Node.js"],
        }

        def normalize_token(tok: str) -> List[str]:
            lower = tok.lower()
            if lower in norm_map:
                return [norm_map[lower]]
            if lower in stack_map:
                return stack_map[lower]
            return [tok]

        normalized: List[str] = []
        for skill in data["skills"]["technical"]:
            normalized.extend(normalize_token(skill))

        deduped = []
        seen = set()
        for s in normalized:
            if s.lower() not in seen:
                seen.add(s.lower())
                deduped.append(s)
        data["skills"]["technical"] = deduped
        return data

    # Validation & schema enforcement + experience inference
    def _validate(self, data: Dict[str, Any], full_text: str) -> Dict[str, Any]:
        # Remove experience without organization
        data["experience"] = [e for e in data["experience"] if e.get("organization")]
        # Remove projects without technologies
        data["projects"] = [p for p in data["projects"] if p.get("technologies")]

        # Confidence tagging
        for edu in data["education"]:
            if edu.get("confidence") not in ("explicit", "contextual", "uncertain"):
                edu["confidence"] = "explicit"
        for exp in data["experience"]:
            if exp.get("confidence") not in ("explicit", "contextual", "uncertain"):
                exp["confidence"] = "explicit"
        for proj in data["projects"]:
            if proj.get("confidence") not in ("explicit", "contextual", "uncertain"):
                proj["confidence"] = "explicit"

        # Experience inference
        data["experience_years"] = self._extract_experience_years(full_text, data)

        # Enforce strict output schema
        return {
            "personal_info": {
                "name": data["personal_info"].get("name", ""),
                "email": data["personal_info"].get("email", ""),
                "phone": data["personal_info"].get("phone", ""),
                "location": data["personal_info"].get("location", "")
            },
            "education": data.get("education", []),
            "experience": data.get("experience", []),
            "projects": data.get("projects", []),
            "skills": {
                "technical": data["skills"].get("technical", []),
                "tools": data["skills"].get("tools", []),
                "soft": data["skills"].get("soft", [])
            },
            "certifications": data.get("certifications", []),
            "experience_years": data.get("experience_years", "Not Mentioned")
        }

    def _first_match(self, pattern: str, text: str, flags: int = 0) -> str:
        m = re.search(pattern, text, flags)
        return m.group(0) if m else ""

    def _extract_name(self, text: str, email: str, phone: str) -> str:
        header_block = text.split("\n")
        # Candidate lines: first 5 non-empty lines
        candidates = [l.strip() for l in header_block if l.strip()][:8]
        forbidden = {"education", "experience", "skills", "projects", "certifications", "summary"}
        # Prefer line near contact info
        contact_index = None
        for i, line in enumerate(candidates):
            if (email and email in line) or (phone and phone in line):
                contact_index = i
                break
        search_order = []
        if contact_index is not None:
            search_order.extend([contact_index - 1, contact_index - 2, contact_index + 1])
        search_order.extend(range(len(candidates)))
        seen = set()
        for idx in search_order:
            if idx < 0 or idx >= len(candidates) or idx in seen:
                continue
            seen.add(idx)
            line = candidates[idx]
            lower = line.lower()
            if lower in forbidden:
                continue
            # 2–4 words, title case, alphabetic
            words = line.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() and w.isalpha() for w in words):
                return line
        return "Not Found"

    def _extract_experience_years(self, text: str, data: Dict[str, Any]) -> str:
        lower = text.lower()
        # Detect if clearly student/fresher (education + projects, no experience entries)
        if data["experience"] == []:
            if data["projects"] or re.search(r"\b(student|fresher|graduat(e|ing))\b", lower):
                return "Fresher"
        # Look for date ranges
        date_ranges = re.findall(r"(20\d{2}|19\d{2})\s*[-–]\s*(present|20\d{2}|19\d{2})", text, re.IGNORECASE)
        total_months = 0
        for start, end in date_ranges:
            try:
                s = int(start)
                e = 2024 if str(end).lower() == "present" else int(end)
                if e >= s:
                    total_months += (e - s + 1) * 12
            except:
                continue
        # Keyword-based hints
        if total_months == 0 and re.search(r"\b(intern|internship|trainee|developer|engineer)\b", lower):
            total_months = 6  # minimal credit for internship hint
        if total_months == 0:
            return "Not Mentioned"
        years = max(0, round(total_months / 12, 1))
        if years == 0:
            return "Fresher"
        return f"{years} years"


resume_analyzer = ResumeAnalyzerAgent()
"""
Resume Analyzer Agent
Extracts structured information from resume text
"""

from typing import Dict, Any, List, Optional
import sys
if sys.version_info >= (3, 9):
    from core.llm_service import llm_service
else:
    from core.llm_service_http import llm_service

class ResumeAnalyzerAgent:
    """Analyzes resume text and extracts structured candidate profile"""
    
    SYSTEM_PROMPT = """You are an expert AI Resume Analyzer. Your task is to extract structured information from resume text.

Extract and normalize the following fields:

Personal Information:
- Full Name
- Email
- Phone (if present)
- Location (city/country if available)

Professional Summary:
- 2-3 line inferred summary if not explicitly present

Education:
- Degree
- Branch / Major
- Institution
- Graduation year (if available)

Experience:
- Job titles
- Company names
- Duration (convert to months/years)
- Responsibilities (summarize into skill-focused bullet points)

Skills:
- Technical skills
- Tools & frameworks
- Programming languages
- Soft skills (communication, teamwork, leadership)

Projects (if available):
- Project title
- Technologies used
- Problem solved
- Role of the candidate

Certifications (if available):
- Certification name
- Platform / organization

Normalize synonyms:
- Treat "JS" as "JavaScript"
- Treat "ML" as "Machine Learning"
- Treat "Fast API" as "FastAPI"
- Merge similar skills into a single canonical form

Be factual and conservative. Never assume skills not present. Only extract information that is clearly stated in the resume."""

    async def analyze(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume text and extract structured profile with fallback"""
        
        prompt = f"""Analyze the following resume text and extract structured information.

Resume Text:
{resume_text}

Return a JSON object with the following structure:
{{
    "personal_info": {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "phone number if available",
        "location": "city, country if available"
    }},
    "professional_summary": "2-3 line summary",
    "education": [
        {{
            "degree": "Degree name",
            "major": "Major/Branch",
            "institution": "Institution name",
            "graduation_year": "year if available"
        }}
    ],
    "experience": [
        {{
            "job_title": "Job title",
            "company": "Company name",
            "duration": "duration in months/years",
            "responsibilities": ["responsibility1", "responsibility2"]
        }}
    ],
    "skills": {{
        "technical_skills": ["skill1", "skill2"],
        "programming_languages": ["Python", "JavaScript"],
        "tools_frameworks": ["React", "Docker"],
        "soft_skills": ["Communication", "Leadership"]
    }},
    "projects": [
        {{
            "title": "Project title",
            "technologies": ["tech1", "tech2"],
            "description": "Brief description"
        }}
    ],
    "certifications": [
        {{
            "name": "Certification name",
            "platform": "Platform/Organization"
        }}
    ],
    "experience_years": "total years of experience",
    "reasoning": "Brief explanation of extraction decisions"
}}"""

        try:
            result = await llm_service.generate_json(prompt, self.SYSTEM_PROMPT)
            
            # Check if LLM returned an error
            if isinstance(result, dict) and result.get("error"):
                error_msg = result.get("message", "Unknown error")
                print(f"LLM returned error in resume analyzer: {error_msg}")
                if "API key" in error_msg or "authentication" in error_msg.lower():
                    return self._generate_fallback_analysis(resume_text)
                raise ValueError(error_msg)
            
            # Validate result structure
            if not isinstance(result, dict):
                raise ValueError("LLM returned invalid result format")
            
            # Ensure all required fields exist
            result.setdefault("personal_info", {})
            result.setdefault("education", [])
            result.setdefault("experience", [])
            result.setdefault("skills", {})
            result.setdefault("projects", [])
            result.setdefault("certifications", [])
            
            if "reasoning" not in result or not result.get("reasoning"):
                result["reasoning"] = "Resume analysis completed successfully. Information extracted based on resume content."
            
            print(f"Resume Analyzer: Successfully extracted profile")
            return result
        except Exception as e:
            print(f"LLM service error in resume analyzer: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self._generate_fallback_analysis(resume_text)
    
    def _generate_fallback_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Generate fallback analysis when LLM is unavailable"""
        text_lower = resume_text.lower()
        
        # Extract email
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, resume_text)
        email = emails[0] if emails else ""
        
        # Extract phone
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        phones = re.findall(phone_pattern, resume_text)
        phone = phones[0] if phones else ""
        
        # Extract name (first line usually)
        lines = resume_text.split('\n')
        name = lines[0].strip() if lines else "Not found"
        
        # Extract skills using keyword matching
        common_skills = {
            "Python", "JavaScript", "Java", "React", "Node.js", "SQL", "Git",
            "AWS", "Docker", "MongoDB", "PostgreSQL", "HTML", "CSS", "TypeScript",
            "Machine Learning", "Data Analysis", "Excel", "Tableau", "REST APIs"
        }
        
        found_skills = [skill for skill in common_skills if skill.lower() in text_lower]
        
        # Estimate experience years
        experience_years = "0"
        if any(word in text_lower for word in ["years", "yr", "experience"]):
            # Try to find number patterns
            year_pattern = r'(\d+)\s*(?:years?|yrs?)'
            year_matches = re.findall(year_pattern, text_lower)
            if year_matches:
                try:
                    max_years = max([int(y) for y in year_matches])
                    experience_years = str(max_years)
                except:
                    pass
        
        reasoning = f"""This analysis was generated using basic pattern matching (AI service temporarily unavailable).

Extracted Information:
- Name: {name}
- Email: {email if email else 'Not found'}
- Phone: {phone if phone else 'Not found'}
- Skills detected: {len(found_skills)} technical skills
- Estimated experience: {experience_years} years

For a more detailed analysis with better extraction, normalization, and structured information, please ensure the AI service is properly configured with a valid API key."""

        return {
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone,
                "location": ""
            },
            "professional_summary": "Professional summary extraction unavailable. Please review resume manually.",
            "education": [],
            "experience": [],
            "skills": {
                "technical_skills": found_skills,
                "programming_languages": [s for s in found_skills if s in ["Python", "JavaScript", "Java", "TypeScript"]],
                "tools_frameworks": [s for s in found_skills if s not in ["Python", "JavaScript", "Java", "TypeScript", "SQL"]],
                "soft_skills": []
            },
            "projects": [],
            "certifications": [],
            "experience_years": experience_years,
            "reasoning": reasoning,
            "fallback": True
        }

resume_analyzer = ResumeAnalyzerAgent()
