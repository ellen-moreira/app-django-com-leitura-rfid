from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from app.models import Saida, Animal

print('SIGNALS')

@receiver(m2m_changed, sender=Saida.animais.through)
def update_animal_status(sender, instance, action, **kwargs):
    if action == 'post_add':
        instance.animais.update(status=False)
    elif action == 'post_remove':
        instance.animais.update(status=True)
