from fastapi.openapi.utils import get_openapi

from src.app.main import app


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Swagger documentation",
        version="0.0.1",
        summary="",
        description="Данная схема описывает следующие эндпоинты:\n \
            /short - основной эндпоинт, принимающий длинную ссылку и возвращающий короткую;\n\
            /{url_id} - эндпоинт, позволяющий осуществлять редирект по короткой ссылке.\n\
            /healthz/ready - технический обработчик проверяющий готовность бд и сервиса\n\
            /healthz/up - технический обработчик проверяющий поднятость сервиса",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

js = str(app.openapi())

with open('openapi.json', 'w') as outfile:
    outfile.write(js)