from django.db import models
from django.utils import formats




class Corridor(models.Model):
    number = models.CharField(max_length=45, unique=True, verbose_name="Número")

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = "Corredor"
        verbose_name_plural = "Corredores"




class Institution(models.Model):
    name = models.CharField(max_length=45, unique=True, verbose_name="Nome")
    city = models.CharField(max_length=45, unique=True, verbose_name="Cidade")

    def __str__(self):
        return f" {self.name} -  {self.city}"

    class Meta:
        ordering = ['name']
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"


class Unit(models.Model):
     name = models.CharField(max_length=45, unique=True, verbose_name="Nome")
     city = models.CharField(max_length=45, unique=True, verbose_name="Cidade")
     institution = models.ForeignKey(Institution, on_delete=models.CASCADE,verbose_name="Instituição" )
     def __str__(self):
        return f" {self.name} - {self.city}"
     class Meta:
        ordering = ['institution']
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
    



        
        
class Floor(models.Model):
    name = models.CharField(max_length=45, unique=True, verbose_name="Nome")
    room_count = models.IntegerField(verbose_name="Quantidade de Salas")
    bathroom_count = models.IntegerField(verbose_name="Quantidade de Banheiros")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"

class Shift(models.Model):
    shift_choices = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
        ('Madrugada', 'Madrugada'),
    ]
    shift = models.CharField(max_length=50, choices=shift_choices, unique=True, verbose_name="Turno")

    def __str__(self):
        return self.shift

    class Meta:
        ordering = ['shift']
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

class ManageShift(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, verbose_name="Turno")
    start_time = models.TimeField(verbose_name="Hora de Início")
    end_time = models.TimeField(verbose_name="Hora de Fim")

    def __str__(self):
        return f"{self.shift}: {self.start_time} - {self.end_time}"

    class Meta:
        ordering = ['start_time']
        verbose_name = "Gerenciar Turno"
        verbose_name_plural = "Gerenciar Turnos"

class DayOfWeek(models.Model):
    day_name = models.CharField(max_length=20, verbose_name="Nome do Dia")
    order = models.PositiveIntegerField(verbose_name="Ordem do Dia")

    def __str__(self):
        return self.day_name

    class Meta:
        ordering = ['order']
        verbose_name = " Dia da Semana"
        verbose_name_plural = "Dias da Semana"

class Building(models.Model):
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE, verbose_name="Instituição")
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE, verbose_name="Unidade")
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    inauguration_date = models.DateField(verbose_name="Data de Inauguração")
    latitude = models.CharField(max_length=50, verbose_name="Latitude")
    longitude = models.CharField(max_length=50, verbose_name="Longitude")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="Piso")
    corridor = models.ForeignKey(Corridor, on_delete=models.CASCADE, verbose_name="Corredor")
    number_of_slots = models.PositiveIntegerField(verbose_name="Número de Horários")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Edifício"
        verbose_name_plural = "Edifícios"

class RoomType(models.Model):
    type_name = models.CharField(max_length=50, unique=True, verbose_name="Tipo")

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']
        verbose_name = "Tipo de Sala"
        verbose_name_plural = "Tipos de Sala"

class RoomStatus(models.Model):
    status_name = models.CharField(max_length=50, unique=True, verbose_name="Status")

    def __str__(self):
        return self.status_name

    class Meta:
        ordering = ['status_name']
        verbose_name = "Status da Sala"
        verbose_name_plural = "Status das Salas"

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="Prédio")
    number = models.CharField(max_length=3, verbose_name="Número")
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="Tipo")
    seats = models.IntegerField(verbose_name="Assentos")
    color = models.CharField(max_length=30, verbose_name="Cor", default="bg-success")
    can_be_reserved = models.BooleanField(default=True, verbose_name="Pode ser reservada")
  

    def __str__(self):
         return f" Prédio: {self.building} - Sala: {self.number} - Tipo: {self.type} - Assentos: {self.seats}"

    class Meta:
        ordering = ['building']
        verbose_name = "Sala"
        verbose_name_plural = "Salas"

class RoomAllocation(models.Model):
    building = models.CharField(max_length=55, verbose_name="Prédio", null=False, blank=False)
    number_rooms = models.CharField(max_length=55, verbose_name="Número Sala", null=False, blank=False)
    data = models.DateField(verbose_name="Data", null=False, blank=False)
    start_time = models.TimeField(verbose_name="Entrada", null=False, blank=False)
    end_time = models.TimeField(verbose_name="Saída", null=False, blank=False)
    name_allocation = models.CharField(max_length=100, verbose_name="Nome de quem irá alocar", null=False, blank=False)
    grade = models.CharField(max_length=100, verbose_name="Turma", null=False, blank=False)
    discipline = models.CharField(max_length=100, verbose_name="Disciplina", null=False, blank=False)

    def __str__(self):
        formatted_date = self.data.strftime('%d-%m-%Y')
        return f"Prédio: {self.building} | Sala: {self.number_rooms} | Data: {formatted_date} | Entrada: {self.start_time} | Saída: {self.end_time} | Alocado para: {self.name_allocation} | Turma: {self.grade} | Disciplina: {self.discipline}"

    class Meta:
        ordering = ['data']
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"