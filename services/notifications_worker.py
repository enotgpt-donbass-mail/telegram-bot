import logging
import time
import datetime

from router.keyboards import get_cancel_inline_markup, get_assessment_inline_markup
from services.booking_service import BookingService
from storage.models.user import User


class NotificationsWorker:
    @staticmethod
    def run(bot):
        """
            Метод обработки оповещений пользователя
        """
        while True:
            try:
                reserved = BookingService.get_reserved()
                now = datetime.datetime.now().replace(second=0, microsecond=0)

                for reserve in reserved['reserved']:
                    reserve_date = datetime.datetime.strptime(reserved['reserved_datetime'], "%Y-%m-%dT%H:%M:%S").replace(second=0, microsecond=0)

                    # Проверяем заявки за час до начала:
                    if reserve_date == now + datetime.timedelta(hours=1):
                        logging.info(f'Send notification about before 1 hour reserve (user: {reserve['uuid']}, code: {reserve['code']})')
                        send_message_before_hour(reserve['uuid'], reserve['code'], reserve_date.strftime("H:%M"),
                                                 reserve['operation_text'], bot)

                    # Проверяем заявки за 15 минут до начала:
                    if reserve_date == now + datetime.timedelta(minutes=15):
                        logging.info(f'Send notification about before 15 minutes reserve (user: {reserve['uuid']}, code: {reserve['code']})')
                        send_message_before_15_mins(reserve['uuid'], reserve['code'], reserve_date.strftime("H:%M"),
                                                    reserve['operation_text'], bot)

                    # Проверяем заявки спустя час после закрытия
                    if reserve_date == now - datetime.timedelta(hours=1):
                        logging.info(
                            f'Send notification service assessment (user: {reserve['uuid']}, code: {reserve['code']})')
                        send_message_service_assessment(reserve['uuid'], reserve['code'], reserve_date.strftime("H:%M"),
                                                    reserve['operation_text'], bot)
            except Exception as e:
                pass

            time.sleep(60)

def send_message_before_hour(user_uuid, code, operation_time, operation, bot):
    """
        Оповещение за час до окончания брони:
    :param operation:
    :param operation_time:
    :param user_uuid:
    :param code:
    :return:
    """

    try:
        user = User.get(User.login == user_uuid)
        message = f'<b>Ваша электронная очередь с кодом {code} (операция {operation} в {operation_time}) будет уже через час.\n\n🙏 Пожалуйста, не забудьте о своем месте или заблаговременно его отмените. Это важно для нас!'
        markup = get_cancel_inline_markup(code)

        bot.send_message(user.telegram_id, message, reply_markup=markup)
    except Exception as e:
        logging.error(e)

def send_message_before_15_mins(user_uuid, code, operation_time, operation, bot):
    """
        Оповещение за час до окончания брони:
    :param operation:
    :param operation_time:
    :param user_uuid:
    :param code:
    :return:
    """

    try:
        user = User.get(User.login == user_uuid)
        message = f'<b>Ваша электронная очередь с кодом {code} (операция {operation} в {operation_time}) будет уже через через 15 минут.\n\n🙏 Если у вас не получится прибыть на место и активировать талон на терминале до этого времени - пожалуйста, отмените бронь и тем самым облегчите нагрузку на отделение. \n\nМы ждем вас ❤️'
        markup = get_cancel_inline_markup(code)

        bot.send_message(user.telegram_id, message, reply_markup=markup)
    except Exception as e:
        logging.error(e)

def send_message_service_assessment(user_uuid, code, operation_time, operation, bot):
    """
        Оповещение об обслуживании
    :param operation:
    :param operation_time:
    :param user_uuid:
    :param code:
    :return:
    """

    try:
        user = User.get(User.login == user_uuid)
        message = f'<b>️Пожалуйста, оставьте оценку работе и обслуживания сотрудника отделения по проведенной операции: {operation} в {operation_time}</b>'
        markup = get_assessment_inline_markup(code)

        bot.send_message(user.telegram_id, message, reply_markup=markup)
    except Exception as e:
        logging.error(e)

