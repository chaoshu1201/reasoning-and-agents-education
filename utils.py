import litellm
from IPython.display import Markdown, display
import os
from dataclasses import dataclass
from enum import Enum

# Define Model API configuration data structure
@dataclass
class ModelApiConfig:
    provider: str                           # Required string
    name: str                               # Required string
    base_url: str | None = None            # Optional string (defaults to None)
    stream: bool = False                   # Optional boolean (defaults to False)
    temperature: float | None = None       # Sampling temperature (0.0 = deterministic)
    top_p: float | None = None            # Nucleus sampling threshold
    max_tokens: int | None = None         # Maximum tokens to generate
    stop: str | list | None = None        # Stop sequence(s)
    logprobs: bool | None = None          # Whether to return log probabilities
    top_logprobs: int | None = None       # Number of top token logprobs to return (1–5)
    seed: int | None = None               # Random seed for reproducibility

# Define supported models
class LLMModels(Enum):
    GITHUB_GPT_41_MINI = ModelApiConfig(
        provider="github",
        name="gpt-4.1-mini",
    )
    GITHUB_GPT_41_NANO = ModelApiConfig(
        provider="github",
        name="gpt-4.1-nano",
    )
    GEMINI_3_FLASH = ModelApiConfig(
        provider="gemini",
        name="gemini-3-flash-preview",
    )
    OLLAMA_QWEN_2_5_1_5B = ModelApiConfig(
        provider="ollama",
        name="qwen2.5:1.5b",
        base_url="http://localhost:11434"
    )
    OLLAMA_QWEN_2_5_7B = ModelApiConfig(
        provider="ollama",
        name="qwen2.5:7b",
        base_url="http://localhost:11434"
    )
    OLLAMA_QWEN_3_1_7B = ModelApiConfig(
        provider="ollama",
        name="qwen3:1.7b",
        base_url="http://localhost:11434"
    )
    OLLAMA_QWEN_3_4B = ModelApiConfig(
        provider="ollama",
        name="qwen3:4b",
        base_url="http://localhost:11434"
    )
    OLLAMA_DEEPSEEK_R1_1_5B = ModelApiConfig(
        provider="ollama",
        name="deepseek-r1:1.5b",
        base_url="http://localhost:11434"
    )
    OLLAMA_GEMMA_3_1B = ModelApiConfig(
        provider="ollama",
        name="gemma3:1b",
        base_url="http://localhost:11434"
    )
    OLLAMA_GEMMA_3_4B_IT_QAT = ModelApiConfig(
        provider="ollama",
        name="gemma3:4b-it-qat",
        base_url="http://localhost:11434"
    )
    OLLAMA_MINISTRAL_3_3B = ModelApiConfig(
        provider="ollama",
        name="ministral-3:3b",
        base_url="http://localhost:11434"
    )
    OLLAMA_LLAMA_3_2_3B = ModelApiConfig(
        provider="ollama",
        name="llama3.2:3b",
        base_url="http://localhost:11434"
    )


def _format_message_content(message):
    """Combine reasoning and content into a single display string."""
    reasoning = getattr(message, "reasoning_content", None)
    content = message.content or ""
    if reasoning:
        return f"<think>{reasoning}</think>{content}"
    return content

def get_completion(system_prompt=None, user_prompt=None, messages=None, model_api_config=LLMModels.GITHUB_GPT_41_MINI.value):
    """
    Get a completion through LiteLLM.
    Args:
        system_prompt: The system prompt
        user_prompt: The user prompt
        messages: List of messages for chat-based models
        model_api_config: The model API configuration to use (default is GITHUB_GPT_41_MINI)
    Returns:
        A (text, response) tuple. Normal success returns the completion text
        and full response object. Streaming success returns (text, None).
        A caught exception returns ("An error occurred: ...", None).
        A None response indicates unavailable metadata, not necessarily failure.
    """
    messages = list(messages or [])
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    try:
        kwargs = {
            "model": f"{model_api_config.provider}/{model_api_config.name}",
            "messages": messages,
            "base_url": model_api_config.base_url,
            "temperature": model_api_config.temperature if model_api_config.temperature is not None else 0.7,
            "top_p": model_api_config.top_p if model_api_config.top_p is not None else 1.0,
            "stream": model_api_config.stream,
        }
        if model_api_config.max_tokens is not None:
            kwargs["max_tokens"] = model_api_config.max_tokens
        if model_api_config.stop is not None:
            kwargs["stop"] = model_api_config.stop
        if model_api_config.logprobs is not None:
            kwargs["logprobs"] = model_api_config.logprobs
        if model_api_config.top_logprobs is not None:
            kwargs["top_logprobs"] = model_api_config.top_logprobs
        if model_api_config.seed is not None:
            kwargs["seed"] = model_api_config.seed

        # Use LiteLLM for multi-provider support
        response = litellm.completion(**kwargs)

        # Handle streaming vs non-streaming responses
        if model_api_config.stream:
            # For streaming, iterate through chunks and collect content
            completion = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    completion += content
            print()  # Print newline at the end
            return completion, None
        else:
            # For non-streaming, access content directly
            message = response.choices[0].message
            content = _format_message_content(message)
            return content, response
    except Exception as e:
        return f"An error occurred: {e}", None


def get_n_completions(
    n,
    system_prompt=None,
    user_prompt=None,
    messages=None,
    model_api_config=LLMModels.GITHUB_GPT_41_MINI.value,
    temperature=0.7,
):
    """
    Function to get multiple completions from a single LiteLLM API call.

    Args:
        n: Number of completions to generate
        system_prompt: The system prompt
        user_prompt: The user prompt
        messages: List of messages for chat-based models
        model_api_config: The model API configuration to use (default is GITHUB_GPT_41_MINI)
        temperature: Sampling temperature

    Returns:
        List of completion texts
    """
    n = int(n)
    if n <= 0:
        return []

    messages = list(messages or [])
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    def _extract_content(choice):
        return _format_message_content(choice.message)

    try:
        response = litellm.completion(
            model=f"{model_api_config.provider}/{model_api_config.name}",
            messages=messages,
            base_url=model_api_config.base_url,
            temperature=temperature,
            n=n,
            stream=False,
        )

        return [_extract_content(choice) for choice in response.choices]
    except Exception as e:
        unsupported_n = (
            e.__class__.__name__ == "UnsupportedParamsError"
            or "does not support parameters: ['n']" in str(e)
        )

        if unsupported_n:
            try:
                completions = []
                for _ in range(n):
                    single_response = litellm.completion(
                        model=f"{model_api_config.provider}/{model_api_config.name}",
                        messages=messages,
                        base_url=model_api_config.base_url,
                        temperature=temperature,
                        stream=False,
                    )
                    completions.append(_extract_content(single_response.choices[0]))
                return completions
            except Exception as fallback_error:
                return [f"An error occurred: {fallback_error}"]

        return [f"An error occurred: {e}"]


def display_responses(*args):
    """Helper function to display responses as Markdown, horizontally."""
    markdown_string = "<table><tr>"
    # Headers
    for arg in args:
        markdown_string += f"<th>System Prompt:<br />{arg['system_prompt']}<br /><br />"
        markdown_string += f"User Prompt:<br />{arg['user_prompt']}</th>"
    markdown_string += "</tr>"
    # Rows
    markdown_string += "<tr>"
    for arg in args:
        markdown_string += f"<td>Response:<br />{arg['response']}</td>"
    markdown_string += "</tr></table>"
    display(Markdown(markdown_string))

def display_responses_truncated(*args, user_prompt_limit=500):
    """Helper function to display responses as Markdown, horizontally."""
    markdown_string = "<table><tr>"
    # Headers
    for arg in args:
        markdown_string += f"<th>System Prompt:<br />{arg['system_prompt']}<br /><br />"
        markdown_string += f"User Prompt:<br />{arg['user_prompt'][:user_prompt_limit]}"
        if len(arg["user_prompt"]) > user_prompt_limit:
            markdown_string += "... [truncated]"
        markdown_string += "</th>"
    markdown_string += "</tr>"
    # Rows
    markdown_string += "<tr>"
    for arg in args:
        markdown_string += f"<td>Response:<br />{arg['response']}</td>"
    markdown_string += "</tr></table>"
    display(Markdown(markdown_string))

SINGLE_TAB_LEVEL = 4

def print_in_box(text, title="", cols=100, tab_level=0):
    """
    Prints the given text in a box with the specified title and dimensions.

    Args:
        text: The text to print in the box.
        title: The title of the box.
        cols: The width of the box.
        tab_level: The level of indentation for the box.
    """
    import textwrap

    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
        tabs
        + "\u2554"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u2557"
    )
    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2 :]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
            line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )


def _fmt_value(value):
    return repr(value) if isinstance(value, str) else str(value)


def _print_tree(value, indent=0, key=None):
    pad = "  " * indent
    label = f"{key}: " if key is not None else ""
    if isinstance(value, dict):
        items = {k: v for k, v in value.items() if v is not None and v != {}}
        if not items:
            return
        print(f"{pad}{label}")
        for k, v in items.items():
            _print_tree(v, indent + 1, k)
    elif isinstance(value, list):
        print(f"{pad}{label}[{len(value)}]")
        for i, v in enumerate(value):
            _print_tree(v, indent + 1, f"[{i}]")
    elif value is not None:
        print(f"{pad}{label}{_fmt_value(value)}")


def print_response(response, max_top_logprobs=5):
    """Print a litellm ModelResponse as an indented, human-readable tree.

    Token logprobs are shown as a compact table (probability and top alternatives)
    instead of the raw nested lists with byte arrays.
    """
    import math

    data = response.model_dump() if hasattr(response, "model_dump") else dict(response)
    choices = data.pop("choices", [])
    _print_tree(data)

    print(f"choices: [{len(choices)}]")
    for choice in choices:
        logprobs = choice.pop("logprobs", None)
        message = choice.pop("message", {})
        content = message.pop("content", None)
        _print_tree(choice, 1, f"[{choice.get('index', 0)}]")
        print("    message:")
        print(f"      role: {message.pop('role', None)!r}")
        print("      content:")
        for line in (content or "").splitlines() or [""]:
            print(f"        | {line}")
        _print_tree(message, 3)

        tokens = (logprobs or {}).get("content") or []
        if tokens:
            print("    logprobs:")
            for t in tokens:
                p = math.exp(t["logprob"])
                print(f"      {t['token']!r:<14} p={p:7.2%}  logprob={t['logprob']:.4f}")
                alts = [a for a in t.get("top_logprobs", []) if a["token"] != t["token"]]
                for a in alts[: max_top_logprobs - 1]:
                    print(
                        f"          alt {a['token']!r:<12} p={math.exp(a['logprob']):7.2%}"
                    )
