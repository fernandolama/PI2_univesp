from django.contrib import admin
from .models import Cliente, PedidoImpressao, OrcamentoEvento

admin.site.register(Cliente)
admin.site.register(PedidoImpressao)
admin.site.register(OrcamentoEvento)
