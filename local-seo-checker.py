#!/usr/bin/env python3
"""
MCP Professional SEO Checker Server

Comprehensive SEO analysis tool for checking:
- Title tags, meta descriptions, headers structure
- Image optimization and alt tags
- Page speed and technical SEO
- Content analysis and keyword density
- Social media tags (Open Graph, Twitter Cards)
- Schema markup detection
- Mobile-friendliness indicators
"""

import asyncio
import json
import logging
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seo-checker")

# Create the FastMCP server
mcp = FastMCP(
    name="Professional SEO Checker",
    instructions="When asked about SEO analysis, page optimization, meta tags, or search engine optimization, use the appropriate SEO checking tools."
)

class SEOChecker:
    """Professional SEO analysis tool"""
    
    def __init__(self):
        self.default_timeout = 20
        self.user_agent = "Mozilla/5.0 (SEO Checker MCP Server; +https://example.com/seo-bot)"
    
    async def analyze_page_seo(self, url: str) -> Dict[str, Any]:
        """Comprehensive SEO analysis of a webpage"""
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        parsed_url = urlparse(url)
        
        results = {
            "url": url,
            "domain": parsed_url.netloc,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "unknown",
            "seo_score": 0,
            "page_info": {},
            "title_analysis": {},
            "meta_analysis": {},
            "header_analysis": {},
            "content_analysis": {},
            "image_analysis": {},
            "technical_seo": {},
            "social_media": {},
            "recommendations": [],
            "critical_issues": [],
            "warnings": [],
            "errors": []
        }
        
        try:
            # Fetch page content and measure performance
            page_data = await self._fetch_page_with_timing(url)
            
            if page_data["status"]["code"] != 200:
                results["errors"].append(f"Cannot access page: {page_data['status']['code']} {page_data['status']['text']}")
                results["status"] = "error"
                return results
            
            # Parse HTML content
            soup = BeautifulSoup(page_data["content"], 'html.parser')
            
            # Perform all SEO analyses
            results["page_info"] = self._analyze_page_info(page_data, soup)
            results["title_analysis"] = self._analyze_title(soup)
            results["meta_analysis"] = self._analyze_meta_tags(soup)
            results["header_analysis"] = self._analyze_headers(soup)
            results["content_analysis"] = self._analyze_content(soup, page_data["content"])
            results["image_analysis"] = self._analyze_images(soup, url)
            results["technical_seo"] = self._analyze_technical_seo(soup, page_data)
            results["social_media"] = self._analyze_social_media_tags(soup)
            
            # Generate recommendations and calculate score
            results["recommendations"], results["critical_issues"], results["warnings"] = self._generate_recommendations(results)
            results["seo_score"] = self._calculate_seo_score(results)
            
            results["status"] = "success"
            
        except Exception as e:
            results["status"] = "error"
            results["errors"].append(str(e))
            logger.error(f"SEO analysis failed for {url} - {e}")
        
        return results
    
    async def _fetch_page_with_timing(self, url: str) -> Dict[str, Any]:
        """Fetch page with performance timing"""
        timeout = aiohttp.ClientTimeout(total=self.default_timeout)
        headers = {'User-Agent': self.user_agent}
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            try:
                async with session.get(url, allow_redirects=True) as response:
                    ttfb_time = time.time()
                    content = await response.text()
                    end_time = time.time()
                    
                    return {
                        "content": content,
                        "status": {
                            "code": response.status,
                            "text": response.reason,
                            "final_url": str(response.url)
                        },
                        "timing": {
                            "ttfb_ms": round((ttfb_time - start_time) * 1000, 2),
                            "total_ms": round((end_time - start_time) * 1000, 2),
                            "size_bytes": len(content.encode('utf-8'))
                        },
                        "headers": dict(response.headers)
                    }
            except Exception as e:
                return {
                    "content": "",
                    "status": {"code": 0, "text": str(e), "final_url": url},
                    "timing": {"ttfb_ms": 0, "total_ms": 0, "size_bytes": 0},
                    "headers": {}
                }
    
    def _analyze_page_info(self, page_data: Dict, soup: BeautifulSoup) -> Dict[str, Any]:
        """Basic page information analysis"""
        return {
            "status_code": page_data["status"]["code"],
            "final_url": page_data["status"]["final_url"],
            "load_time_ms": page_data["timing"]["total_ms"],
            "page_size_kb": round(page_data["timing"]["size_bytes"] / 1024, 2),
            "has_doctype": str(soup).startswith('<!DOCTYPE'),
            "language": soup.find('html', {'lang': True}).get('lang') if soup.find('html', {'lang': True}) else None,
            "charset": self._extract_charset(soup)
        }
    
    def _extract_charset(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract character encoding"""
        charset_tag = soup.find('meta', {'charset': True})
        if charset_tag:
            return charset_tag.get('charset')
        
        content_type = soup.find('meta', {'http-equiv': 'Content-Type'})
        if content_type and content_type.get('content'):
            content = content_type.get('content')
            match = re.search(r'charset=([^;]+)', content)
            if match:
                return match.group(1)
        
        return None
    
    def _analyze_title(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze title tag"""
        title_tag = soup.find('title')
        
        if not title_tag:
            return {
                "exists": False,
                "content": "",
                "length": 0,
                "issues": ["Missing title tag"],
                "score": 0
            }
        
        title_text = title_tag.get_text().strip()
        title_length = len(title_text)
        issues = []
        score = 100
        
        # Title length analysis
        if title_length == 0:
            issues.append("Title tag is empty")
            score -= 50
        elif title_length < 30:
            issues.append("Title is too short (< 30 characters)")
            score -= 20
        elif title_length > 60:
            issues.append("Title may be truncated in search results (> 60 characters)")
            score -= 10
        
        # Additional checks
        if title_text.count('|') > 2:
            issues.append("Too many separators in title")
            score -= 5
        
        if title_text.upper() == title_text and len(title_text) > 10:
            issues.append("Title is in ALL CAPS")
            score -= 10
        
        return {
            "exists": True,
            "content": title_text,
            "length": title_length,
            "issues": issues,
            "score": max(0, score)
        }
    
    def _analyze_meta_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta tags"""
        meta_analysis = {
            "description": self._analyze_meta_description(soup),
            "keywords": self._analyze_meta_keywords(soup),
            "robots": self._analyze_robots_meta(soup),
            "viewport": self._analyze_viewport_meta(soup),
            "canonical": self._analyze_canonical(soup)
        }
        
        return meta_analysis
    
    def _analyze_meta_description(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta description"""
        desc_tag = soup.find('meta', {'name': 'description'}) or soup.find('meta', {'property': 'description'})
        
        if not desc_tag or not desc_tag.get('content'):
            return {
                "exists": False,
                "content": "",
                "length": 0,
                "issues": ["Missing meta description"],
                "score": 0
            }
        
        desc_text = desc_tag.get('content').strip()
        desc_length = len(desc_text)
        issues = []
        score = 100
        
        if desc_length == 0:
            issues.append("Meta description is empty")
            score -= 50
        elif desc_length < 120:
            issues.append("Meta description is too short (< 120 characters)")
            score -= 15
        elif desc_length > 160:
            issues.append("Meta description may be truncated (> 160 characters)")
            score -= 10
        
        return {
            "exists": True,
            "content": desc_text,
            "length": desc_length,
            "issues": issues,
            "score": max(0, score)
        }
    
    def _analyze_meta_keywords(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta keywords (mostly obsolete but worth noting)"""
        keywords_tag = soup.find('meta', {'name': 'keywords'})
        
        if not keywords_tag:
            return {"exists": False, "note": "Meta keywords not used (good - they're obsolete)"}
        
        return {
            "exists": True,
            "content": keywords_tag.get('content', '').strip(),
            "note": "Meta keywords are obsolete and ignored by search engines"
        }
    
    def _analyze_robots_meta(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze robots meta tag"""
        robots_tag = soup.find('meta', {'name': 'robots'})
        
        if not robots_tag:
            return {"exists": False, "directives": [], "issues": []}
        
        content = robots_tag.get('content', '').lower()
        directives = [d.strip() for d in content.split(',')]
        issues = []
        
        if 'noindex' in directives:
            issues.append("Page is set to NOINDEX - won't appear in search results")
        
        if 'nofollow' in directives:
            issues.append("Page is set to NOFOLLOW - links won't be followed")
        
        return {
            "exists": True,
            "directives": directives,
            "issues": issues
        }
    
    def _analyze_viewport_meta(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze viewport meta tag for mobile optimization"""
        viewport_tag = soup.find('meta', {'name': 'viewport'})
        
        if not viewport_tag:
            return {
                "exists": False,
                "issues": ["Missing viewport meta tag - may not be mobile-friendly"]
            }
        
        content = viewport_tag.get('content', '')
        has_width = 'width=' in content
        has_initial_scale = 'initial-scale=' in content
        
        issues = []
        if not has_width:
            issues.append("Viewport should specify width")
        if not has_initial_scale:
            issues.append("Viewport should specify initial-scale")
        
        return {
            "exists": True,
            "content": content,
            "issues": issues
        }
    
    def _analyze_canonical(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze canonical link tag"""
        canonical_tag = soup.find('link', {'rel': 'canonical'})
        
        if not canonical_tag:
            return {
                "exists": False,
                "issues": ["Missing canonical URL - may cause duplicate content issues"]
            }
        
        canonical_url = canonical_tag.get('href', '')
        issues = []
        
        if not canonical_url:
            issues.append("Canonical tag exists but has no href")
        elif not canonical_url.startswith(('http://', 'https://')):
            issues.append("Canonical URL should be absolute")
        
        return {
            "exists": True,
            "url": canonical_url,
            "issues": issues
        }
    
    def _analyze_headers(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze header tag structure (H1-H6)"""
        headers = {}
        structure_issues = []
        
        for i in range(1, 7):
            header_tags = soup.find_all(f'h{i}')
            headers[f'h{i}'] = {
                "count": len(header_tags),
                "content": [tag.get_text().strip()[:100] for tag in header_tags[:5]]  # First 5, truncated
            }
        
        # H1 analysis
        h1_count = headers['h1']['count']
        if h1_count == 0:
            structure_issues.append("Missing H1 tag")
        elif h1_count > 1:
            structure_issues.append(f"Multiple H1 tags found ({h1_count}) - should have only one")
        
        # Structure analysis
        has_headers = any(headers[f'h{i}']['count'] > 0 for i in range(1, 7))
        if not has_headers:
            structure_issues.append("No header tags found")
        
        return {
            "structure": headers,
            "issues": structure_issues,
            "score": 100 - (len(structure_issues) * 15)
        }
    
    def _analyze_content(self, soup: BeautifulSoup, html_content: str) -> Dict[str, Any]:
        """Analyze page content"""
        # Extract text content
        text_content = soup.get_text()
        words = text_content.split()
        word_count = len(words)
        
        # Content analysis
        issues = []
        score = 100
        
        if word_count < 300:
            issues.append("Content is thin (< 300 words)")
            score -= 25
        elif word_count < 150:
            issues.append("Very thin content (< 150 words)")
            score -= 40
        
        # Text to HTML ratio
        html_size = len(html_content)
        text_size = len(text_content)
        text_ratio = (text_size / html_size) * 100 if html_size > 0 else 0
        
        if text_ratio < 15:
            issues.append("Low text-to-HTML ratio (< 15%)")
            score -= 15
        
        return {
            "word_count": word_count,
            "character_count": len(text_content),
            "text_to_html_ratio": round(text_ratio, 1),
            "issues": issues,
            "score": max(0, score)
        }
    
    def _analyze_images(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Analyze images for SEO optimization"""
        img_tags = soup.find_all('img')
        total_images = len(img_tags)
        
        if total_images == 0:
            return {
                "total_images": 0,
                "images_with_alt": 0,
                "images_without_alt": 0,
                "issues": ["No images found"],
                "score": 100
            }
        
        images_with_alt = 0
        images_without_alt = 0
        issues = []
        
        for img in img_tags:
            alt_text = img.get('alt')
            if alt_text is not None and alt_text.strip():
                images_with_alt += 1
            else:
                images_without_alt += 1
        
        # Calculate score
        alt_percentage = (images_with_alt / total_images) * 100
        score = alt_percentage
        
        if images_without_alt > 0:
            issues.append(f"{images_without_alt} images missing alt text")
        
        return {
            "total_images": total_images,
            "images_with_alt": images_with_alt,
            "images_without_alt": images_without_alt,
            "alt_percentage": round(alt_percentage, 1),
            "issues": issues,
            "score": round(score)
        }
    
    def _analyze_technical_seo(self, soup: BeautifulSoup, page_data: Dict) -> Dict[str, Any]:
        """Analyze technical SEO factors"""
        issues = []
        
        # Page speed analysis
        load_time = page_data["timing"]["total_ms"]
        if load_time > 3000:
            issues.append("Slow page load time (> 3 seconds)")
        elif load_time > 2000:
            issues.append("Page load time could be improved (> 2 seconds)")
        
        # HTTPS check
        is_https = page_data["status"]["final_url"].startswith('https')
        if not is_https:
            issues.append("Page is not served over HTTPS")
        
        # Check for schema markup
        schema_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        has_schema = len(schema_scripts) > 0
        
        return {
            "https": is_https,
            "load_time_ms": load_time,
            "page_size_kb": round(page_data["timing"]["size_bytes"] / 1024, 2),
            "has_schema_markup": has_schema,
            "schema_types": len(schema_scripts),
            "issues": issues
        }
    
    def _analyze_social_media_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze Open Graph and Twitter Card tags"""
        # Open Graph tags
        og_tags = {}
        og_metas = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        for tag in og_metas:
            prop = tag.get('property', '').replace('og:', '')
            og_tags[prop] = tag.get('content', '')
        
        # Twitter Card tags
        twitter_tags = {}
        twitter_metas = soup.find_all('meta', {'name': lambda x: x and x.startswith('twitter:')})
        for tag in twitter_metas:
            name = tag.get('name', '').replace('twitter:', '')
            twitter_tags[name] = tag.get('content', '')
        
        # Analysis
        og_score = 0
        twitter_score = 0
        
        essential_og = ['title', 'description', 'image', 'url']
        og_score = sum(25 for tag in essential_og if tag in og_tags and og_tags[tag])
        
        essential_twitter = ['card', 'title', 'description']
        twitter_score = sum(33 for tag in essential_twitter if tag in twitter_tags and twitter_tags[tag])
        
        return {
            "open_graph": {
                "tags": og_tags,
                "score": og_score,
                "has_essential": og_score == 100
            },
            "twitter_cards": {
                "tags": twitter_tags,
                "score": min(twitter_score, 100),
                "has_essential": twitter_score >= 100
            }
        }
    
    def _generate_recommendations(self, results: Dict) -> Tuple[List[str], List[str], List[str]]:
        """Generate SEO recommendations based on analysis"""
        recommendations = []
        critical_issues = []
        warnings = []
        
        # Title issues
        if not results["title_analysis"]["exists"]:
            critical_issues.append("Add a title tag to the page")
        elif results["title_analysis"]["length"] < 30:
            recommendations.append("Expand title tag (aim for 30-60 characters)")
        elif results["title_analysis"]["length"] > 60:
            warnings.append("Consider shortening title tag to avoid truncation")
        
        # Meta description issues
        if not results["meta_analysis"]["description"]["exists"]:
            critical_issues.append("Add a meta description tag")
        elif results["meta_analysis"]["description"]["length"] < 120:
            recommendations.append("Expand meta description (aim for 120-160 characters)")
        
        # Header issues
        if results["header_analysis"]["structure"]["h1"]["count"] == 0:
            critical_issues.append("Add an H1 tag to the page")
        elif results["header_analysis"]["structure"]["h1"]["count"] > 1:
            warnings.append("Use only one H1 tag per page")
        
        # Content issues
        if results["content_analysis"]["word_count"] < 300:
            recommendations.append("Increase content length (aim for 300+ words)")
        
        # Image issues
        if results["image_analysis"]["images_without_alt"] > 0:
            recommendations.append(f"Add alt text to {results['image_analysis']['images_without_alt']} images")
        
        # Technical issues
        tech_issues = results["technical_seo"]["issues"]
        for issue in tech_issues:
            if "HTTPS" in issue:
                critical_issues.append("Implement SSL certificate (HTTPS)")
            elif "slow" in issue.lower():
                recommendations.append("Improve page load speed")
        
        # Social media
        if not results["social_media"]["open_graph"]["has_essential"]:
            recommendations.append("Add Open Graph tags for better social media sharing")
        
        return recommendations, critical_issues, warnings
    
    def _calculate_seo_score(self, results: Dict) -> int:
        """Calculate overall SEO score"""
        scores = []
        
        # Title score (20% weight)
        scores.append(results["title_analysis"].get("score", 0) * 0.20)
        
        # Meta description score (15% weight)
        scores.append(results["meta_analysis"]["description"].get("score", 0) * 0.15)
        
        # Headers score (15% weight)
        scores.append(results["header_analysis"].get("score", 0) * 0.15)
        
        # Content score (20% weight)
        scores.append(results["content_analysis"].get("score", 0) * 0.20)
        
        # Images score (10% weight)
        scores.append(results["image_analysis"].get("score", 0) * 0.10)
        
        # Technical SEO score (20% weight)
        tech_score = 100
        if results["technical_seo"]["issues"]:
            tech_score -= len(results["technical_seo"]["issues"]) * 20
        scores.append(max(0, tech_score) * 0.20)
        
        return round(sum(scores))

# Initialize SEO checker
seo_checker = SEOChecker()

@mcp.tool()
async def analyze_seo(url: str) -> str:
    """Comprehensive SEO analysis of a webpage
    
    Args:
        url: The webpage URL to analyze (e.g., 'example.com' or 'https://example.com')
    
    Returns:
        Detailed SEO analysis and recommendations
    """
    result = await seo_checker.analyze_page_seo(url)
    
    if result["status"] == "error":
        return f"❌ SEO analysis failed for {url}\n\nErrors:\n" + "\n".join(result["errors"])
    
    # SEO Score emoji
    score = result["seo_score"]
    if score >= 90:
        score_emoji = "🏆"
        grade = "EXCELLENT"
    elif score >= 80:
        score_emoji = "🟢"
        grade = "GOOD"
    elif score >= 70:
        score_emoji = "🟡"
        grade = "FAIR"
    elif score >= 60:
        score_emoji = "🟠"
        grade = "NEEDS WORK"
    else:
        score_emoji = "🔴"
        grade = "POOR"
    
    title = result["title_analysis"]
    meta_desc = result["meta_analysis"]["description"]
    headers = result["header_analysis"]
    content = result["content_analysis"]
    images = result["image_analysis"]
    
    response = f"""{score_emoji} SEO Analysis for {result["domain"]}

🎯 OVERALL SEO SCORE: {score}/100 ({grade})

📄 TITLE TAG
• Content: "{title.get('content', 'MISSING')[:80]}{'...' if len(title.get('content', '')) > 80 else ''}"
• Length: {title.get('length', 0)} characters
• Status: {'✅ Good' if title.get('score', 0) >= 80 else '⚠️ Needs improvement'}

📝 META DESCRIPTION
• Content: "{meta_desc.get('content', 'MISSING')[:100]}{'...' if len(meta_desc.get('content', '')) > 100 else ''}"
• Length: {meta_desc.get('length', 0)} characters
• Status: {'✅ Good' if meta_desc.get('score', 0) >= 80 else '⚠️ Needs improvement'}

🏗️ HEADER STRUCTURE
• H1 Tags: {headers['structure']['h1']['count']} {'✅' if headers['structure']['h1']['count'] == 1 else '⚠️'}
• H2 Tags: {headers['structure']['h2']['count']}
• H3 Tags: {headers['structure']['h3']['count']}

📊 CONTENT ANALYSIS
• Word Count: {content['word_count']} words
• Text-to-HTML Ratio: {content['text_to_html_ratio']}%
• Status: {'✅ Good' if content['word_count'] >= 300 else '⚠️ Thin content'}

🖼️ IMAGE OPTIMIZATION
• Total Images: {images['total_images']}
• With Alt Text: {images['images_with_alt']} ({images.get('alt_percentage', 0)}%)
• Missing Alt Text: {images['images_without_alt']}

⚡ TECHNICAL SEO
• HTTPS: {'✅ Yes' if result['technical_seo']['https'] else '❌ No'}
• Load Time: {result['technical_seo']['load_time_ms']}ms
• Page Size: {result['technical_seo']['page_size_kb']} KB
• Schema Markup: {'✅ Yes' if result['technical_seo']['has_schema_markup'] else '❌ No'}
"""
    
    # Critical issues
    if result["critical_issues"]:
        response += f"\n🚨 CRITICAL ISSUES ({len(result['critical_issues'])})\n"
        for issue in result["critical_issues"]:
            response += f"• {issue}\n"
    
    # Recommendations
    if result["recommendations"]:
        response += f"\n💡 RECOMMENDATIONS ({len(result['recommendations'])})\n"
        for rec in result["recommendations"][:5]:  # Top 5 recommendations
            response += f"• {rec}\n"
        
        if len(result["recommendations"]) > 5:
            response += f"• ... and {len(result['recommendations']) - 5} more recommendations\n"
    
    return response

@mcp.tool()
async def seo_quick_check(url: str) -> str:
    """Quick SEO health check
    
    Args:
        url: The webpage URL to check
    
    Returns:
        Brief SEO status summary
    """
    result = await seo_checker.analyze_page_seo(url)
    
    if result["status"] == "error":
        return f"❌ Cannot analyze {url}: {'; '.join(result['errors'])}"
    
    score = result["seo_score"]
    domain = result["domain"]
    
    # Quick status indicators
    title_ok = result["title_analysis"].get("score", 0) >= 80
    meta_ok = result["meta_analysis"]["description"].get("score", 0) >= 80
    h1_ok = result["header_analysis"]["structure"]["h1"]["count"] == 1
    content_ok = result["content_analysis"]["word_count"] >= 300
    images_ok = result["image_analysis"]["images_without_alt"] == 0
    https_ok = result["technical_seo"]["https"]
    
    # Score emoji
    if score >= 80:
        score_emoji = "🟢"
        status = "GOOD"
    elif score >= 60:
        score_emoji = "🟡"
        status = "NEEDS WORK"
    else:
        score_emoji = "🔴"
        status = "POOR"
    
    return f"""{score_emoji} {domain} - SEO Health: {status} ({score}/100)

Quick Checks:
{'✅' if title_ok else '❌'} Title tag | {'✅' if meta_ok else '❌'} Meta description | {'✅' if h1_ok else '❌'} H1 structure
{'✅' if content_ok else '❌'} Content length | {'✅' if images_ok else '❌'} Image alt tags | {'✅' if https_ok else '❌'} HTTPS

{len(result['critical_issues'])} critical issues, {len(result['recommendations'])} recommendations"""

@mcp.tool()
async def seo_meta_tags_check(url: str) -> str:
    """Focused analysis of meta tags and social media optimization
    
    Args:
        url: The webpage URL to analyze
    
    Returns:
        Detailed meta tags and social media analysis
    """
    result = await seo_checker.analyze_page_seo(url)
    
    if result["status"] == "error":
        return f"❌ Meta tags analysis failed for {url}\n\nErrors:\n" + "\n".join(result["errors"])
    
    title = result["title_analysis"]
    meta = result["meta_analysis"]
    social = result["social_media"]
    
    response = f"""🏷️ Meta Tags & Social Media Analysis for {result["domain"]}

📄 TITLE TAG
• Content: "{title.get('content', 'MISSING')}"
• Length: {title.get('length', 0)} characters (optimal: 30-60)
• Issues: {', '.join(title.get('issues', [])) or 'None'}

📝 META DESCRIPTION
• Content: "{meta['description'].get('content', 'MISSING')}"
• Length: {meta['description'].get('length', 0)} characters (optimal: 120-160)
• Issues: {', '.join(meta['description'].get('issues', [])) or 'None'}

🔍 META ROBOTS
• Status: {'Present' if meta['robots']['exists'] else 'Not set (default: index,follow)'}
"""
    
    if meta['robots']['exists']:
        response += f"• Directives: {', '.join(meta['robots']['directives'])}\n"
        if meta['robots']['issues']:
            response += f"• Issues: {', '.join(meta['robots']['issues'])}\n"
    
    response += f"""
🔗 CANONICAL URL
• Status: {'Present' if meta['canonical']['exists'] else 'Missing'}
"""
    
    if meta['canonical']['exists']:
        response += f"• URL: {meta['canonical'].get('url', 'Empty')}\n"
        if meta['canonical']['issues']:
            response += f"• Issues: {', '.join(meta['canonical']['issues'])}\n"
    
    # Social Media Tags
    og = social['open_graph']
    twitter = social['twitter_cards']
    
    response += f"""
📱 SOCIAL MEDIA OPTIMIZATION
• Open Graph Score: {og['score']}/100
• Twitter Cards Score: {twitter['score']}/100

🌍 OPEN GRAPH TAGS ({len(og['tags'])} found)
"""
    
    essential_og = ['title', 'description', 'image', 'url']
    for tag in essential_og:
        status = "✅" if tag in og['tags'] and og['tags'][tag] else "❌"
        content = og['tags'].get(tag, 'Missing')[:60]
        response += f"• og:{tag}: {status} {content}\n"
    
    response += f"\n🐦 TWITTER CARD TAGS ({len(twitter['tags'])} found)\n"
    
    essential_twitter = ['card', 'title', 'description']
    for tag in essential_twitter:
        status = "✅" if tag in twitter['tags'] and twitter['tags'][tag] else "❌"
        content = twitter['tags'].get(tag, 'Missing')[:60]
        response += f"• twitter:{tag}: {status} {content}\n"
    
    return response

@mcp.resource("seo://analyze/{url}")
async def seo_analysis_resource(url: str) -> str:
    """Get SEO analysis data as a resource"""
    # URL decode if needed
    url = url.replace('%2F', '/').replace('%3A', ':')
    result = await seo_checker.analyze_page_seo(url)
    return json.dumps(result, indent=2, default=str)

if __name__ == "__main__":
    # Local stdio transport - works with Claude Desktop
    mcp.run()
