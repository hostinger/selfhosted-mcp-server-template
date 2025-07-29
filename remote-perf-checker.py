#!/usr/bin/env python3
"""
Remote MCP Server - Website Performance Checker

This is a remote MCP server for website performance monitoring that can be deployed 
to Hostinger or other hosting platforms. This implementation provides comprehensive
website performance checking capabilities.

DEPLOYMENT WORKFLOW:
1. Deploy this server to Hostinger using your hosting account
2. Get the deployed URL from Hostinger (e.g., https://srv563806.hstgr.cloud)
3. Use that URL + /mcp in your MCP client configuration:
   - Claude Desktop/Code
   - Cursor
   - Windsurf
   - Other MCP-compatible applications

Example MCP client configuration:
{
  "mcpServers": {
    "perf-checker": {
      "url": "https://srv563806.hstgr.cloud/mcp",
      "description": "Website performance monitoring and TTFB checking"
    }
  }
}

This remote MCP server provides tools for checking:
- Time To First Byte (TTFB)
- Response times and download speeds
- HTTP status codes and headers
- Basic website health monitoring
- Performance grading and recommendations
- Bulk website performance testing
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import aiohttp
from fastmcp import FastMCP

# Configure logging for the MCP server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("perf-checker")

# Create the FastMCP server instance
# This is the main MCP server object that will handle client connections
mcp = FastMCP(
    name="Website Performance Checker",
    instructions="When asked about website performance, TTFB, response times, or website health checks, use the appropriate performance checking tools."
)

class WebsitePerformanceChecker:
    """Website performance checker with comprehensive monitoring capabilities
    
    This class encapsulates the core performance checking logic that will be
    exposed through MCP tools. It measures various performance metrics including
    TTFB, total load time, and provides performance recommendations.
    """
    
    def __init__(self):
        # Configure reasonable timeouts to prevent hanging requests
        self.default_timeout = 30
        self.user_agent = "Mozilla/5.0 (Performance Checker MCP Server)"
    
    async def check_website_performance(self, url: str) -> Dict[str, Any]:
        """Comprehensive website performance check
        
        This is the main async method that coordinates performance checking.
        MCP tools must be async to avoid blocking the server.
        """
        # Ensure URL has protocol for proper parsing
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        parsed_url = urlparse(url)
        
        # Initialize result structure with all possible fields
        results = {
            "url": url,
            "hostname": parsed_url.hostname,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "unknown",
            "performance": {},
            "response": {},
            "errors": []
        }
        
        try:
            # Perform the performance measurement
            perf_data = await self._measure_performance(url)
            results.update(perf_data)
            results["status"] = "success"
            
        except Exception as e:
            results["status"] = "error"
            results["errors"].append(str(e))
            logger.error(f"Performance check failed for {url} - {e}")
        
        return results
    
    async def _measure_performance(self, url: str) -> Dict[str, Any]:
        """Measure website performance metrics
        
        Uses aiohttp for async HTTP requests to measure timing accurately.
        All timing measurements are done in milliseconds for consistency.
        """
        
        # Create aiohttp session with custom settings for reliability
        timeout = aiohttp.ClientTimeout(total=self.default_timeout)
        headers = {'User-Agent': self.user_agent}
        
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            # Record start time for total measurement
            start_time = time.time()
            
            try:
                # Make the HTTP request with redirect following
                async with session.get(url, allow_redirects=True) as response:
                    # Record TTFB (Time To First Byte) - when headers are received
                    ttfb_time = time.time()
                    ttfb = (ttfb_time - start_time) * 1000  # Convert to milliseconds
                    
                    # Read response body to get total time including download
                    content = await response.read()
                    end_time = time.time()
                    
                    # Calculate timing metrics
                    total_time = (end_time - start_time) * 1000
                    download_time = total_time - ttfb
                    
                    # Analyze performance and generate grade
                    performance_grade = self._grade_performance(ttfb, total_time)
                    
                    return {
                        "performance": {
                            "ttfb_ms": round(ttfb, 2),
                            "total_time_ms": round(total_time, 2),
                            "download_time_ms": round(download_time, 2),
                            "content_size_bytes": len(content),
                            "content_size_kb": round(len(content) / 1024, 2),
                            "grade": performance_grade,
                            "recommendations": self._get_recommendations(ttfb, total_time)
                        },
                        "response": {
                            "status_code": response.status,
                            "status_text": response.reason,
                            "headers": dict(response.headers),
                            "content_type": response.headers.get('content-type', 'Unknown'),
                            "server": response.headers.get('server', 'Unknown'),
                            "final_url": str(response.url),
                            "redirects": len(response.history) if hasattr(response, 'history') else 0
                        }
                    }
            
            except asyncio.TimeoutError:
                raise Exception(f"Request timed out after {self.default_timeout} seconds")
            except aiohttp.ClientError as e:
                raise Exception(f"Network error: {str(e)}")
    
    def _grade_performance(self, ttfb: float, total_time: float) -> str:
        """Grade website performance based on industry standards
        
        Performance grading based on common web performance benchmarks:
        - TTFB should be under 200ms for excellent performance
        - Total page load should be under 2 seconds for good user experience
        """
        if ttfb <= 200 and total_time <= 1000:
            return "A+"  # Excellent
        elif ttfb <= 500 and total_time <= 2000:
            return "A"   # Very Good
        elif ttfb <= 800 and total_time <= 3000:
            return "B"   # Good
        elif ttfb <= 1200 and total_time <= 5000:
            return "C"   # Average
        elif ttfb <= 2000 and total_time <= 8000:
            return "D"   # Below Average
        else:
            return "F"   # Poor
    
    def _get_recommendations(self, ttfb: float, total_time: float) -> List[str]:
        """Generate performance improvement recommendations
        
        Provides actionable advice based on measured performance metrics.
        """
        recommendations = []
        
        if ttfb > 1000:
            recommendations.append("High TTFB detected - consider server optimization or CDN")
        elif ttfb > 500:
            recommendations.append("TTFB could be improved with server-side caching")
        
        if total_time > 5000:
            recommendations.append("Page load time is slow - optimize images and resources")
        elif total_time > 3000:
            recommendations.append("Consider minifying CSS/JS and enabling compression")
        
        if not recommendations:
            recommendations.append("Performance looks good! Consider monitoring regularly")
        
        return recommendations
    
    async def check_multiple_websites(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Check performance for multiple websites concurrently
        
        This method demonstrates efficient batch processing using asyncio.gather
        for concurrent execution, which is important for MCP server performance.
        """
        if not urls:
            return []
        
        # Check all URLs concurrently for better performance
        tasks = [self.check_website_performance(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions in the results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "url": urls[i],
                    "status": "error",
                    "errors": [str(result)]
                })
            else:
                processed_results.append(result)
        
        return processed_results

# Initialize performance checker instance
# This will be used by all MCP tools
perf_checker = WebsitePerformanceChecker()

# MCP TOOLS
# Tools are functions that MCP clients can call to perform actions
# They must be decorated with @mcp.tool() and should be async

@mcp.tool()
async def check_ttfb(url: str) -> str:
    """Check Time To First Byte (TTFB) for a website
    
    This MCP tool provides detailed TTFB analysis with performance grading.
    Returns a formatted string response for easy reading by MCP clients.
    
    Args:
        url: The website URL to check (e.g., 'google.com' or 'https://google.com')
    
    Returns:
        TTFB and performance analysis
    """
    result = await perf_checker.check_website_performance(url)
    
    if result["status"] == "error":
        return f"❌ Performance check failed for {url}\n\nErrors:\n" + "\n".join(result["errors"])
    
    perf = result["performance"]
    response = result["response"]
    
    # Performance emoji based on grade
    grade_emoji = {
        "A+": "🚀", "A": "⚡", "B": "🟢", 
        "C": "🟡", "D": "🟠", "F": "🔴"
    }
    emoji = grade_emoji.get(perf["grade"], "❓")
    
    response_text = f"""{emoji} Performance Analysis for {result["hostname"]}

⏱️ TIMING METRICS
• Time To First Byte (TTFB): {perf["ttfb_ms"]}ms
• Total Load Time: {perf["total_time_ms"]}ms
• Download Time: {perf["download_time_ms"]}ms
• Performance Grade: {perf["grade"]}

📊 RESPONSE INFO
• Status: {response["status_code"]} {response["status_text"]}
• Content Size: {perf["content_size_kb"]} KB
• Content Type: {response["content_type"]}
• Server: {response["server"]}
• Redirects: {response["redirects"]}

💡 RECOMMENDATIONS
"""
    
    for rec in perf["recommendations"]:
        response_text += f"• {rec}\n"
    
    return response_text

@mcp.tool()
async def check_website_health(url: str) -> str:
    """Quick website health check
    
    This MCP tool provides a quick health status summary.
    Useful for monitoring multiple websites efficiently.
    
    Args:
        url: The website URL to check
    
    Returns:
        Basic health status and response time
    """
    result = await perf_checker.check_website_performance(url)
    
    if result["status"] == "error":
        return f"❌ {url} - Health check failed: {'; '.join(result['errors'])}"
    
    response = result["response"]
    perf = result["performance"]
    
    # Health status determination based on HTTP status codes
    if response["status_code"] == 200:
        status_emoji = "🟢"
        health_status = "HEALTHY"
    elif 200 <= response["status_code"] < 300:
        status_emoji = "🟢"
        health_status = "HEALTHY"
    elif 300 <= response["status_code"] < 400:
        status_emoji = "🟡"
        health_status = "REDIRECT"
    elif 400 <= response["status_code"] < 500:
        status_emoji = "🔴"
        health_status = "CLIENT ERROR"
    else:
        status_emoji = "🔴"
        health_status = "SERVER ERROR"
    
    return f"""{status_emoji} {result["hostname"]} - {health_status}
Status: {response["status_code"]} {response["status_text"]}
TTFB: {perf["ttfb_ms"]}ms | Total: {perf["total_time_ms"]}ms | Grade: {perf["grade"]}"""

@mcp.tool()
async def check_multiple_ttfb(urls: List[str]) -> str:
    """Check TTFB for multiple websites
    
    This MCP tool demonstrates batch processing capabilities.
    Useful for monitoring multiple websites simultaneously.
    
    Args:
        urls: List of website URLs to check
    
    Returns:
        Performance summary for all websites
    """
    if not urls:
        return "Error: Please provide at least one URL"
    
    if len(urls) > 10:
        return "Error: Maximum 10 URLs allowed"
    
    results = await perf_checker.check_multiple_websites(urls)
    
    response = f"🚀 Website Performance Results ({len(results)} sites)\n\n"
    
    for result in results:
        if result["status"] == "error":
            hostname = urlparse(result["url"]).hostname or result["url"]
            response += f"❌ {hostname} - ERROR: {'; '.join(result.get('errors', ['Unknown error']))}\n"
            continue
        
        hostname = result["hostname"]
        perf = result["performance"]
        resp = result["response"]
        
        # Status emoji for quick visual feedback
        if resp["status_code"] == 200:
            status_emoji = "🟢"
        elif 200 <= resp["status_code"] < 400:
            status_emoji = "🟡"
        else:
            status_emoji = "🔴"
        
        response += f"{status_emoji} {hostname} | TTFB: {perf['ttfb_ms']}ms | Grade: {perf['grade']} | {resp['status_code']}\n"
    
    return response

@mcp.tool()
async def performance_report(url: str) -> str:
    """Comprehensive performance report for a website
    
    This MCP tool provides detailed performance analysis including
    timing breakdown, content analysis, and optimization recommendations.
    
    Args:
        url: The website URL to analyze
    
    Returns:
        Detailed performance analysis report
    """
    result = await perf_checker.check_website_performance(url)
    
    if result["status"] == "error":
        return f"❌ Performance report failed for {url}\n\nErrors:\n" + "\n".join(result["errors"])
    
    perf = result["performance"]
    response = result["response"]
    
    report = f"""📊 Performance Report for {result["hostname"]}
Generated: {result["timestamp"]}

🎯 OVERALL PERFORMANCE GRADE: {perf["grade"]}

⏱️ TIMING BREAKDOWN
• Time To First Byte (TTFB): {perf["ttfb_ms"]}ms
• Content Download: {perf["download_time_ms"]}ms
• Total Load Time: {perf["total_time_ms"]}ms

📦 CONTENT ANALYSIS  
• Response Size: {perf["content_size_kb"]} KB ({perf["content_size_bytes"]} bytes)
• Content Type: {response["content_type"]}
• Compression: {'Yes' if 'gzip' in response["headers"].get('content-encoding', '') else 'Unknown'}

🌐 SERVER RESPONSE
• Status Code: {response["status_code"]} {response["status_text"]}
• Server Software: {response["server"]}
• Final URL: {response["final_url"]}
• Redirects: {response["redirects"]}

🔍 RESPONSE HEADERS
"""
    
    # Show important performance-related headers
    important_headers = ['cache-control', 'expires', 'last-modified', 'etag', 'content-encoding', 'x-cache']
    for header in important_headers:
        value = response["headers"].get(header, 'Not set')
        report += f"• {header.title()}: {value}\n"
    
    report += f"\n💡 PERFORMANCE RECOMMENDATIONS\n"
    for rec in perf["recommendations"]:
        report += f"• {rec}\n"
    
    # Performance benchmarks with visual indicators
    report += f"""
📈 PERFORMANCE BENCHMARKS
• TTFB < 200ms: Excellent ({'✅' if perf['ttfb_ms'] < 200 else '❌'})
• TTFB < 500ms: Good ({'✅' if perf['ttfb_ms'] < 500 else '❌'}) 
• Total < 2s: Fast ({'✅' if perf['total_time_ms'] < 2000 else '❌'})
• Total < 3s: Acceptable ({'✅' if perf['total_time_ms'] < 3000 else '❌'})
"""
    
    return report

# MCP RESOURCES
# Resources are data that can be accessed by MCP clients using URIs
# They provide a way to expose structured data through the MCP protocol

@mcp.resource("perf://check/{url}")
async def performance_resource(url: str) -> str:
    """Get website performance data as a resource
    
    This MCP resource allows clients to access performance data using a URI like:
    perf://check/example.com
    
    Resources return raw data (JSON) rather than formatted strings.
    """
    # URL decode if needed for proper processing
    url = url.replace('%2F', '/').replace('%3A', ':')
    result = await perf_checker.check_website_performance(url)
    return json.dumps(result, indent=2, default=str)

# MCP SERVER STARTUP
# This section configures and starts the MCP server for remote deployment
if __name__ == "__main__":
    import os
    
    # Get port from environment variable (used by hosting platforms like Hostinger)
    port = int(os.environ.get("PORT", 8080))
    
    # Start the MCP server with HTTP transport for remote access
    # - transport="streamable-http": Uses HTTP for communication with MCP clients
    # - host="0.0.0.0": Accepts connections from any IP (needed for remote deployment)
    # - port: The port to listen on (from environment or default 8080)
    # - log_level="debug": Enables detailed logging for development and troubleshooting
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, log_level="debug")
