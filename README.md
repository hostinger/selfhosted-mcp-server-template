# Remote MCP Server - Professional SEO Checker

This is a **remote MCP server** for comprehensive SEO analysis that can be deployed to Hostinger or other hosting platforms. This template demonstrates a comprehensive SEO analysis tool that performs detailed website audits including title tags, meta descriptions, header structure, content analysis, image optimization, technical SEO, and social media tags. Built with the modern FastMCP framework for reliable and professional SEO insights that you can use from any MCP-compatible client (Claude Desktop, Cursor, Windsurf, etc.) without local installation.

## Deploy this Remote MCP Server to Hostinger
[![Deploy to Hostinger](https://img.shields.io/badge/Deploy%20to-Hostinger-673AB8?style=for-the-badge&logo=hostinger)](https://www.hostinger.com/vps-hosting)

## Features

- ✅ **Comprehensive SEO Analysis**: Title tags, meta descriptions, headers structure
- 🖼️ **Image Optimization**: Alt tags checking and accessibility analysis  
- ⚡ **Technical SEO**: Page speed, HTTPS, schema markup detection
- 📊 **Content Analysis**: Word count, text-to-HTML ratio, content quality
- 📱 **Social Media Tags**: Open Graph and Twitter Cards optimization
- 🎯 **SEO Scoring**: Weighted scoring system with actionable recommendations
- 🔍 **Multiple Analysis Types**: Full analysis, quick checks, and meta tags focus
- 🚀 **Async Operations**: Non-blocking operations with proper timeout handling

## Using Your Remote MCP Server

### Option 1: Deploy Your Own Instance (1-Click)

Use Hostinger's 1-click deploy to get your own instance:

1. **Click the "Deploy to Hostinger" button** above
2. **Connect your GitHub account** and select this repository
3. **Hostinger automatically handles** the Docker setup and deployment
4. **Get your deployed URL** (e.g., `https://your-app.hstgr.cloud`)
5. **Add to your MCP client**:

```json
{
  "mcpServers": {
    "seo-checker": {
      "url": "https://your-app.hstgr.cloud/mcp",
      "description": "Professional SEO analysis and optimization recommendations"
    }
  }
}
```

### Option 2: With FastMCP Development Tools

```bash
# Make sure your virtual environment is activated
fastmcp dev local-seo-checker.py
```

### Option 3: Configure Local MCP Server

This MCP server works with Claude Desktop, Cursor, Windsurf, and other MCP-compatible applications.

#### Configuration Locations

- **Claude Desktop** (Note: Remote MCP requires newer versions):
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

- **Cursor**:
  - Settings > Tools & Integrations > MCP Tools
  - Or edit: `~/Library/Application Support/Cursor/cursor_desktop_config.json` (macOS)
  - Windows: `%APPDATA%\Cursor\cursor_desktop_config.json`

- **Windsurf**:
  - macOS: `~/Library/Application Support/Windsurf/windsurf_desktop_config.json`
  - Windows: `%APPDATA%\Windsurf\windsurf_desktop_config.json`

For local development, add the following configuration to the appropriate file:

```json
{
  "mcpServers": {
    "seo-checker": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/your/local-seo-checker.py"]
    }
  }
}
```

**Important**: 
- Replace paths with the actual paths to your virtual environment and SEO checker directory
- Use `local-seo-checker.py` for local development (simpler configuration)
- `remote-seo-checker.py` is configured for remote deployment with additional parameters

## Installation (For Local Use)

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Docker (for containerized deployment)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hostinger/selfhosted-mcp-server-template.git
   cd selfhosted-mcp-server-template
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On macOS/Linux
   source venv/bin/activate
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Deploy to Hostinger (1-Click) or Other Platforms

This MCP server can be deployed as a remote MCP server on various hosting platforms.

### Hostinger (Recommended - 1-Click Deploy)

Hostinger provides seamless 1-click deployment for this MCP server template:

1. **Click "Deploy to Hostinger"** button at the top
2. **Connect your GitHub account** if not already connected
3. **Select this repository** from your repositories
4. **Hostinger automatically**:
   - Sets up the Docker environment
   - Installs all dependencies
   - Configures the correct port (8080)
   - Provides you with a live URL
5. **Your MCP server is ready!** Use the provided URL + `/mcp`

**No manual configuration needed!** Hostinger handles all the Docker Compose setup automatically.

### Other Hosting Platforms (Manual Docker Deployment)

For other hosting platforms that support Docker:

### Prerequisites

- A hosting account (Hostinger, VPS, etc.)
- Docker support on your hosting platform
- Git repository with your code

### Deployment Steps

#### Method 1: Hostinger 1-Click Deploy (Recommended)

Simply use the deploy button at the top of this README. Hostinger handles everything automatically including:
- ✅ Docker environment setup
- ✅ Dependency installation  
- ✅ Port configuration
- ✅ SSL certificate (HTTPS)
- ✅ Automatic scaling
- ✅ Live URL provisioning

#### Method 2: Manual Docker Deployment (Other Platforms)

1. **Push your code to a Git repository**
   ```bash
   git add .
   git commit -m "Initial SEO MCP server"
   git push origin main
   ```

2. **Connect to your server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Clone and deploy**
   ```bash
   # Install Docker if not present
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
   
   # Clone your repository
   git clone https://github.com/hostinger/selfhosted-mcp-server-template.git
   cd selfhosted-mcp-server-template
   
   # Deploy with Docker Compose
   docker-compose up -d --build
   ```

4. **Configure firewall** (if needed)
   ```bash
   ufw allow 8080/tcp
   ```

5. **Test your deployment**
   ```bash
   curl http://your-server-ip:8080
   ```

#### Method 3: Traditional Hosting (Shared/VPS)

1. **Upload files to your hosting platform**
2. **Create a Procfile** (if required):
   ```
   web: python remote-seo-checker.py
   ```
3. **Set environment variables**:
   - `PORT=8080`
4. **Install dependencies and run**

### Using Your Deployed Server

Once deployed, configure your MCP client:

```json
{
  "mcpServers": {
    "seo-checker": {
      "url": "http://your-server-domain:8080/mcp",
      "description": "Professional SEO analysis and optimization recommendations"
    }
  }
}
```

### Updating Your Deployment

#### Hostinger (1-Click Updates)
Hostinger automatically detects changes when you push to your main branch and redeploys your MCP server.

#### Other Platforms (Manual Updates)
To update your deployed server:

```bash
cd /path/to/your/server
git pull origin main
docker-compose up -d --build
```

## Available Tools

### 1. `analyze_seo`
**Comprehensive SEO analysis of a webpage**

Usage: "Analyze the SEO of example.com"

Features:
- Title tag analysis (length, content, issues)
- Meta description optimization
- Header structure (H1-H6) analysis
- Content quality assessment
- Image alt text optimization
- Technical SEO factors
- Social media tags (Open Graph, Twitter Cards)
- Overall SEO scoring with recommendations

### 2. `seo_quick_check`
**Quick SEO health check**

Usage: "Do a quick SEO check on github.com"

Features:
- Rapid assessment of key SEO factors
- Quick status indicators
- Summary of critical issues
- Basic performance metrics

### 3. `seo_meta_tags_check`
**Focused analysis of meta tags and social media optimization**

Usage: "Check the meta tags for linkedin.com"

Features:
- Detailed meta tags analysis
- Open Graph tags verification
- Twitter Cards optimization
- Canonical URL analysis
- Robots meta tag inspection

## Usage Examples

### Comprehensive Analysis
"Analyze the SEO of my-website.com"

### Quick Health Check
"Do a quick SEO check on competitor.com"

### Meta Tags Focus
"Check the meta tags and social media optimization for blog-post-url.com"

### Batch Analysis
"Compare the SEO of google.com, bing.com, and duckduckgo.com"

## Understanding Results

### SEO Score Grades

- **🏆 90-100 (EXCELLENT)**: Outstanding SEO optimization
- **🟢 80-89 (GOOD)**: Well-optimized with minor improvements needed
- **🟡 70-79 (FAIR)**: Decent SEO with several optimization opportunities
- **🟠 60-69 (NEEDS WORK)**: Significant SEO issues requiring attention
- **🔴 0-59 (POOR)**: Major SEO problems that need immediate action

### Sample Output

```
🟢 SEO Analysis for example.com

🎯 OVERALL SEO SCORE: 85/100 (GOOD)

📄 TITLE TAG
• Content: "Example Domain - Official Website"
• Length: 35 characters
• Status: ✅ Good

📝 META DESCRIPTION
• Content: "This domain is for use in illustrative examples in documents..."
• Length: 145 characters
• Status: ✅ Good

🏗️ HEADER STRUCTURE
• H1 Tags: 1 ✅
• H2 Tags: 3
• H3 Tags: 2

📊 CONTENT ANALYSIS
• Word Count: 450 words
• Text-to-HTML Ratio: 25.3%
• Status: ✅ Good

🖼️ IMAGE OPTIMIZATION
• Total Images: 5
• With Alt Text: 4 (80%)
• Missing Alt Text: 1

⚡ TECHNICAL SEO
• HTTPS: ✅ Yes
• Load Time: 1250ms
• Page Size: 45.2 KB
• Schema Markup: ✅ Yes

💡 RECOMMENDATIONS (3)
• Add alt text to 1 images
• Consider adding more internal links
• Optimize images for faster loading
```

## Technical Architecture

### Core Components

- **SEOChecker Class**: Main analysis engine
- **FastMCP Framework**: Modern MCP server implementation  
- **Async HTTP Client**: Non-blocking web requests with aiohttp
- **BeautifulSoup Parser**: Robust HTML parsing and analysis
- **Multi-layered Analysis**: Comprehensive SEO factor evaluation

### Analysis Methodology

1. **Page Retrieval**: Fetch webpage with performance timing
2. **HTML Parsing**: Extract and analyze all SEO-relevant elements
3. **Multi-factor Analysis**: Evaluate 6+ key SEO categories
4. **Scoring Algorithm**: Weighted scoring based on SEO best practices
5. **Recommendation Engine**: Generate actionable improvement suggestions

### Performance Features

- ⚡ **Async Operations**: Non-blocking concurrent analysis
- 🔄 **Timeout Handling**: Graceful handling of slow websites
- 📊 **Comprehensive Metrics**: Detailed timing and performance data
- 🛡️ **Error Resilience**: Robust error handling and recovery

## Troubleshooting

### Debug Commands

```bash
# Check if server is running
curl http://your-server:8080

# View Docker logs
docker-compose logs -f seo-mcp-server

# Test locally
python remote-seo-checker.py

# Check port availability
netstat -tlnp | grep 8080
```

## Development

### Local Development

```bash
# Run in development mode
python local-seo-checker.py

# Test with MCP Inspector
npx @modelcontextprotocol/inspector
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Adding New Analysis Features

The SEO checker is designed to be easily extensible. You can add new analysis methods by:

1. Adding methods to the `SEOChecker` class
2. Integrating them into the main `analyze_page_seo` method
3. Adding corresponding MCP tools
4. Updating the scoring algorithm

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📖 **Documentation**: Check this README and code comments
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Contact**: [your-email@example.com]

---

**Disclaimer**: This tool provides SEO analysis based on current best practices and guidelines. SEO is complex and constantly evolving - always verify recommendations with current SEO guidelines and consider your specific use case.
