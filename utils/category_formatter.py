def format_category(category: str) -> str:
    match category:
        case 'Отправления':
            return '📦 Отправления'
        case 'Переводы':
            return '✉️ Переводы'
        case 'Платежи':
            return '💵 Платежи'
        case 'Стартовые пакеты':
            return '🏷 Стартовые пакеты'
        case 'Прочее':
            return '🗂 Прочее'

    return category

def reformat_category(category: str) -> str:
    match category:
        case '📦 Отправления':
            return 'Отправления'
        case '✉️ Переводы':
            return 'Переводы'
        case '💵 Платежи':
            return 'Платежи'
        case '🏷 Стартовые пакеты':
            return 'Стартовые пакеты'
        case '🗂 Прочее':
            return 'Прочее'

    return category