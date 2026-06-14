import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from alphabetic_sort import alphabetic_sort, get_supported_languages
from alphabetic_sort.exceptions import AlphabeticSortError

app = FastAPI(title="Alphabetic Sort Demo")

_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)


def _parse_numbers(raw: str) -> list:
    result = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        f = float(token)
        i = int(f)
        result.append(i if f == i else f)
    return result


def _render(request: Request, name: str, context: dict):
    # Starlette 1.x uses keyword-only request + name + context signature
    try:
        return templates.TemplateResponse(request=request, name=name, context=context)
    except TypeError:
        # Fallback for older Starlette where request is part of context dict
        return templates.TemplateResponse(name, {"request": request, **context})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return _render(request, "index.html", {
        "supported_languages": get_supported_languages(),
        "numbers_input": "",
        "lang_selected": "en",
        "result": None,
        "original_numbers": None,
        "original_words": None,
        "sorted_words": None,
        "error": None,
    })


@app.post("/sort", response_class=HTMLResponse)
async def sort_numbers(
    request: Request,
    numbers: str = Form(...),
    lang: str = Form(...),
):
    result = None
    original_numbers = None
    original_words = None
    sorted_words = None
    error = None

    try:
        parsed = _parse_numbers(numbers)
        if not parsed:
            raise ValueError("Please enter at least one number.")
        sorted_nums, orig_words, srtd_words = alphabetic_sort(
            parsed, lang, return_words=True
        )
        result = sorted_nums
        original_numbers = parsed
        original_words = orig_words
        sorted_words = srtd_words
    except AlphabeticSortError as exc:
        error = str(exc)
    except ValueError as exc:
        error = f"Invalid input: {exc}"

    return _render(request, "index.html", {
        "supported_languages": get_supported_languages(),
        "numbers_input": numbers,
        "lang_selected": lang,
        "result": result,
        "original_numbers": original_numbers,
        "original_words": original_words,
        "sorted_words": sorted_words,
        "error": error,
    })
