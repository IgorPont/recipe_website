from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


class CustomExceptionHandlerMiddleware:
    """
    Кастомное логирование необработанных исключений и
    возврат страницы с ошибкой 500
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Логирование исключения
        logger.exception("An error occurred: %s", str(exception))

        # Возвращаем пользователю страницу с ошибкой 500
        if isinstance(exception, Exception):
            return render(request, 'errors/500.html', status=500)
