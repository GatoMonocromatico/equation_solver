import re


class Solver():
    def __init__(self, conta=""):
        conta.replace(" ", "")
        self.eqc = {f"membro1": conta.split("=")[0],
                    f"membro2": conta.split("=")[1]}
        self.formata_equacao()
        self.resultado = f"{self.eqc['membro1']} = {self.eqc['membro2']}"
        self.conta = conta
        # self.resolve_membros()

    def retorna_resultado(self):
        return self.resultado + "\n"

    def retorna_conta(self):
        return self.conta + "\n"

    def define_membro_x_membro_num(self):
        padrao_tem_numero = re.compile(r"\d")
        padroes_multiplicando_dividindo_x = (re.compile(r"[\d.]+[*/]x"), re.compile(r"x[*/][\d.]+"))
        if "x" in str(self.eqc["membro1"]):
            lista_termos_x = []

            for termo in self.eqc["membro1"]:
                if "x" in termo:
                    lista_termos_x.append(termo)

            while lista_termos_x:
                termo = lista_termos_x.pop(0)
                self.troca_termo_de_membro(termo, "membro1", "membro2")

        if re.search(padrao_tem_numero, str(self.eqc["membro2"])):
            padrao_termo_num = re.compile(r"[+-]\d+\.?\d*")
            lista_termos_num = []

            for termo in self.eqc["membro2"]:
                if re.fullmatch(padrao_termo_num, termo):
                    lista_termos_num.append(termo)

            print(lista_termos_num)
            while lista_termos_num:
                termo = lista_termos_num.pop(0)
                self.troca_termo_de_membro(termo, "membro2", "membro1")

    def troca_termo_de_membro(self, termo, membro_atual, membro_para_passar, manter_parte=False):
        operacoes = self.define_operacao(termo)

        if operacoes["atual"] not in ["*", "/"]:
            self.eqc[membro_atual].remove(termo)
            self.eqc[membro_para_passar].append(termo.replace(operacoes["atual"], operacoes["inversa"]))
        else:
            padroes = (re.compile(r"([+-]?x)([/*][+-]?\d+\.?\d*)"), re.compile(r"([+-]?\d+\.?\d*[/*])([+-]?x)"))
            index = 0
            for padrao in padroes:
                procura = re.search(padrao, termo)
                if procura:
                    if index == 0:
                        incognita = procura.groups()[0]
                        numero = procura.groups()[1]
                    else:
                        incognita = procura.groups()[1]
                        numero = procura.groups()[0]
                    break
                index += 1
            index = 0
            for item in self.eqc[membro_atual]:
                if item == termo:
                    break
                index += 1

            if membro_atual == "membro1":
                if manter_parte:
                    self.eqc[membro_atual][index] = f"{operacoes['sinal']}{numero.replace(operacoes['atual'], '')}"
                    self.eqc[membro_para_passar].append(f"{operacoes['inversa']}{incognita}")
                else:
                    self.eqc[membro_atual].remove(termo)
                    self.eqc[membro_para_passar].append(f"{operacoes['sinal_inverso']}{termo.replace(operacoes['sinal'], '')}")
            else:
                if manter_parte:
                    self.eqc[membro_atual][index] = incognita
                    self.eqc[membro_para_passar].append(f"{numero.replace(operacoes['atual'], operacoes['inversa'])}")
                else:
                    self.eqc[membro_atual].remove(termo)
                    self.eqc[membro_para_passar].append(f"{operacoes['sinal_inverso']}{termo.replace(operacoes['atual'], '')}")


    def define_operacao(self, termo):
        if termo[0] == "-":
            sinal, sinal_inverso, atual, inv = "-", "+", "-", "+"

        else:
            sinal, sinal_inverso, atual, inv = "+", "-", "+", "-"

        if "*" in termo:
            inv, atual = "/", "*"
        elif "/" in termo:
            inv, atual = "*", "/"

        return {"inversa": inv, "atual": atual, "sinal": sinal, "sinal_inverso": sinal_inverso}

    def formata_equacao(self):
        for membro in self.eqc:
            self.define_termos(membro)
        print(self.eqc['membro1'], "=", self.eqc['membro2'])

        self.define_membro_x_membro_num()
        print(self.eqc['membro1'], "=", self.eqc['membro2'])

        index = 0
        for termo in self.eqc["membro2"][:]:
            self.eqc["membro2"][index] = termo.replace("x", "1")

            index += 1

        self.resolve_membros()

    def resolve_membros(self):
        print("resolve_membros")
        print(self.eqc['membro1'], "=", self.eqc['membro2'])

        for membro in self.eqc:
            resultado = 0
            for termo in self.eqc[membro]:
                if "*" in termo or "/" in termo:
                    self.define_termos(membro)
                    self.resolve_membros()
                    return ""
                else:
                    resultado += float(termo)

            self.eqc[membro] = [f"{resultado}", ]

        if self.eqc["membro2"] != 1:
            valor = f"{self.eqc['membro2'][0]}*x"
            print(valor)
            self.eqc["membro2"] = [valor,]
            self.troca_termo_de_membro(valor, "membro2", "membro1", True)

            self.eqc["membro1"] = self.resolve_divisao(self.eqc["membro1"][0], self.eqc["membro1"][1])

        self.eqc["membro2"] = "x"

        print(self.eqc['membro1'], "=", self.eqc['membro2'])

    def define_termos(self, membro):
        print("definindo termos")
        self.some_termos_multiplicando_dividindo(membro)

        termos = self.eqc[membro].split("-")
        index = 0
        for termo in termos[:]:
            print(termo, "<= termo, todos os termos ->", termos)
            if index == 0:
                if len(termos) > 1:
                    termo = str(termo).replace('"[', '').replace(']"', '')
                if termo != "":
                    if termo[0] not in ["+", "-"]:
                        termos[0] = f"+{termo}"
            else:
                termo = f"-{termo}"
                termos[index] = termo
            index += 1

        padrao_termos_agrupados = re.compile(r"[-+][\dx]+")
        termos.reverse()
        for termo in termos[:]:
            if re.fullmatch(padrao_termos_agrupados, termo):
                termos.remove(termo)
                termos.insert(0, termo)
            else:
                termos.remove(termo)
                for item in termo.split("+"):
                    if item != "":
                        if item[0] not in ["+", "-"]:
                            item = f"+{item}"
                        termos.insert(0, item)
        index = 0
        for termo in termos:
            termos[index] = termo
            index += 1

        self.eqc[membro] = termos

    def resolve_multiplicacao(self, numeros):
        resultado = 1
        for numero in numeros:
            resultado = resultado * float(numero)
        return resultado

    def resolve_divisao(self, numerador, denominador):
        return float(numerador)/float(denominador.replace("/", ""))

    def some_termos_multiplicando_dividindo(self, membro_do_termo):
        padrao_multiplicacao_divisao = re.compile(r"[+-]?[\d.]+[*/][+-]?[\d.]+")

        membro = str(self.eqc[membro_do_termo]).replace("[", "").replace("]", "").replace("'", "").replace(",", "")

        termo_formatar = re.search(padrao_multiplicacao_divisao, membro)

        while termo_formatar:
            termo = termo_formatar.group()
            eh_multiplicacao = True if "*" in termo else False

            if eh_multiplicacao:
                numeros = termo.split("*")
                resultado = self.resolve_multiplicacao(numeros)
            else:
                numerador, denominador = termo.split("/")[0], termo.split("/")[1]
                resultado = self.resolve_divisao(numerador, denominador)

            membro = membro.replace(termo, str(resultado))
            self.eqc[membro_do_termo] = membro

            termo_formatar = re.search(padrao_multiplicacao_divisao, membro)

        self.eqc[membro_do_termo] = membro


#solucionador = Solver("62*x=7123+611-3*6-x/2")
