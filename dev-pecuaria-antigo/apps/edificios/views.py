from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
import calendar
from datetime import datetime, timedelta
    
# Restrição de acesso com base em grupos de usuários (utiliza função)
from django.contrib.auth.decorators import user_passes_test, login_required

# Função que verifica se o usuário é membro do grupo Edificios
def is_edificios_member(user):
    return user.groups.filter(name='Edificios').exists() or user.is_superuser

@login_required # Restrição de acesso com base em login
@user_passes_test(is_edificios_member) # Só permite o acesso se o usuário for membro do grupo Edificios
def index_base(request):
    context = {}
    return render(request, "index_base.html", context)

# INFORMÁTICA
@login_required
@user_passes_test(is_edificios_member)
def salas_tecnologia_informacao(request):
    # Suponha que 'Tecnologia da Informação' é o nome do prédio
    predio_ti = Building.objects.get(name='Tecnologia da Informação')

    # Filtrar as salas do prédio de Tecnologia da Informação que podem ser reservadas
    salas_ti_reservaveis = Room.objects.filter(building=predio_ti, can_be_reserved=True)

    dias_semana = DayOfWeek.objects.all()
    
    horasM = ManageShift.objects.filter(shift=Shift.objects.get(shift="Matutino"))
    horasV = ManageShift.objects.filter(shift=Shift.objects.get(shift="Vespertino"))
    horasN = ManageShift.objects.filter(shift=Shift.objects.get(shift="Noturno"))
    today = datetime.today()
    year = today.year
    month = today.month

    # Gere as datas para o mês atual
    _, last_day = calendar.monthrange(year, month)
    first_date = datetime(year, month, 1)
    last_date = datetime(year, month, last_day)

    # Lista de datas separadas em períodos de 5 dias
    date_range = []
    current_date = first_date
    while current_date <= last_date:
        if current_date.weekday() < 5:  # Verifica se é um dia de semana (segunda a sexta-feira)
            date_range.append(current_date)
        current_date += timedelta(days=1)

    

    # Agora, você pode usar as salas de Tecnologia da Informação que podem ser reservadas, os dias da semana e as horas como necessário
    context = {
        'salas_ti_reservaveis': salas_ti_reservaveis,
        'nome_predio': predio_ti,
        'date_range': date_range,
        'dias_semana': dias_semana,
        'horasM': horasM,
        'horasV': horasV,
        'horasN': horasN,
    }
    return render(request, 'dashboard_info.html', context)


def Allocation_Info(request):
    if request.method == 'POST':
        try:
            room_allocation = RoomAllocation()
            room_allocation.building = request.POST.get('predio')
            room_allocation.number_rooms = request.POST.get('numero')
            room_allocation.data = request.POST.get('data')
            room_allocation.start_time = request.POST.get('entrada')
            room_allocation.end_time = request.POST.get('saida')
            room_allocation.name_allocation = request.POST.get('nomeAlocacao')
            room_allocation.grade = request.POST.get('nomeTurma')
            room_allocation.discipline = request.POST.get('nomeDisciplina')

            # Adicione logs para verificar os valores dos campos
            print(f"Building: {room_allocation.building}")
            print(f"Number Rooms: {room_allocation.number_rooms}")
            print(f"Data: {room_allocation.data}")
            print(f"Start Time: {room_allocation.start_time}")
            print(f"End Time: {room_allocation.end_time}")
            print(f"Name Allocation: {room_allocation.name_allocation}")
            print(f"Grade: {room_allocation.grade}")
            print(f"Discipline: {room_allocation.discipline}")

            # Verificar se todos os campos obrigatórios estão presentes
            if None in [room_allocation.building, room_allocation.number_rooms, room_allocation.data,
                        room_allocation.start_time, room_allocation.end_time, room_allocation.name_allocation,
                        room_allocation.grade, room_allocation.discipline]:
                raise ValueError("Todos os campos devem ser preenchidos.")

            room_allocation.save()
            print("Alocação bem-sucedida.")
        except ValueError as ve:
            print(f"Erro ao alocar sala: {ve}")
            return JsonResponse({'success': False, 'error': f"Erro ao alocar sala: {ve}"}, status=400)
        except IntegrityError as ie:
            print(f"Erro de integridade: {ie}")
            return JsonResponse({'success': False, 'error': f"Erro de integridade: {ie}"}, status=400)
        except Exception as e:
            print(f"Erro desconhecido ao alocar sala: {e}")
            return JsonResponse({'success': False, 'error': f"Erro ao alocar sala: {e}"}, status=400)

    alocacoes = {
        'alocacoes': RoomAllocation.objects.all()
    }
    return render(request, 'dashboard_info.html', alocacoes)



# VETERINÁRIA
@login_required
@user_passes_test(is_edificios_member)
def salas_vet(request):
    # Suponha que 'Tecnologia da Informação' é o nome do prédio
    predio_vet = Building.objects.get(name='Medicina Veterinária')

    # Filtrar as salas do prédio de Tecnologia da Informação que podem ser reservadas
    salas_veterinaria_reservaveis = Room.objects.filter(building=predio_vet, can_be_reserved=True)

    dias_semana = DayOfWeek.objects.all()
    
    horasM = ManageShift.objects.filter(shift=Shift.objects.get(shift="Matutino"))
    horasV = ManageShift.objects.filter(shift=Shift.objects.get(shift="Vespertino"))
    horasN = ManageShift.objects.filter(shift=Shift.objects.get(shift="Noturno"))
    today = datetime.today()
    year = today.year
    month = today.month

    # Gere as datas para o mês atual
    _, last_day = calendar.monthrange(year, month)
    first_date = datetime(year, month, 1)
    last_date = datetime(year, month, last_day)

    # Lista de datas separadas em períodos de 5 dias
    date_range = []
    current_date = first_date
    while current_date <= last_date:
        if current_date.weekday() < 5:  # Verifica se é um dia de semana (segunda a sexta-feira)
            date_range.append(current_date)
        current_date += timedelta(days=1)

    

    # Agora, você pode usar as salas de Tecnologia da Informação que podem ser reservadas, os dias da semana e as horas como necessário
    context = {
        'salas_veterinaria_reservaveis': salas_veterinaria_reservaveis,
        'nome_predio': predio_vet,
        'date_range': date_range,
        'dias_semana': dias_semana,
        'horasM': horasM,
        'horasV': horasV,
        'horasN': horasN,
    }
    return render(request, 'dashboard_veterinaria.html', context)


def Allocation_Vet(request):
    if request.method == 'POST':
        try:
            room_allocation = RoomAllocation()
            room_allocation.building = request.POST.get('predio')
            room_allocation.number_rooms = request.POST.get('numero')
            room_allocation.data = request.POST.get('data')
            room_allocation.start_time = request.POST.get('entrada')
            room_allocation.end_time = request.POST.get('saida')
            room_allocation.name_allocation = request.POST.get('nomeAlocacao')
            room_allocation.grade = request.POST.get('nomeTurma')
            room_allocation.discipline = request.POST.get('nomeDisciplina')

            # Verificar se todos os campos obrigatórios estão presentes
            if None in [room_allocation.building, room_allocation.number_rooms, room_allocation.data,
                        room_allocation.start_time, room_allocation.end_time, room_allocation.name_allocation,
                        room_allocation.grade, room_allocation.discipline]:
                raise ValueError("Todos os campos devem ser preenchidos.")

            room_allocation.save()
            print("Alocação bem-sucedida.")
            return redirect('dashboard_veterinaria')
        except ValueError as ve:
            print(f"Erro ao alocar sala: {ve}")
            return HttpResponse(f"Erro ao alocar sala: {ve}")
        except IntegrityError as ie:
            print(f"Erro de integridade: {ie}")
            return HttpResponse(f"Erro de integridade: {ie}")
        except Exception as e:
            print(f"Erro desconhecido ao alocar sala: {e}")
            return HttpResponse(f"Erro desconhecido ao alocar sala: {e}")

    alocacoes = {
        'alocacoes': RoomAllocation.objects.all()
    }
    return render(request, 'dashboard_veterinaria.html', alocacoes)

# PRÉDIO H
@login_required
@user_passes_test(is_edificios_member)
def salas_predio_h(request):
    # Suponha que 'Tecnologia da Informação' é o nome do prédio
    predio_h = Building.objects.get(name='Prédio H')

    # Filtrar as salas do prédio de Tecnologia da Informação que podem ser reservadas
    salas_H_reservaveis = Room.objects.filter(building=predio_h, can_be_reserved=True)

    dias_semana = DayOfWeek.objects.all()
    
    horasM = ManageShift.objects.filter(shift=Shift.objects.get(shift="Matutino"))
    horasV = ManageShift.objects.filter(shift=Shift.objects.get(shift="Vespertino"))
    horasN = ManageShift.objects.filter(shift=Shift.objects.get(shift="Noturno"))
    today = datetime.today()
    year = today.year
    month = today.month

    # Gere as datas para o mês atual
    _, last_day = calendar.monthrange(year, month)
    first_date = datetime(year, month, 1)
    last_date = datetime(year, month, last_day)

    # Lista de datas separadas em períodos de 5 dias
    date_range = []
    current_date = first_date
    while current_date <= last_date:
        if current_date.weekday() < 5:  # Verifica se é um dia de semana (segunda a sexta-feira)
            date_range.append(current_date)
        current_date += timedelta(days=1)

    

    # Agora, você pode usar as salas de Tecnologia da Informação que podem ser reservadas, os dias da semana e as horas como necessário
    context = {
        'salas_H_reservaveis': salas_H_reservaveis,
        'nome_predio': predio_h,
        'date_range': date_range,
        'dias_semana': dias_semana,
        'horasM': horasM,
        'horasV': horasV,
        'horasN': horasN,
    }
    return render(request, 'dashboard_predioh.html', context)

@login_required
@user_passes_test(is_edificios_member)
def create_room_allocation(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        name_allocation = request.POST.get('name_allocation')
        grade = request.POST.get('grade')
        discipline = request.POST.get('discipline')

        room_allocation = RoomAllocation(
            data=data,
            start_time=start_time,
            end_time=end_time,
            name_allocation=name_allocation,
            grade=grade,
            discipline=discipline
        )
        room_allocation.save()
        return redirect('sucesso')  # Redirecione para uma página de sucesso

    return render(request, 'dashboard_info.html')

@login_required
@user_passes_test(is_edificios_member)
def generate_time_slots(self):
        start_time = datetime.time(7, 0)  # Horário de início (7:00 da manhã)
        end_time = datetime.time(22, 0)   # Horário de término (22:00 à noite)
        time_slots = []

        if self.number_of_slots <= 0:
            return []

        total_minutes = (end_time.hour - start_time.hour) * 60
        slot_duration = total_minutes / self.number_of_slots

        for i in range(self.number_of_slots):
            minutes = int(i * slot_duration)
            hours = minutes // 60
            minutes %= 60
            time_slot = (start_time.replace(hour=start_time.hour + hours, minute=start_time.minute + minutes))
            time_slots.append(time_slot.strftime("%H:%M"))

        return time_slots


@login_required
@user_passes_test(is_edificios_member)
def Allocation(request):
    if request.method == 'POST':
        try:
            room_allocation = RoomAllocation()
            room_allocation.building = request.POST.get('predio')
            room_allocation.number_rooms = request.POST.get('numero')
            room_allocation.data = request.POST.get('data')
            room_allocation.start_time = request.POST.get('entrada')
            room_allocation.end_time = request.POST.get('saida')
            room_allocation.name_allocation = request.POST.get('nomeAlocacao')
            room_allocation.grade = request.POST.get('nomeTurma')
            room_allocation.discipline = request.POST.get('nomeDisciplina')

            # Verificar se todos os campos obrigatórios estão presentes
            if None in [room_allocation.building, room_allocation.number_rooms, room_allocation.data,
                        room_allocation.start_time, room_allocation.end_time, room_allocation.name_allocation,
                        room_allocation.grade, room_allocation.discipline]:
                raise ValueError("Todos os campos devem ser preenchidos.")

            room_allocation.save()
            print("Alocação bem-sucedida.")
            return redirect('dashboard_predioh')
        except ValueError as ve:
            print(f"Erro ao alocar sala: {ve}")
            return JsonResponse({'success': False, 'error': f"Erro ao alocar sala: {ve}"}, status=400)
        except IntegrityError as ie:
            print(f"Erro de integridade: {ie}")
            return JsonResponse({'success': False, 'error': f"Erro ao alocar sala: {ve}"}, status=400)
        except Exception as e:
            print(f"Erro desconhecido ao alocar sala: {e}")
            return JsonResponse({'success': False, 'error': f"Erro ao alocar sala: {ve}"}, status=400)

    alocacoes = {
        'alocacoes': RoomAllocation.objects.all()
    }
    return render(request, 'dashboard_info.html', alocacoes)

def generate_time_slots(self):
        start_time = datetime.time(7, 0)  # Horário de início (7:00 da manhã)
        end_time = datetime.time(22, 0)   # Horário de término (22:00 à noite)
        time_slots = []

        if self.number_of_slots <= 0:
            return []

        total_minutes = (end_time.hour - start_time.hour) * 60
        slot_duration = total_minutes / self.number_of_slots

        for i in range(self.number_of_slots):
            minutes = int(i * slot_duration)
            hours = minutes // 60
            minutes %= 60
            time_slot = (start_time.replace(hour=start_time.hour + hours, minute=start_time.minute + minutes))
            time_slots.append(time_slot.strftime("%H:%M"))

        return time_slots
    


def amem(request):
    # Suponha que 'Tecnologia da Informação' é o nome do prédio
    predio_ti = Building.objects.get(name='Tecnologia da Informação')

    # Filtrar as salas do prédio de Tecnologia da Informação que podem ser reservadas
    amemm = Room.objects.filter(building=predio_ti, can_be_reserved=True)

    dias_semana = DayOfWeek.objects.all()
    
    horasM = ManageShift.objects.filter(shift=Shift.objects.get(shift="Matutino"))
    horasV = ManageShift.objects.filter(shift=Shift.objects.get(shift="Vespertino"))
    horasN = ManageShift.objects.filter(shift=Shift.objects.get(shift="Noturno"))
    today = datetime.today()
    year = today.year
    month = today.month

    # Gere as datas para o mês atual
    _, last_day = calendar.monthrange(year, month)
    first_date = datetime(year, month, 1)
    last_date = datetime(year, month, last_day)

    # Lista de datas separadas em períodos de 5 dias
    date_range = []
    current_date = first_date
    while current_date <= last_date:
        if current_date.weekday() < 5:  # Verifica se é um dia de semana (segunda a sexta-feira)
            date_range.append(current_date)
        current_date += timedelta(days=1)

    

    # Agora, você pode usar as salas de Tecnologia da Informação que podem ser reservadas, os dias da semana e as horas como necessário
    context = {
        'amemm': amemm,
        'nome_predio': predio_ti,
        'date_range': date_range,
        'dias_semana': dias_semana,
        'horasM': horasM,
        'horasV': horasV,
        'horasN': horasN,
    }
    return render(request, 'amem.html', context)
