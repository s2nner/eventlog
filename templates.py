print_global = """
95-й перцентиль времени работы: {{ p }}
Идентификаторы запросов с самой долгой фазой отправки результатов пользователю: {{ r }}
Запросы с неполным набором ответевших ГР: {{ gr }}
"""


group_request = """
ID реквеста: {{ id }}
    {% for gr, backends in gr.items() %}
    ГР: {{ gr }}
        {% for id, backend in backends.items() %}
            {{ backend.name }}
            Обращения: 
                {{ backend.requests }}
            {% if backend.errors %}
            Ошибки: 
                {{ backend.errors }}
            {% endif %}
        {% endfor %}
    {% endfor %}
"""