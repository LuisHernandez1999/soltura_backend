from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
from .models import Soltura
from colaboradores.models import Colaboradores
from veiculos.models import Veiculo

@csrf_exempt
@require_GET
def listar_colaboradores(request):
    try:
        _ = request  
        motoristas = list(Colaboradores.objects.filter(tipo="Motorista").values_list("nome", flat=True))
        coletores = list(Colaboradores.objects.filter(tipo="Coletor").values_list("nome", flat=True))
        operadores = list(Colaboradores.objects.filter(tipo="Operador").values_list("nome", flat=True))

        return JsonResponse({
            "motoristas": motoristas,
            "coletores": coletores,
            "operadores": operadores
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_POST
def criar_soltura(request):
    try:
        data = json.loads(request.body)
        motorista = Colaboradores.objects.filter(nome=data.get("motorista"), tipo="Motorista").first()
        if not motorista:
            return JsonResponse({"error": "Motorista não encontrado ou inválido."}, status=400)
        veiculo = Veiculo.objects.filter(modelo=data.get("prefixo")).first()
        if not veiculo:
            return JsonResponse({"error": "Veículo não encontrado."}, status=400)
        nomes_coletores = data.get("coletores", [])
        nomes_operadores = data.get("operadores", [])
        coletores = list(Colaboradores.objects.filter(nome__in=nomes_coletores, tipo="Coletor"))
        operadores = list(Colaboradores.objects.filter(nome__in=nomes_operadores, tipo="Operador"))
        nomes_enviados = set(nomes_coletores + nomes_operadores)
        nomes_encontrados = {c.nome for c in coletores + operadores}
        nomes_faltando = nomes_enviados - nomes_encontrados
        if nomes_faltando:
            return JsonResponse({"error": f"os seguintes colaboradores nao foram encontrados: {list(nomes_faltando)}"}, status=400)
        soltura = Soltura.objects.create(
            motorista=motorista,
            tipo_veiculo=veiculo,
            frequencia=data.get("frequencia", "Diária"),
            setores=data.get("setores", ""),
            celular=data.get("celular", ""),
            lider=data.get("lider", "")
        )
        soltura.coletores.set(coletores + operadores)
        return JsonResponse({
            "message": "soltura criada com sucesso",
            "motorista": motorista.nome,
            "veiculo": veiculo.prefixo,
            "frequencia": soltura.frequencia,
            "setores": soltura.setores,
            "celular": soltura.celular,
            "lider": soltura.lider,
            "coletores": [c.nome for c in coletores],
            "operadores": [o.nome for o in operadores]
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Erro ao decodificar JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
