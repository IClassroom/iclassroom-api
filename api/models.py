from django.db import models

class Cronograma(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.IntegerField()

    class Meta:
        db_table = 'iclassroom\".\"cronograma'
        verbose_name_plural = 'Cronogromas'

class Aula(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    cronograma_id = models.ForeignKey(
        Cronograma, 
        on_delete = models.CASCADE,
        db_column = 'cronograma_id'
    )

    dia = models.DateField()

    titulo = models.CharField(
        max_length = 250
    )

    assuntos = models.CharField(
        max_length = 500
    )

    descricao = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'iclassroom\".\"aula'
        verbose_name_plural = 'Aulas'