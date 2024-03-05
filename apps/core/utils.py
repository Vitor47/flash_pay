# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from itertools import cycle

import requests
from django.utils.translation import gettext_lazy as _

TAMANHO_CPF = 11


def is_cpf_valid(cpf: str) -> bool:
    if len(cpf) != TAMANHO_CPF:
        return False

    if cpf in (c * TAMANHO_CPF for c in "1234567890"):
        return False

    cpf_reverso = cpf[::-1]
    for i in range(2, 0, -1):
        cpf_enumerado = enumerate(cpf_reverso[i:], start=2)
        dv_calculado = (
            sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
        )
        if cpf_reverso[i - 1 : i] != str(dv_calculado % 10):
            return False

    return True


LENGTH_CNPJ = 14


def is_cnpj_valid(cnpj: str) -> bool:
    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1 : i] != str(dv % 10):
            return False

    return True


def is_email_valid(email: str) -> bool:
    res = re.search(r"^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,3}$", email)
    if res is None:
        return False

    return True


def format_cpf_cnpj(cpf_cnpj: str) -> str:
    if len(cpf_cnpj) == 11:
        # Formatar CPF
        return f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
    elif len(cpf_cnpj) == 14:
        # Formatar CNPJ
        return f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"

    return cpf_cnpj


def format_cpf(cpf: str) -> str:
    return "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


def validate_ibge_code(ibge_code: str) -> bool:
    if not re.match(r"^\d{7}$", ibge_code):
        return False

    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{ibge_code}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def only_numbers(string: str) -> str:
    return re.sub(r"[^0-9]", "", string)


def is_valid_cep(cep: str) -> bool:
    if not re.match(r"\d{8}", cep):
        return False

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if "erro" not in data:
            return True

    return False


def translate_permissions(obj: str) -> str:
    permissions_translated = [
        _(w)
        .replace("Can", "Pode")
        .replace("add", "adicionar")
        .replace("change", "alterar")
        .replace("delete", "excluir")
        .replace("view", "visualizar")
        for w in (obj).split()
    ]
    return " ".join(permissions_translated)


def is_password_valid(password):
    if len(password) < 8:
        return False

    if re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
        return True
    return False
