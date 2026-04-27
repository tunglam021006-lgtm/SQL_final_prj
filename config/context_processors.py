from .ui_texts import get_lang_from_request, get_ui_texts


def ui_texts(request):
    lang = get_lang_from_request(request)
    return {
        "LANG_CODE": lang,
        "T": get_ui_texts(lang),
    }