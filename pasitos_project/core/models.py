from django.db import models

class PerfilAventurero(models.Model):
    AVATAR_CHOICES = [
        ('avatar1', 'Niño Camisa Roja'),
        ('avatar2', 'Niña Trenzas'),
        ('avatar3', 'Niña Cabello Corto'),
        ('avatar4', 'Niño Chaleco Azul'),
    ]

    nombre_usuario = models.CharField(max_length=50)
    edad = models.IntegerField()
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} - {self.edad} años"


class Registro(models.Model):
    # Esto genera automáticamente el INT AUTO_INCREMENT PRIMARY KEY
    id_usuario = models.AutoField(primary_key=True)
    
    # Conectamos el registro con el perfil creado. Si el perfil se borra, el registro se borra (on_delete=models.CASCADE)
    perfil = models.ForeignKey(PerfilAventurero, on_delete=models.CASCADE, related_name='registros')
    
    # Guardamos automáticamente la fecha y hora exacta de la creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro {self.id_usuario} - Perfil: {self.perfil.nombre_usuario} ({self.fecha_creacion})"