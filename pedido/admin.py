from django.contrib import admin
from.import models
# Register your models here.

class ItempedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1
    
class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItempedidoInline]    


admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido)



