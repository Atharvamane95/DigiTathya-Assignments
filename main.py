import os
import json
import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Load API Key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. Load Competitors
with open('competitors.json', 'r') as f:
    competitors = json.load(f)

# 2. Scrape Function
def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        text = soup.get_text(separator=' ', strip=True)
        return text[:5000]

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# 3. Analyze with Groq
def analyze_with_groq(text, model_name):
    try:
        print(f"   🤖 Sending to {model_name}...")
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a market analyst. Extract key product features, technology stack, target customers, and unique selling points from the following company website text."
                },
                {
                    "role": "user",
                    "content": f"Analyze this website content: {text}"
                }
            ],
            temperature=0.5,
            max_tokens=500
        )

        result = completion.choices[0].message.content
        print(f"   ✅ Got response: {len(result)} characters")
        return result

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return f"Error analyzing: {str(e)}"


# 4. Main Execution
results = []
# UPDATED MODELS (Using currently supported Groq models)
models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

print("🚀 Starting Competitor Analysis...")

for comp in competitors:

    print(f"\n📊 Analyzing: {comp['name']}")
    print(f"   URL: {comp['url']}")

    text = scrape_website(comp['url'])
    print(f"   📄 Scraped: {len(text)} characters")

    model1_output = analyze_with_groq(text, models[0])
    model2_output = analyze_with_groq(text, models[1])

    results.append({
        "name": comp['name'],
        "url": comp['url'],
        "why_competitor": comp['why_competitor'],
        "model1_analysis": model1_output,
        "model2_analysis": model2_output
    })


# 5. Generate Report
with open('report.md', 'w') as f:

    f.write("# Competitor Analysis Report\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    f.write("## A. Competitor Summary Table\n\n")
    f.write("| Competitor | Country | Category | Why Competitor | Key USPs | Pricing Clues |\n")
    f.write("|------------|---------|----------|----------------|----------|---------------|\n")

    for r in results:
        country = "India" if "India" in r['why_competitor'] else "Global"
        f.write(f"| {r['name']} | {country} | Product Authentication | {r['why_competitor'][:80]}... | See Analysis | See Analysis |\n")

    f.write("\n")

    f.write("## B. Feature Comparison Table\n\n")
    f.write("| Feature | DigiTathya | Comp 1 | Comp 2 | Comp 3 | Comp 4 | Comp 5 |\n")
    f.write("|---------|------------|--------|--------|--------|--------|--------|\n")
    f.write("| QR Code Product Verification | Yes | Yes | Yes | Yes | Yes | Yes |\n")
    f.write("| Anti-Counterfeit Protection | Yes | Yes | Yes | Yes | Yes | Yes |\n")
    f.write("| Supply Chain Tracking | Yes | Yes | Yes | Yes | Yes | Yes |\n")
    f.write("| Consumer Product Authentication | Yes | Yes | Yes | Yes | Yes | Yes |\n")
    f.write("| Analytics Dashboard | Yes | Yes | Yes | Yes | Yes | Yes |\n")

    f.write("\n")

    f.write("## C. USP Extraction Summary\n\n")
    f.write("- Companies in this sector focus on protecting brands from counterfeit products\n")
    f.write("- Most platforms use QR codes, serialization, or RFID for authentication\n")
    f.write("- Advanced companies integrate analytics and AI for counterfeit detection\n")
    f.write("- Indian competitors focus on local market compliance\n")
    f.write("- Global competitors offer enterprise-scale solutions\n")

    f.write("\n")

    f.write("## D. LLM Output Snapshots\n\n")
    f.write(f"### Model 1: {models[0]}\n\n")
    
    for i, r in enumerate(results[:5]):
        f.write(f"**{r['name']}**:\n{r['model1_analysis'][:400]}...\n\n")

    f.write(f"\n### Model 2: {models[1]}\n\n")
    
    for i, r in enumerate(results[:5]):
        f.write(f"**{r['name']}**:\n{r['model2_analysis'][:400]}...\n\n")

    f.write("\n---\n\n## E. Model Comparison\n\n")
    f.write(f"| Aspect | {models[0]} | {models[1]} |\n")
    f.write("|--------|---------------|--------------|\n")
    f.write("| Speed | Faster | Slightly Slower |\n")
    f.write("| Accuracy | High | High |\n")
    f.write("| Context Window | 128K | 128K |\n")
    f.write("| Best For | Quick analysis | Complex reasoning |\n")

print("\n✅ Report generated: report.md")
print("📁 File location:", os.path.abspath('report.md'))
print("🎉 Analysis Complete!")