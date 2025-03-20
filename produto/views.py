from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse

from django.views import View
from django.http import HttpResponse
from . import models
from pprint import pprint

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
    
class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    
class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacaoestoque = variacao.estoque
        produto = variacao.produto

        if variacaoestoque < 1:
            messages.error(self.request, 'Produto sem estoque')
            return redirect(http_referer)  # 🚀 Retorna sem adicionar ao carrinho

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            nova_quantidade = quantidade_carrinho + 1

            if nova_quantidade > variacaoestoque:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {nova_quantidade}x do '
                    f'produto "{produto.nome} {variacao.nome}". Apenas {variacaoestoque}x disponíveis.'
                )
                nova_quantidade = variacaoestoque  # Limita a quantidade ao estoque disponível

            carrinho[variacao_id]['quantidade'] = nova_quantidade
            carrinho[variacao_id]['preco_quantitativo'] = variacao.preco * nova_quantidade
            carrinho[variacao_id]['preco_quantitativo_promocional'] = variacao.preco_promocional * nova_quantidade

            # Apenas exibe a mensagem de sucesso se a quantidade realmente foi aumentada
            if nova_quantidade > quantidade_carrinho:
                messages.success(
                    self.request,
                    f'Produto {produto.nome} {variacao.nome} adicionado ao seu '
                    f'carrinho ({nova_quantidade}x).'
                )

        else:
            carrinho[variacao_id] = {
                'produto_id': produto.id,
                'produto_nome': produto.nome,
                'variacao_nome': variacao.nome or '',
                'variacao_id': variacao_id,
                'preco_unitario': variacao.preco,
                'preco_unitario_promocional': variacao.preco_promocional,
                'preco_quantitativo': variacao.preco,
                'preco_quantitativo_promocional': variacao.preco_promocional,
                'quantidade': 1,
                'slug': produto.slug,
                'imagem': produto.imagem.name if produto.imagem else '',
            }

            messages.success(
                self.request,
                f'Produto {produto.nome} {variacao.nome} adicionado ao seu carrinho (1x).'
            )

        self.request.session.save()
        return redirect(http_referer)

        

class RemoverDoCarrinho(View):
       def get(self, *args, **kwargs):
            http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
            variacao_id = self.request.GET.get('vid')

            if not variacao_id:
                return redirect(http_referer)
            
            if not self.request.session.get('carrinho'):
                return redirect(http_referer)   
            
            if variacao_id not in self.request.session['carrinho']:
                return redirect(http_referer)
            
            carrinho = self.request.session['carrinho'] [variacao_id]
            messages.success(
                self.request,
                f'produto{carrinho["produto_nome"]} {carrinho["variacao_nome"]}' 
                f'removido do carrinho.')
            del self.request.session['carrinho'][variacao_id]
            self.request.session.save()
            return redirect(http_referer)    
        

class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'produto/carrinho.html', contexto)

class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')
