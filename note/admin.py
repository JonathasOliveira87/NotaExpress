from django.contrib import admin
from .models import cNota, selectSetor, OrdemServico

class cNotaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'setor', 'format_numero', 'tag', 'data_criacao']
    search_fields = ['titulo', 'setor']

    def format_numero(self, obj):
        return f"{obj.numero:06d}"

    format_numero.short_description = 'Nota'

admin.site.register(cNota, cNotaAdmin)



admin.site.register(selectSetor)




class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('get_numero_ordem', 'preco_total', 'data_criacao')
    readonly_fields = ('get_numero_ordem',)
    readonly_fields = ['encerrado_por', 'finalizado_por']  # Define os campos como somente leitura
    exclude = ('produto',)

    def get_numero_ordem(self, obj):
        return obj.id_hexadecimal
    get_numero_ordem.short_description = 'Número da Ordem'


admin.site.register(OrdemServico, OrdemServicoAdmin)