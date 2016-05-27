$(function () {
    var widgetPopup = '#add_widget';
    var $addWidgetForm = $('form[name=add_widget]', widgetPopup);
    // добавление виджета
    $addWidgetForm.on('submit', function (event) {
        event.preventDefault();
        createOrUpdateWidget(this, 'PUT', function (data) {
            // добавляем в начало (свежие записи - первые)
            $('.card-columns').prepend(data);
        });
    });

    var editWidget = '#edit_widget';
    var $editWidgetForm = $('form', editWidget);
    // получение инфы о виджете
    $('[data-widget=edit]').on('click', function () {
        var widgetId = $(this).closest('[data-id]').data('id');
        // GET-запрос с передачей id-шника
        $.get('/widget?id=' + widgetId, function (data) {
            // заполняем поля попапа
            $('span.widget_id', editWidget).html(widgetId);
            $('textarea', $editWidgetForm).val(data.message);
            $('select', $editWidgetForm).val(data.color);
            $('input[name=id]', $editWidgetForm).val(data.id);
            $('input[name=image]', $editWidgetForm).val(data.image);
            // открываем его
            $(editWidget).modal();
        })
    });

    // редактирование виджета
    $editWidgetForm.on('submit', function (event) {
        event.preventDefault();
        createOrUpdateWidget(this, 'POST', function (data) {
            var $card = $('.card[data-id=' + data.id + ']');
            // вычищаем классы-бэкграунды и добавляем нужный
            $('.card-block', $card).removeClass('card-primary card-info card-success card-warning card-danger');
            $('.card-block', $card).addClass('card-' + data.color);
            // сам текст
            $('p', $card).html(data.message);
            // проставляем дату создания и модификации
            var cite = data.created;
            if (data.created != data.modified) {
                cite += ' (' + data.modified + ')';
            }
            $('cite', $card).html(cite);
            // и картиночку
            $('img', $card).attr('src', data.image);
        });
    });

    /**
     * AJAX-запрос на импорт (создание/редактирование) виджета
     *
     * @param form      Элемент формы (не jQuery-объект)
     * @param method    Метод отпавки формы
     * @param callback  Функция после успешного запроса (1 аргумент - полученные данные)
     */
    var createOrUpdateWidget = function (form, method, callback) {
        $form = $(form);
        $.ajax({
            url: "/widget",
            method: method,
            data: $form.serialize(),
            success: function (data) {
                callback.call(this, data);
                // закрываем попап
                $form.closest('.modal').modal('hide');
                // очищаем поля формы
                //$('input, select, textarea', $form).val('');
                $('input, textarea', $form).val('');
                $('select', $form).prop('selectedIndex', 0);
            }
        });
    };

    // удаление виджета
    $('[data-widget=delete]').on('click', function () {
        var widgetId = $(this).closest('[data-id]').data('id');
        $.ajax({
            url: "/widget",
            method: 'DELETE',
            data: {id: widgetId},
            success: function (data) {
                // удаляем ноду с дата-атрибутом, который вернул аякс-запрос
                $('.card[data-id=' + data.id + ']').remove();
            }
        });
    });

    var settings = '#settings';
    var $settingsForm = $('form', settings);

    // получение настроек
    $('[data-target="#settings"]').on('click', function () {
        $.get('/settings', function (data) {
            $('input[name=name]', $settingsForm).val(data.name);
            $('input[name=surname]', $settingsForm).val(data.surname);
            $('input[name=birthdate]', $settingsForm).val(data.birthdate);
            $('input[name=sex][value=' + data.sex + ']', $settingsForm).prop('checked', true);
            $('input[name=city]', $settingsForm).val(data.city);
        })
    });

    // обновление настроек
    $settingsForm.on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: "/settings",
            method: 'POST',
            data: $settingsForm.serialize(),
            success: function (data) {
                var $userbar = $('#self .media');
                $('h4', $userbar).html(data.name + ' ' + data.surname);
                $('p', $userbar).html(data.age + ', ' + data.city);
                // баба или мужик?
                var src = data.sex == 'female' ? '/static/img/woman.png' : '/static/img/man.png';
                $('img', $userbar).attr('src', src);
                $settingsForm.closest('.modal').modal('hide');
                $('input:not([type=radio]), select, textarea', $settingsForm).val('');
            }
        });
    });
});