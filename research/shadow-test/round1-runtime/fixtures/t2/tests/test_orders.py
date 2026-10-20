import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from orders import Gateway, OrderProcessor


def test_submit_charges_once():
    g = Gateway()
    p = OrderProcessor(g)
    assert p.submit("A1", 50) is True
    assert g.charges == [("A1", 50)]


def test_resubmit_is_rejected():
    g = Gateway()
    p = OrderProcessor(g)
    p.submit("A1", 50)
    assert p.submit("A1", 50) is False
    assert len(g.charges) == 1


def test_different_orders_both_charge():
    g = Gateway()
    p = OrderProcessor(g)
    p.submit("A1", 50)
    p.submit("B2", 20)
    assert len(g.charges) == 2
