"""Base decorator for GlassDash chart components."""

import inspect
from functools import wraps

from glassdash.components._validation import SCHEMAS, _render_error_card, validate_dataframe


def _with_validation(chart_func):
    """Decorator that validates DataFrame before calling chart function."""

    @wraps(chart_func)
    def wrapper(dataframe=None, **kwargs):
        schema = SCHEMAS.get(chart_func.__name__, {})

        if schema and dataframe is not None:
            # Resolve actual column names from parameters (handles x="month", y="fte" style calls)
            sig = inspect.signature(chart_func)
            bound = sig.bind_partial(**kwargs)
            # Apply defaults for missing args
            for param_name, param in sig.parameters.items():
                if (
                    param_name not in bound.arguments
                    and param.default is not inspect.Parameter.empty
                ):
                    bound.arguments[param_name] = param.default

            # Map schema keys to actual column names
            column_mapping = {}
            for key in schema:
                if key in bound.arguments:
                    val = bound.arguments[key]
                    # Only treat string values as column names
                    if isinstance(val, str):
                        column_mapping[key] = val

            is_valid, errors = validate_dataframe(dataframe, schema, column_mapping)
            if not is_valid:
                return _render_error_card(chart_func.__name__, errors, dataframe.columns)

        return chart_func(dataframe=dataframe, **kwargs)

    return wrapper
