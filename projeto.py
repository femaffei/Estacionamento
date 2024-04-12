import datetime

def cadastrar_tarifa(tarifas, tipo_veiculo, valor_base, valor_por_3h, valor_por_hora_extra):
    tarifas[tipo_veiculo] = {'valor_base': valor_base, 'valor_por_3h': valor_por_3h, 'valor_por_hora_extra': valor_por_hora_extra}

def registrar_entrada():
    placa = input("Informe a placa do veículo: ")
    tipo_veiculo = input("Informe o tipo de veículo: ")
    hora_entrada = datetime.datetime.now()
    print("Entrada registrada para", tipo_veiculo, "de placa", placa + ".")
    return {'placa': placa, 'tipo': tipo_veiculo, 'hora_entrada': hora_entrada}

def registrar_saida(veiculo, tarifas, metodo_pagamento):
    hora_saida = datetime.datetime.now()
    tempo_permanencia = hora_saida - veiculo['hora_entrada']
    horas_totais = tempo_permanencia.total_seconds() / 3600

    tipo_veiculo = veiculo['tipo']
    tarifa = tarifas.get(tipo_veiculo)

    if tarifa is None:
        print("Tipo de veículo não cadastrado. Não é possível calcular o valor a pagar.")
        return None

    valor_a_pagar = tarifa['valor_base']
    if horas_totais > 3:
        horas_extras = horas_totais - 3
        valor_a_pagar += tarifa['valor_por_3h'] * (horas_extras // 3) + tarifa['valor_por_hora_extra'] * (horas_extras % 3)

    if metodo_pagamento.lower() == 'pix':
        desconto = valor_a_pagar * 0.05
        valor_a_pagar -= desconto

    print("Saída registrada para", veiculo['tipo'], "de placa", veiculo['placa'] + ".")
    print("Tempo de permanência:", tempo_permanencia)
    print("Valor a pagar:", valor_a_pagar)
    return valor_a_pagar

def gerar_relatorio_diario(entradas, tarifas):
    total_entradas = len(entradas)
    total_saidas = len([veiculo for veiculo in entradas if registrar_saida(veiculo, tarifas, 'dinheiro') is not None])

def gerar_relatorio_por_tipo_veiculo(entradas, tarifas):
    tipos_veiculo = set([veiculo['tipo'] for veiculo in entradas])
    for tipo_veiculo in tipos_veiculo:
        total_veiculos = sum(1 for veiculo in entradas if veiculo['tipo'] == tipo_veiculo)
        valor_total = sum(registrar_saida(veiculo, tarifas, 'dinheiro') or 0 for veiculo in entradas if veiculo['tipo'] == tipo_veiculo)

def exibir_menu():
    print("Opções do Menu:")
    print("1. Cadastrar Tarifas")
    print("2. Registrar Entrada de Veículo")
    print("3. Registrar Saída de Veículo")
    print("4. Gerar Relatório diário")
    print("5. Gerar Relatório por tipo de veículo")
    print("6. Sair")

def main():
    tarifas = {}
    entradas = []
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            tipo_veiculo = input("Informe o tipo de veículo: ")
            valor_base = float(input("Informe o valor base: "))
            valor_por_3h = float(input("Informe o valor por 3 horas: "))
            valor_por_hora_extra = float(input("Informe o valor por hora extra: "))
            cadastrar_tarifa(tarifas, tipo_veiculo, valor_base, valor_por_3h, valor_por_hora_extra)
        elif opcao == '2':
            entradas.append(registrar_entrada())
        elif opcao == '3':
            placa = input("Informe a placa do veículo: ")
            veiculo = next((veiculo for veiculo in entradas if veiculo['placa'] == placa), None)
            if veiculo:
                metodo_pagamento = input("Informe o método de pagamento (PIX, dinheiro, cartão): ")
                registrar_saida(veiculo, tarifas, metodo_pagamento)
                entradas.remove(veiculo)
            else:
                print("Veículo não encontrado.")
        elif opcao == '4':
            gerar_relatorio_diario(entradas, tarifas)
        elif opcao == '5':
            gerar_relatorio_por_tipo_veiculo(entradas, tarifas)
        elif opcao == '6':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
