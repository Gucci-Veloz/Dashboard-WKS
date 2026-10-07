import json

from app.seguridad import sesion


def _cuentas(monkeypatch, tmp_path, datos):
    ruta = tmp_path / "works_cuentas.json"
    ruta.write_text(json.dumps(datos), encoding="utf-8")
    monkeypatch.setenv("WORKS_CUENTAS_CONFIG", str(ruta))
    monkeypatch.delenv("WORKS_WHATSAPP_DAVID", raising=False)
    monkeypatch.delenv("WORKS_WHATSAPP_GRECIA", raising=False)


def test_numero_guardado_con_signos_y_1_coincide_con_el_de_vania(monkeypatch, tmp_path):
    _cuentas(monkeypatch, tmp_path, {"david": "+52 1 000 000 0001", "grecia": "+521-000-000-0002"})
    assert sesion.persona_por_whatsapp("520000000001") == "david"
    assert sesion.persona_por_whatsapp("520000000002") == "grecia"
    assert sesion.persona_por_whatsapp("+52 1 000 000 0001") == "david"


def test_numero_de_otro_pais_con_los_mismos_10_digitos_no_coincide(monkeypatch, tmp_path):
    _cuentas(monkeypatch, tmp_path, {"david": "+52 1 000 000 0001"})
    assert sesion.persona_por_whatsapp("10000000001") is None
    assert sesion.persona_por_whatsapp("0000000001") is None


def test_identificador_lid_o_vacio_no_coincide(monkeypatch, tmp_path):
    _cuentas(monkeypatch, tmp_path, {"david": "+52 1 000 000 0001"})
    assert sesion.persona_por_whatsapp("100000000000001") is None
    assert sesion.persona_por_whatsapp("") is None
    assert sesion.persona_por_whatsapp(None) is None
