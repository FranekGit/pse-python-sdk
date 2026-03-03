from pse._base import BaseEndpoint, SplitMethod


class PriceCost(BaseEndpoint):
    path = "price-cost"
    method_name = "get_price_cost"
    doc = "Price and cost data from the PSE balancing market."
    splits = [
        SplitMethod("get_cen", ["cen_cost"], "CEN — settlement imbalance price"),
        SplitMethod("get_ckoeb", ["ckoeb_cost"], "CKOeB — balancing energy cost"),
        SplitMethod("get_ceb_sr", ["ceb_sr_cost"], "CEB_SR — avg balancing energy price"),
        SplitMethod("get_cor_pp", ["cor_pp_cost"], "COR_PP — premium price correction"),
        SplitMethod("get_imb_energy", ["imb_energy"], "Imbalance energy volume"),
        SplitMethod("get_contracting", ["contracting"], "Contracting direction (long/short)"),
    ]
