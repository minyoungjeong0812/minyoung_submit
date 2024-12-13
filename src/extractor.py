import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


class ThreatIntelExtractor:
    def __init__(self, base_url: str, api_key: str, model: str = "meta/llama-3.1-405b-instruct"):
        """
        Initialize the extractor with LLM credentials and model details.
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def load_prompt(self, template_path: str, report_text: str) -> str:
        """
        Load the prompt template and append the report text.
        """
        with open(template_path, "r") as f:
            template = f.read()
        return template + "\n\n" + report_text

    def run_extraction(self, prompt: str) -> str:
        """
        Run extraction by sending the prompt to the LLM and returning the raw JSON string.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        return completion.choices[0].message.content

    def validate_and_normalize_output(self, json_str: str) -> dict:
        """
        Validate that the LLM output is valid JSON and contains the required schema.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError("The LLM output is not valid JSON.")

        if "entities" not in data or "relationships" not in data:
            raise ValueError("The JSON does not contain required keys 'entities' or 'relationships'.")

        for entity in data["entities"]:
            if "id" not in entity or "name" not in entity or "type" not in entity:
                raise ValueError("An entity is missing 'id', 'name', or 'type' fields.")

        for rel in data["relationships"]:
            if "source" not in rel or "target" not in rel or "type" not in rel:
                raise ValueError("A relationship is missing 'source', 'target', or 'type' fields.")

        return data

    def load_report(self, source: str) -> str:
        """
        Load the report text from either a URL or a local file path.
        If source is a URL, fetch the content and parse with BeautifulSoup.
        If source is a file path, read the file.
        """
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source)
            response.raise_for_status()
            content = response.text
        else:
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text()
        return text.strip()

    def extract_threat_intel(self, report_source: str, prompt_path: str) -> dict:
        """
        High-level method to:
        1. Load prompt and report
        2. Run extraction
        3. Validate and return results
        """
        report_text = self.load_report(report_source)
        prompt = self.load_prompt(prompt_path, report_text)
        raw_output = self.run_extraction(prompt)
        data = self.validate_and_normalize_output(raw_output)
        return data