import argparse
import json
from extractor import ThreatIntelExtractor

def main():
    parser = argparse.ArgumentParser(description="Entity and Relationship Extraction from Cybersecurity Reports")
    parser.add_argument("--report", type=str, required=True, help="Path or URL to the input report (text or HTML)")
    parser.add_argument("--prompt", type=str, default="src/prompt.txt", help="Path to the prompt template")
    parser.add_argument("--output", type=str, default="output.json", help="Path to save the JSON output")
    parser.add_argument("--base_url", type=str, required=True, help="Base URL for LLM endpoint")
    parser.add_argument("--api_key", type=str, required=True, help="API key for LLM")
    parser.add_argument("--model", type=str, default="meta/llama-3.1-405b-instruct", help="Model name")

    args = parser.parse_args()

    extractor = ThreatIntelExtractor(base_url=args.base_url, api_key=args.api_key, model=args.model)
    data = extractor.extract_threat_intel(args.report, args.prompt)

    with open(args.output, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Extraction completed. Results saved to {args.output}")

if __name__ == "__main__":
    main()
