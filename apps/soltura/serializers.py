from rest_framework import serializers
from .models import Soltura
from colaboradores.models import Colaborador
from veiculos.models import Veiculo
class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['id', 'modelo', 'prefixo']  
class SolturaSerializer(serializers.ModelSerializer):
    motorista = serializers.PrimaryKeyRelatedField(queryset=Colaborador.objects.filter(tipo="Motorista"))
    tipo_veiculo = VeiculoSerializer(read_only=True)  
    coletores = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Colaborador.objects.filter(tipo=["Coletor", "Operador"])
    )
    motoristas = serializers.SerializerMethodField()
    coletores_lista = serializers.SerializerMethodField()
    operadores_lista = serializers.SerializerMethodField()
    class Meta:
        model = Soltura
        fields = [
            'id', 'motorista', 'tipo_veiculo', 'frequencia', 'setores', 
            'coletores', 'celular', 'lider', 'motoristas', 'coletores_lista', 'operadores_lista'
        ]
    
    def get_motoristas(self, obj):
        return obj.motoristas

    def get_coletores_lista(self, obj):
        return obj.coletores_lista

    def get_operadores_lista(self, obj):
        return obj.operadores_lista
