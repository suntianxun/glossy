"""Base decorator for GlassDash chart components."""

from functools import wraps
from glassdash.components._validation import SCHEMAS, validate_dataframe, _render_error_card


def _with_validation(chart_func):
    """Decorator that validates DataFrame before calling chart function."""

    @wraps(chart_func)
    def wrapper(dataframe=None, **kwargs):
        schema = SCHEMAS.get(chart_func.__name__, {})

        if schema and dataframe is not None:
            is_valid, errors = validate_dataframe(dataframe, schema)
            if not is_valid:
                return _render_error_card(chart_func.__name__, errors, dataframe.columns)

        return chart_func(dataframe=dataframe, **kwargs)

    return wrapper
