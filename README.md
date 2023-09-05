## Контекст

Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», рассылки для информирования и привлечения клиентов.
Разработайте сервис управления рассылками, администрирования и получения статистики.

## Описание задачи

- Реализуйте интерфейс заполнения рассылок, то есть CRUD-механизм для управления рассылками.
- Реализуйте скрипт рассылки, который работает как из командой строки, так и по расписанию.
- Добавьте настройки конфигурации для периодического запуска задачи.

## Сущности системы

- Клиент сервиса:
  - контактный email,
  - ФИО,
  - комментарий.
- Рассылка (настройки):
  - время рассылки;
  - периодичность: раз в день, раз в неделю, раз в месяц;
  - статус рассылки: завершена, создана, запущена.
- Сообщение для рассылки:
  - тема письма,
  - тело письма.
- Логи рассылки:
  - дата и время последней попытки;
  - статус попытки;
  - ответ почтового сервера, если он был.


Программа для автоматизации рассылок.

Страницы: главная, клиенты, рассылки, завершенные рассылки, сообщения, блог, вход/регистрация/восстановление пароля.

После запуска сервера рассылка может быть запущена
- вручную командой "python manage.py mailing"
- выполняться автоматически с установленной периодичностью после выполнения команды "python manage.py crontab add".
  Периодичность работы по умолчанию - 1 минута, настраивается в settings.py в переменной CRONJOBS.

При запуске скрипта проверяются данные рассылок, при наступлении времени, указанного в рассылке,
происходит отправка писем по содержащимся в рассылке адресам. При каждой отправке формируется лог, 
рассылка деактивируется до наступления очередного времени в соответствии с требованиями - раз в день, неделю, месяц.

Кроме того, реализован блог, регистрация пользователей.
