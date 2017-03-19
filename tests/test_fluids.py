from scadasim.fluids import Water

def test_water():
    water = Water()
    assert isinstance(water.ph, float)
