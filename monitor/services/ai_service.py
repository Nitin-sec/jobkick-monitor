from monitor.ai_logger import log_ai_usage


def track_ai_success(
    user_id,
    api_provider,
    model_name,
    endpoint,
    tokens_input,
    tokens_output,
    estimated_cost,
    api_key,
):
    return log_ai_usage(
        user_id=user_id,
        api_provider=api_provider,
        model_name=model_name,
        endpoint=endpoint,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        estimated_cost=estimated_cost,
        api_key=api_key,
        status="success",
        error_message=None,
    )


def track_ai_failure(
    user_id,
    api_provider,
    model_name,
    endpoint,
    tokens_input,
    tokens_output,
    estimated_cost,
    api_key,
    error_message,
):
    return log_ai_usage(
        user_id=user_id,
        api_provider=api_provider,
        model_name=model_name,
        endpoint=endpoint,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        estimated_cost=estimated_cost,
        api_key=api_key,
        status="failure",
        error_message=error_message,
    )
