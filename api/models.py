from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Cronograma(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.BigIntegerField()

    class Meta:
        db_table = 'public\".\"cronograma'
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
        db_table = 'public\".\"aula'
        verbose_name_plural = 'Aulas'

class Bibliografia(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.BigIntegerField()

    class Meta:
        db_table = 'public\".\"bibliografia'
        verbose_name_plural = 'Bibliografias'

class Usuario(AbstractBaseUser):
    id = models.AutoField(
        primary_key = True
    )

    nome = models.CharField(
        max_length = 250
    )

    email = models.CharField(
        max_length = 250,
        unique = True
    )

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'public\".\"usuario'
        verbose_name_plural = 'Usuarios'

class Turma(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    professor_id = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='professor_id',
    )

    codigo = models.CharField(
        max_length = 250,
        unique = True
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"turma'
        verbose_name_plural = 'Turmas'

class UsuarioTurma(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    usuario_id = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        db_column = 'usuario_id'
    )

    turma_id = models.ForeignKey(
        Turma,
        on_delete = models.CASCADE,
        db_column = 'turma_id'
    )

    tipo = models.IntegerField()

    expulso = models.BooleanField()

    class Meta:
        db_table = 'public\".\"usuario_turma'
        verbose_name_plural = 'Usuario Turmas'

class Topico(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.ForeignKey(
        Turma,
        on_delete = models.CASCADE,
        db_column = 'turma_id'
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"topico'
        verbose_name_plural = 'Topicos'

class Atividade(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.ForeignKey(
        Turma,
        on_delete = models.CASCADE,
        db_column = 'turma_id'
    )

    topico_id = models.ForeignKey(
        Topico,
        on_delete = models.CASCADE,
        db_column = 'topico_id'
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    prazo = models.DateField()

    pontuacao = models.IntegerField()

    class Meta:
        db_table = 'public\".\"atividade'
        verbose_name_plural = 'Atividades'

class Material(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    topico_id = models.ForeignKey(
        Topico,
        on_delete = models.CASCADE,
        db_column = 'topico_id'
    )

    aula_id = models.ForeignKey(
        Aula,
        on_delete = models.CASCADE,
        db_column = 'aula_id'
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"material'
        verbose_name_plural = 'Materiais'

class Duvida(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.ForeignKey(
        Turma,
        on_delete = models.CASCADE,
        db_column = 'turma_id'
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    resolvida = models.BooleanField()

    publicada = models.BooleanField()

    labels = models.CharField(
        max_length = 250
    )

    class Meta:
        db_table = 'public\".\"duvida'
        verbose_name_plural = 'Duvidas'

class RespostaDuvida(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    duvida_id = models.ForeignKey(
        Duvida,
        on_delete = models.CASCADE,
        db_column = 'duvida_id'
    )

    usuario_id = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        db_column = 'usuario_id'
    )

    texto = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"resposta_duvida'
        verbose_name_plural = 'Resposta Duvidas'

class RespostaAtividade(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    usuario_id = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        db_column = 'usuario_id'
    )

    nota = models.PositiveIntegerField()

    data_envio = models.DateField()

    envio_confirmado = models.BooleanField()

class Anexo(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    material_id = models.ForeignKey(
        Material,
        on_delete = models.CASCADE,
        db_column = 'material_id'
    )

    atividade_id = models.ForeignKey(
        Atividade,
        on_delete = models.CASCADE,
        db_column = 'atividade_id'
    )

    resposta_atividade_id = models.ForeignKey(
        RespostaAtividade,
        on_delete = models.CASCADE,
        db_column = 'resposta_atividade_id'
    )

    url = models.CharField(
        max_length = 1000
    )

    class Meta:
        db_table = 'public\".\"anexos'
        verbose_name_plural = 'Anexos'

class Aviso(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    turma_id = models.ForeignKey(
        Turma,
        on_delete = models.CASCADE,
        db_column = 'turma_id'
    )

    usuario_id = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        db_column = 'usuario_id'
    )

    titulo = models.CharField(
        max_length = 250
    )

    descricao = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"aviso'
        verbose_name_plural = 'Avisos'

class ComentarioAviso(models.Model):
    id = models.AutoField(
        primary_key = True
    )

    aviso_id = models.ForeignKey(
        Aviso,
        on_delete = models.CASCADE,
        db_column = 'aviso_id'
    )

    usuario_id = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        db_column = 'usuario_id'
    )

    texto = models.CharField(
        max_length = 700
    )

    class Meta:
        db_table = 'public\".\"comentario_aviso'
        verbose_name_plural = 'Comentario Avisos'

