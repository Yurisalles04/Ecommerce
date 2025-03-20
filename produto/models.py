"""
Este módulo contém funções e classes relacionadas ao processamento de dados
para o ecommerce. Ele inclui funcionalidades para manipulação de produtos,
carrinho de compras, etc.
"""
from django.conf import settings
from utils import utils
import os
from PIL import Image
from django.db import models
from django.utils.text import slugify



class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Preço promocional')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
         ) # Parênteses corretamente fechados aqui
    )
    
    
    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'
    
    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promocional'
    
    
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        
        if original_width <= new_width:
            print('Retornando largura original menor que nova largura')
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(img_full_path, optimize=True, quality=50)
        
        print('imagem redimensionada')
        
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.nome)}'
            
            
        super().save(*args, **kwargs)
        
        max_image_size = 800
        
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)
            
            
    def __str__(self):
        return self.nome
    
    
class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    
    
    def __str__(self):
        return self.nome or self.produto.nome    
    
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


