from datetime import date, timedelta

def get_request_priority(request_type):
    if request_type == "Прорыв трубы" or request_type == "Нет отопления":
        return "Критический"
    elif request_type == "Неисправность розетки" or request_type == "Капающий кран":
        return "Средний"
    else:
        return "Низкий"

def calculate_deadline(priority, current_date):
    if priority == "Критический":
        deadline = current_date + timedelta(hours=2)
        return f"В течение 2 часов (до {deadline})"
    elif priority == "Средний":
        deadline = current_date + timedelta(days=3)
        return f"В течение 3 дней (до {deadline})"
    else:
        deadline = current_date + timedelta(days=7)
        return f"В течение 7 дней (до {deadline})"

def generate_request_card(tenant_name, flat_number, request_type, is_urgent):
    priority = get_request_priority(request_type)
    
    base_cost = 500.0
    if is_urgent:
        final_cost = base_cost * 1.5
    else:
        final_cost = base_cost
        
    today = date.today()
    deadline_info = calculate_deadline(priority, today)
    
    card = "--- КАРТОЧКА ЗАЯВКИ ---\n"
    card += f"Жилец: {tenant_name}\n"
    card += f"Квартира: {str(flat_number)}\n" 
    card += f"Проблема: {request_type}\n"
    card += f"Приоритет: {priority}\n"
    card += f"Срок выполнения: {deadline_info}\n"
    card += f"Предв. стоимость: {final_cost} руб.\n"
    card += "------------------------"
    return card

if __name__ == "__main__":
    print("Система управления заявками жильцов. Создание новой заявки.")
    
    name = input("Введите ФИО жильца: ")
    flat = int(input("Введите номер квартиры: "))
    problem = input("Опишите проблему (например, 'Прорыв трубы'): ")
    urgent_input = input("Требуется срочный выезд? (да/нет): ")
    
    is_urgent = True if urgent_input.lower() == "да" else False
    
    request_card = generate_request_card(name, flat, problem, is_urgent)
    print("\n" + request_card)