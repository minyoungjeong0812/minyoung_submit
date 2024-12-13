# Cyber Threat Intelligence Entity and Relationship Extraction

## Overview

This project uses a Large Language Model (LLM), specifically Llama 3.1 405b instruct model, to automatically extract entities and relationships from a cybersecurity threat intelligence report. After extracting these entities and relationships into structured JSON, you can optionally visualize them using a provided script. Additionally, a test.py script is included for experimenting with or testing the NVIDIA NIM API endpoint.

## Code Structure

extractor.py (under src directory): Contains the ThreatIntelExtractor class that encapsulates all logic for:

- Loading and preparing prompts.
- Interacting with the LLM.
- Validating and normalizing the output.

prompt.txt (under src directory) : Contains a promprt to interact with the Llama model

main.py: Provides a command-line interface (CLI) to run the extraction process.

visual.py: After the JSON output is generated, this script can load the JSON file and visualize the extracted entities and relationships as a graph.

test.py: A test file to experiment with or validate the NVIDIA NIM API endpoint directly, separate from the main extraction workflow.

## Setup Instructions
1. Clone the Repository:

```bash
git clone https://your-repo-url.git
cd your-repo
```
2. Install Dependencies:

```bash
pip install -r requirements.txt
```

3. Provide LLM Credentials and Endpoint:

Ensure you have a valid api_key and base_url for the LLM you intend to use.
Adjust the model parameter as needed in main.py or pass it as a command-line argument.

4. Run the Extraction:

```bash
python src/main.py \
  --report data/sample_report.txt \
  --prompt src/prompt.txt \
  --base_url "https://your.llm.endpoint" \
  --api_key "your_api_key" \
  --output output.json
```

This command reads the input report (data/sample_report.txt), uses the src/prompt.txt template, queries the LLM, and writes the extracted entities and relationships to output.json.

Visualization (Optional): Once output.json is generated, you can visualize the relationships:

```bash
python src/visual.py \
  --input output.json \
  --output_graph graph.png
```

This will produce graph.png, a visual representation of the extracted entities and their relationships.

## Testing the NVIDIA NIM API Endpoint (Optional)
The test.py file can be used to test direct interactions with the NVIDIA NIM API endpoint, separate from the main extraction logic:

```bash
python src/test.py \
  --base_url "https://integrate.api.nvidia.com/v1" \
  --api_key "your_test_api_key"
```

Use this for debugging API responses, ensuring authentication works, or experimenting with queries.

## Notes and Limitations

- Prompt Tuning: You may need to adjust the prompt in prompt.txt for better accuracy in extraction.
- LLM Output Format: If the LLM fails to return valid JSON, consider adjusting the prompt or lowering the temperature.
- Visualization: The visualization is based on networkx and matplotlib. You can improve or customize layouts, colors, and edge labels in visual.py.
- Performance: For larger reports, consider additional preprocessing or chunking logic.

## Example

Input (data/sample_report.txt):

```
The threat actor "ShadowBear" has been identified using the malware "MalNet"
in a targeted campaign against the healthcare industry in Europe.
The campaign involved phishing emails to deliver the malware. ShadowBear
is suspected of being linked to the region of Eastern Europe and has
previously targeted government institutions.
```

Expected Output (output.json):

```json
{
  "entities": [
    {"id": "1", "name": "ShadowBear", "type": "Threat Actor"},
    {"id": "2", "name": "MalNet", "type": "Malware"},
    {"id": "3", "name": "Healthcare", "type": "Industry"},
    {"id": "4", "name": "Europe", "type": "Region"}
  ],
  "relationships": [
    {"source": "1", "target": "2", "type": "uses"},
    {"source": "1", "target": "3", "type": "targets"},
    {"source": "1", "target": "4", "type": "associated_with"}
  ]
}
```

After running visual.py, the resulting graph.png will show these entities as nodes and their relationships as directed edges.

## Further Extensions

- Additional Entity Types: Modify the prompt and possibly add validation code for new entity types.
- Integration with Knowledge Graphs: Use the extracted data to feed into a knowledge graph system.
- Advanced Visualization: Use interactive visualization libraries (e.g., Plotly, pyvis) for more complex interactions.

By following these instructions, one should be able to run extraction, visualize results, and test the NVIDIA NIM endpoint.
