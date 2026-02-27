import requests
import logging

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b-instruct"

def check_ollama_connection():
    """Verify Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        logger.info(f"Ollama is running. Available models: {[m.get('name') for m in models]}")
        
        # Check if the required model is installed
        model_names = [m.get('name', '').split(':')[0] for m in models]
        if 'qwen2.5' not in model_names:
            logger.warning(f"Model {MODEL_NAME} is not installed. Please run: ollama pull qwen2.5:3b-instruct")
            return False, f"Model {MODEL_NAME} not found. Available: {model_names}"
        
        return True, "Ollama is ready"
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama at http://localhost:11434")
        return False, "Ollama is not running. Start it with: ollama serve"
    except Exception as e:
        logger.error(f"Ollama connection error: {e}")
        return False, str(e)

def build_grounded_prompt(question, docs, confidence):
    # docs is the list your retriever returns (content + metadata)
    context_lines = []
    for i, d in enumerate(docs, start=1):
        context_lines.append(f"[{i}] {d['content']}")
    context = "\n\n".join(context_lines)

    return f"""You are an internal knowledge assistant.

RULES:
1) Answer ONLY using the CONTEXT.
2) Add citations like [1], [2] after each sentence.
3) If the answer is not in the context, say exactly: Not found in the provided documents.
4) Be concise.

CONFIDENCE: {confidence}

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

def generate_answer(question, context_unused, sources, confidence):
    """Generate answer using Ollama"""
    try:
        prompt = build_grounded_prompt(question, sources, confidence)

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 220
            }
        }

        logger.debug(f"Sending request to Ollama: {OLLAMA_URL}")
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        
        if r.status_code != 200:
            logger.error(f"Ollama returned status {r.status_code}: {r.text}")
            raise Exception(f"Ollama error: {r.status_code}")
        
        response_data = r.json()
        answer = response_data.get("response", "").strip()
        
        print("answer",answer)
        if not answer:
            logger.warning("Ollama returned empty response")
            return "Unable to generate answer. Please try again."
        
        return answer
        
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        raise Exception("Response generation timed out. Model may be overloaded.")
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama")
        raise Exception("Cannot connect to Ollama. Make sure it's running on port 11434.")
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise
