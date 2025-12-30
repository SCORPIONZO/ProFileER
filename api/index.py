import os
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Получаем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN обязательна")

# Создаем приложение глобально
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка сообщения при команде /start"""
    welcome_text = (
        "Добро пожаловать в бота по изучению психологических профилей поведения!\n\n"
        "Это обучающее приложение по профилированию и выявлению обмана.\n\n"
        "Доступные команды:\n"
        "/profiles - Просмотреть список всех психологических профилей\n"
        "/help - Получить справочную информацию\n\n"
        "Выберите интересующий вас профиль из меню ниже:"
    )
    
    keyboard = [[InlineKeyboardButton("Просмотреть профили", callback_data='show_profiles')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка справочной информации при команде /help"""
    help_text = (
        "СПРАВКА:\n\n"
        "Это приложение предназначено для изучения различных типов поведения человека и создания психологических профилей.\n\n"
        
        "КАК ИСПОЛЬЗОВАТЬ:\n"
        "1. Используйте команду /profiles для просмотра всех профилей\n"
        "2. Нажмите на интересующий вас профиль\n"
        "3. Получите подробную информацию о типе поведения\n\n"
        
        "Психологический профиль включает:\n"
        "- Характерные черты\n"
        "- Поведенческие особенности\n"
        "- Тип темперамента\n"
        "- Признаки обмана\n"
        "- Рекомендации по ведению диалога"
    )
    
    await update.message.reply_text(help_text)


class ProfileBot:
    def __init__(self):
        self.data_file = "profiles.json"
        self.profiles = self.load_profiles()
    
    def load_profiles(self):
        """Загрузка профилей из JSON файла"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.data_file} не найден, создаем пустой список")
            return []
        except json.JSONDecodeError:
            print(f"Ошибка чтения {self.data_file}, создаем пустой список")
            return []

    def format_profile(self, profile):
        """Форматирование профиля для отправки в Telegram"""
        profile_text = f"*{profile['name']}*\n\n"
        profile_text += f"_{profile['description']}_\n\n"
        
        profile_text += "*ХАРАКТЕРНЫЕ ЧЕРТЫ:*\n"
        for trait in profile["traits"]:
            profile_text += f"• {trait}\n"
        
        profile_text += "\n*ПОВЕДЕНЧЕСКИЕ ОСОБЕННОСТИ:*\n"
        for behavior in profile["behaviors"]:
            profile_text += f"• {behavior}\n"
        
        # Добавляем дополнительные поля если они существуют
        if "temperament" in profile:
            profile_text += "\n*ТИП ТЕМПЕРАМЕНТА:*\n"
            for temperament in profile.get("temperament", ["Информация отсутствует"]):
                profile_text += f"• {temperament}\n"
        
        if "sexual_behavior" in profile:
            profile_text += "\n*СЕКСУАЛЬНОЕ ПОВЕДЕНИЕ:*\n"
            for behavior in profile.get("sexual_behavior", ["Информация отсутствует"]):
                profile_text += f"• {behavior}\n"
        
        if "clothing_preferences" in profile:
            profile_text += "\n*ПРЕДПОЧТЕНИЯ В ОДЕЖДЕ:*\n"
            for clothing in profile.get("clothing_preferences", ["Информация отсутствует"]):
                profile_text += f"• {clothing}\n"
        
        # Добавляем анализ обмана
        profile_text += "\n*АНАЛИЗ ПОВЕДЕНИЯ НА ПРЕДМЕТ ОБМАНА:*\n"
        deception_indicators = self.get_deception_indicators_for_profile(profile)
        if deception_indicators:
            profile_text += f"Признаки обмана для профиля '{profile['name']}':\n"
            for indicator in deception_indicators:
                profile_text += f"• {indicator}\n"
        else:
            profile_text += f"Профиль '{profile['name']}' не содержит специфических признаков обмана.\n"
        
        # Добавляем общие признаки обмана
        profile_text += "\n*ОБЩИЕ ПРИЗНАКИ ОБМАНА В ПОВЕДЕНИИ:*\n"
        general_indicators = self.get_general_deception_indicators()
        for indicator in general_indicators:
            profile_text += f"• {indicator}\n"
        
        # Добавляем рекомендации по диалогу
        profile_text += "\n*ВЕДЕНИЕ ДИАЛОГА С ТИПОМ ЛИЧНОСТИ:*\n"
        dialog_approaches = self.get_dialog_approaches_for_profile(profile)
        for approach in dialog_approaches:
            profile_text += f"• {approach}\n"
        
        return profile_text

    def get_general_deception_indicators(self):
        """Получение общих признаков обмана"""
        return [
            "Когнитивная нагрузка: более медленные ответы, паузы, запинания",
            "Несоответствие вербальной и невербальной информации",
            "Изменение стиля речи и использования языка",
            "Увеличение дистанции в общении",
            "Избегание прямого ответа на вопросы",
            "Увеличение количества оговорок и переспросов",
            "Изменение жестов и мимики (увеличение или уменьшение)",
            "Контрольные движения: прикосновения к лицу, уху, горлу",
            "Непривычное поведение, нехарактерное для человека",
            "Избегание зрительного контакта или наоборот чрезмерное внимание",
            "Физиологические признаки стресса: потливость, дрожь, покраснение"
        ]

    def get_deception_indicators_for_profile(self, profile):
        """Получение специфических признаков обмана для профиля"""
        name_lower = profile["name"].lower()

        # Научно обоснованные признаки обмана для разных типов личностей
        profile_indicators = {
            "нарциссический": [
                "Искажение реальности в целях самоидеализации",
                "Преувеличение своих достижений и талантов",
                "Использование харизмы для манипуляции",
                "Склонность к созданию ложного впечатления",
                "Попытки контролировать восприятие окружающих через ложь"
            ],
            "пассивно-агрессивное": [
                "Косвенное выражение негативных чувств вместо прямого признания",
                "Скрытое саботирование при ложных заверениях о сотрудничестве",
                "Фальшивое согласие с последующим неисполнением",
                "Ложь о причинах провала с целью избежать ответственности"
            ],
            "антиобщественное": [
                "Повторяющееся лгание и обман для получения выгоды",
                "Использование обаяния для манипуляции (социопатический обман)",
                "Отсутствие чувства вины при лжи",
                "Мошенническое поведение с тщательно спланированными ложными историями",
                "Склонность к созданию ложных биографий"
            ],
            "пограничное": [
                "Ложь, вызванная нестабильностью восприятия реальности",
                "Искажение фактов из-за эмоционального состояния",
                "Попытки манипуляции через жалобы на других",
                "Ложь для получения эмоциональной реакции"
            ],
            "шизоидное": [
                "Отказ от общения может быть воспринят как обман",
                "Склонность к изоляции, которая может скрывать истинные намерения"
            ],
            "параноидное": [
                "Скрытие информации из-за недоверия",
                "Искажение мотивов из-за подозрительности",
                "Скрытность, которая может быть воспринята как обман",
                "Склонность к интерпретации честных действий других как угроз"
            ],
            "обсессивно-компульсивное": [
                "Чрезмерная педантичность может казаться неестественной",
                "Скрытие ошибок из-за страха перед несовершенством"
            ],
            "истероидное": [
                "Преувеличение эмоций для привлечения внимания",
                "Драматизация ситуаций с искажением реальности",
                "Создание впечатления, что события более значительны, чем они есть на самом деле"
            ],
            "шизотипическое": [
                "Странные убеждения могут быть восприняты как обман",
                "Необычное восприятие реальности, приводящее к ложным убеждениям"
            ],
            "ассистентное": [
                "Подавление своих истинных чувств для избегания конфликта",
                "Согласие с неприемлемыми условиями",
                "Ложь для избегания неприятностей"
            ],
            "депрессивное": [
                "Самоуничижение, которое может искажать реальность",
                "Негативное восприятие ситуации, искажающее факты"
            ],
            "садистическое": [
                "Скрытие истинных мотивов причинения вреда",
                "Обман для получения удовольствия от контроля над другими"
            ],
            "мазохистическое": [
                "Искажение своих способностей для получения негативного внимания",
                "Создание ситуаций, в которых они получают страдания"
            ]
        }

        # Найти подходящие индикаторы для профиля
        matched_indicators = []
        for key, indicators in profile_indicators.items():
            if key in name_lower:
                matched_indicators.extend(indicators)
                break

        return matched_indicators

    def get_dialog_approaches_for_profile(self, profile):
        """Получение рекомендаций по диалогу для конкретного профиля"""
        name_lower = profile["name"].lower()

        # Научно обоснованные рекомендации по диалогу для разных типов личностей
        profile_approaches = {
            "нарциссический": [
                "Подчеркивайте их значимость и уникальность",
                "Используйте уважительный тон и избегайте критики",
                "Показывайте восхищение их достижениями (но не чрезмерно)",
                "Фокусируйтесь на их успехах и талантах",
                "Избегайте конфронтации - они могут воспринять это как угрозу",
                "Будьте уверенными, но не доминирующими в общении"
            ],
            "пассивно-агрессивное": [
                "Будьте прямолинейны и ясны в общении",
                "Избегайте двусмысленных формулировок",
                "Задавайте открытые вопросы для выявления истинных чувств",
                "Не принимайте на веру уклончивые ответы",
                "Обсуждайте поведение напрямую, но деликатно",
                "Предлагайте конструктивные способы выражения недовольства"
            ],
            "антиобщественное": [
                "Сохраняйте формальный, но не слишком интимный тон",
                "Избегайте эмоциональных призывов - они неэффективны",
                "Фокусируйтесь на выгодах и последствиях",
                "Будьте готовы к манипуляциям и попыткам контроля",
                "Устанавливайте четкие границы и следите за их соблюдением",
                "Не пытайтесь вызвать чувство вины - это не сработает"
            ],
            "пограничное": [
                "Будьте последовательны и надежны в общении",
                "Избегайте резких перемен в подходе",
                "Поддерживайте стабильный, спокойный тон",
                "Избегайте двойных сообщений или неоднозначных сигналов",
                "Поддерживайте четкие границы и структуру",
                "Будьте терпеливы с эмоциональными реакциями",
                "Предлагайте стабильность и предсказуемость"
            ],
            "шизоидное": [
                "Уважайте их потребность в дистанции и независимости",
                "Не настаивайте на эмоциональной близости",
                "Фокусируйтесь на интеллектуальных аспектах",
                "Избегайте давления в общении",
                "Предлагайте информацию, а не эмоциональные связи",
                "Будьте терпеливы - они могут быть медлительными в ответах"
            ],
            "параноидное": [
                "Будьте последовательны в словах и действиях",
                "Избегайте двусмысленных высказываний",
                "Демонстрируйте честность и прозрачность",
                "Не отрицайте их подозрения напрямую",
                "Фокусируйтесь на фактах, а не на эмоциях",
                "Избегайте насмешек над их страхами",
                "Демонстрируйте надежность через действия"
            ],
            "обсессивно-компульсивное": [
                "Будьте точными и структурированными в общении",
                "Предоставляйте детальную информацию",
                "Избегайте импровизации - придерживайтесь плана",
                "Уважайте их потребность в контроле",
                "Фокусируйтесь на логике, а не на эмоциях",
                "Предлагайте пошаговые объяснения",
                "Избегайте давления - это может вызвать тревогу"
            ],
            "истероидное": [
                "Обеспечивайте внимание и поддержку",
                "Используйте визуальные средства и демонстрации",
                "Будьте эмоционально отзывчивыми",
                "Избегайте игнорирования их эмоций",
                "Поддерживайте интерес к обсуждению",
                "Используйте яркие примеры и образы",
                "Предоставляйте обратную связь и похвалу"
            ],
            "шизотипическое": [
                "Избегайте критики их странных убеждений",
                "Будьте терпимыми к необычным идеям",
                "Фокусируйтесь на текущих задачах, а не на фантазиях",
                "Используйте простой и понятный язык",
                "Избегайте социального давления",
                "Будьте терпеливы с их социальной неуклюжестью"
            ],
            "антипедическое": [
                "Предоставляйте поддержку и поощрение",
                "Избегайте давления и критики",
                "Помогайте принимать решения постепенно",
                "Демонстрируйте терпение и понимание",
                "Избегайте агрессивного давления",
                "Поддерживайте их инициативу и самостоятельность",
                "Предлагайте помощь, а не командовать"
            ],
            "ассистентное": [
                "Поощряйте выражение собственных потребностей",
                "Избегайте использования их уступчивости",
                "Предлагайте безопасное пространство для выражения мнений",
                "Поддерживайте их, когда они устанавливают границы",
                "Избегайте давления и манипуляций",
                "Признавайте их вклад и усилия",
                "Помогайте развивать уверенность"
            ],
            "депрессивное": [
                "Проявляйте сочувствие и понимание",
                "Избегайте банальностей и критики",
                "Поддерживайте позитивный, но реалистичный тон",
                "Предлагайте эмоциональную поддержку",
                "Будьте терпеливы с негативными мыслями",
                "Фокусируйтесь на сильных сторонах, а не на слабостях",
                "Предлагайте надежду и реальные решения"
            ],
            "садистическое": [
                "Сохраняйте твердую, но спокойную позицию",
                "Избегайте подчинения или уступчивости",
                "Устанавливайте четкие границы и последствия",
                "Фокусируйтесь на ответственности и последствиях",
                "Не поддавайтесь на провокации",
                "Избегайте эмоциональных реакций",
                "Демонстрируйте профессионализм и контроль"
            ],
            "мазохистическое": [
                "Избегайте участия в их саморазрушительном поведении",
                "Поддерживайте их позитивные качества",
                "Избегайте чрезмерной заботы или жалости",
                "Фокусируйтесь на их сильных сторонах",
                "Предлагайте поддержку, а не спасение",
                "Будьте терпеливы с их потребностью в критике"
            ]
        }

        # Найти подходящие рекомендации для профиля
        matched_approaches = []
        for key, approaches in profile_approaches.items():
            if key in name_lower:
                matched_approaches.extend(approaches)
                break

        # Если не найдено специфических рекомендаций, использовать общие
        if not matched_approaches:
            matched_approaches = [
                "Используйте уважительный тон общения",
                "Будьте внимательны к их реакциям",
                "Фокусируйтесь на темах, представляющих интерес для этого типа личности",
                "Избегайте тем, которые могут вызвать негативную реакцию",
                "Демонстрируйте понимание их особенностей",
                "Сохраняйте терпеливое и поддерживающее отношение",
                "Предоставляйте достаточно времени для обработки информации"
            ]

        return matched_approaches


async def profiles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка списка профилей"""
    profile_bot = ProfileBot()  # Создаем экземпляр бота
    
    keyboard = []
    for profile in profile_bot.profiles:
        # Ограничиваем длину callback_data, используя хэш для длинных имен
        profile_name = profile["name"]
        # Проверяем длину в байтах, а не в символах, так как Telegram проверяет байты
        test_callback = f'profile_{profile_name}'
        if len(test_callback.encode('utf-8')) > 64:  # Убедимся, что callback_data не превышает 64 байта
            profile_hash = hashlib.md5(profile_name.encode()).hexdigest()[:8]
            callback_data = f'profile_{profile_hash}'
        else:
            callback_data = test_callback
        keyboard.append([InlineKeyboardButton(profile["name"], callback_data=callback_data)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите психологический профиль:', reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    profile_bot = ProfileBot()  # Создаем экземпляр бота
    
    query = update.callback_query
    await query.answer()
    
    if query.data == 'show_profiles':
        keyboard = []
        for profile in profile_bot.profiles:
            # Ограничиваем длину callback_data, используя хэш для длинных имен
            profile_key = profile["name"]
            # Проверяем длину в байтах, а не в символах, так как Telegram проверяет байты
            test_callback = f'profile_{profile_key}'
            if len(test_callback.encode('utf-8')) > 64:  # Убедимся, что callback_data не превышает 64 байта
                profile_hash = hashlib.md5(profile_key.encode()).hexdigest()[:8]
                callback_data = f'profile_{profile_hash}'
            else:
                callback_data = test_callback
            keyboard.append([InlineKeyboardButton(profile["name"], callback_data=callback_data)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.edit_message_text(text='Выберите психологический профиль:', reply_markup=reply_markup)
        except Exception:
            # Если не удалось отредактировать сообщение, отправляем новое
            await query.message.reply_text('Выберите психологический профиль:', reply_markup=reply_markup)

    elif query.data.startswith('profile_'):
        # Проверяем, является ли это хэш-идентификатором
        profile_key = query.data[8:]  # Убираем 'profile_' из начала
        
        # Ищем профиль по имени или по хэшу
        profile = None
        for p in profile_bot.profiles:
            # Проверяем оригинальное имя
            test_callback = f'profile_{p["name"]}'
            if p["name"] == profile_key and len(test_callback.encode('utf-8')) <= 64:
                profile = p
                break
            # Проверяем, соответствует ли хэш этому профилю
            elif len(test_callback.encode('utf-8')) > 64:
                expected_hash = hashlib.md5(p["name"].encode()).hexdigest()[:8]
                if expected_hash == profile_key:
                    profile = p
                    break
        
        if profile:
            profile_text = profile_bot.format_profile(profile)
            
            # Добавляем кнопку "Назад"
            keyboard = [[InlineKeyboardButton("Назад к списку профилей", callback_data='show_profiles')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Проверяем длину сообщения и разбиваем на части при необходимости
            if len(profile_text) > 4096:  # Лимит Telegram для текста сообщения
                parts = []
                current_part = ""
                for line in profile_text.split("\n"):
                    if len(current_part + line + "\n") <= 4000:  # Оставляем запас на форматирование
                        current_part += line + "\n"
                    else:
                        if current_part:  # Если текущая часть не пустая
                            parts.append(current_part)
                        current_part = line + "\n"
                
                if current_part.strip():  # Добавляем последнюю часть, если она не пустая
                    parts.append(current_part)
                
                try:
                    # Отправляем первую часть с клавиатурой
                    await query.edit_message_text(text=parts[0], parse_mode='Markdown', reply_markup=reply_markup)
                    
                    # Отправляем оставшиеся части как новые сообщения
                    for part in parts[1:]:
                        await query.message.reply_text(text=part, parse_mode='Markdown')
                except Exception:
                    # Если не удалось отредактировать сообщение, отправляем все части как новые сообщения
                    for part in parts:
                        await query.message.reply_text(text=part, parse_mode='Markdown')
                    
                    # Отправляем сообщение с клавиатурой отдельно
                    await query.message.reply_text(text="Выберите действие:", reply_markup=reply_markup)
            else:
                # Если сообщение не длинное, обрабатываем как обычно
                try:
                    # Отправляем информацию о профиле с кнопкой "Назад"
                    await query.edit_message_text(text=profile_text, parse_mode='Markdown', reply_markup=reply_markup)
                except Exception as e:
                    # Если не удалось отредактировать сообщение с клавиатурой, пробуем сначала отредактировать текст
                    try:
                        await query.edit_message_text(text=profile_text, parse_mode='Markdown', reply_markup=None)
                        # Затем отправляем новое сообщение с кнопкой "Назад"
                        await query.message.reply_text(text="Выберите действие:", reply_markup=reply_markup)
                    except Exception:
                        # Если и это не работает, отправляем все в одном новом сообщении
                        await query.message.reply_text(text=profile_text, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            try:
                await query.edit_message_text(text="Профиль не найден.")
            except Exception:
                await query.message.reply_text(text="Профиль не найден.")


# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("profiles", profiles_command))
application.add_handler(CallbackQueryHandler(button_handler))


async def handle(request):
    """Основная функция обработки запросов для Vercel"""
    try:
        # Получаем JSON-данные из тела запроса
        body = await request.json()
        
        # Создаем объект Update из полученных данных
        update = Update.de_json(body)
        
        # Обрабатываем обновление
        # Используем уже созданное приложение
        async with application:
            await application.process_update(update)
        
        # Возвращаем успешный ответ
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "ok"})
        }
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "error", "message": str(e)})
        }


def main():
    """Основная функция для локального тестирования"""
    if not TOKEN:
        print("Ошибка: Необходимо указать токен бота в переменной окружения BOT_TOKEN")
        return

    print("Бот готов к работе с вебхуками на Vercel")


if __name__ == "__main__":
    main()