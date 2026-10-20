# Endpoints

All endpoints share the same signature:

```python
(start: str, end: str, format: OutputFormat = "dict")
```

## Common Response Columns

Every endpoint returns these columns plus endpoint-specific columns:

- `dtime` — timestamp
- `period` — period identifier
- `business_date` — business date
- `publication_ts` — publication timestamp

## Endpoints Coverage

> API reference: `https://api.raporty.pse.pl/api/openapi`

| Endpoint | Description | Column | Method | Status |
|---|---|---|---|---|
| `price-cost` | CEN price | `cen_cost` | `get_cen()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | CKOEB price | `ckoeb_cost` | `get_ckoeb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | CEBśr price | `ceb_sr_cost` | `get_ceb_sr()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | Operating reserve price (COR) | `cor_pp_cost` | `get_cor_pp()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | Imbalance energy | `imb_energy` | `get_imb_energy()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | KSE contracting status (`short` if < 0, else `long`) | `contracting` | `get_contracting()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `csdac-pln` | SDAC price (PLN) | `csdac_pln` | `get_csdac()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | KSE power demand | `demand` | `get_demand()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | National cross-border exchange balance (parallel) | `swm_p` | `get_swm_p()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | National cross-border exchange balance (non-parallel) | `swm_np` | `get_swm_np()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of scheduling units in KSE (JGw, JGm, JGz, JGa) | `jg` | `get_jg()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of generating scheduling units JGw (ZAK=1) | `jgw1` | `get_jgw1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of generating scheduling units JGw (ZAK=2) | `jgw2` | `get_jgw2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of energy storage scheduling units JGm (ZAK=1) | `jgm1` | `get_jgm1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of energy storage scheduling units JGm (ZAK=2) | `jgm2` | `get_jgm2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of wind and PV scheduling units JGz (ZAK=1) | `jgz1` | `get_jgz1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of wind and PV scheduling units JGz (ZAK=2) | `jgz2` | `get_jgz2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of wind and PV scheduling units JGz (ZAK=3) | `jgz3` | `get_jgz3()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of aggregator scheduling units (JGa) | `jga` | `get_jga()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total consumption of receiving scheduling units (JGo) | `jgo` | `get_jgo()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total generation of units not actively participating in balancing market | `jnwrb` | `get_jnwrb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total JGm charging power | `jgm` | `get_jgm()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total wind generation | `wi` | `get_wi()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | Total photovoltaic generation | `pv` | `get_pv()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `kmb-kro-rozl` | Balancing capacity cost (KMB) | `kmb` | `get_kmb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `kmb-kro-rozl` | Operating reserve cost (KRO) | `kro` | `get_kro()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | KB cost | `kb` | `get_kb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | KO cost | `ko` | `get_ko()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | KCZ cost | `kcz` | `get_kcz()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | Forecasted KSE contracting status determined on day d-1 | `sk_d1_fcst` | `get_sk_d1_fcst()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | Forecasted KSE contracting status determined on day d | `sk_d_fcst` | `get_sk_d_fcst()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | KSE contracting status | `sk_cost` | `get_sk_cost()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `afrr-status` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cmbp-tp` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cmbu-tu` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `codn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cor` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cor-q-1` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cordmax` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `crb-rozl` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi1` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi2` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi3` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi4` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi5` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi6` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi7` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi8` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi9` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi10` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `eb-rozl` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `en-rozl` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `energy-prices` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `gen-jw` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `his-bil-mocy` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `his-gen-pal` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-oeb-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-oeb-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-omb-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-omb-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-opmb-rmb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-ot-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-pp-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-pp-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-use-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-use-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `kse-load` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `lolp` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `mbp-tp` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `mbu-tu` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `oeb-bpkdbo` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-b` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-b-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d1` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d1-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d2` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d2-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d39` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d39-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-m` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-m-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-oper` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-oper-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-r` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-r-head` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-rmb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgobpkd` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgopkd` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgsz` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdwkseub` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pk5l-wp` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poeb-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poeb-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pomb-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `popmb-rmb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poze-redoze` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `price-fcst` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `przeplywy-mocy` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-dost-op` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-igcc-in` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdn-rdb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `rcco2` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `rce-pln` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ro-prog` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ro-rozl` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `specwezlow` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `unav-pk5l` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `use-sprz-rbb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `use-sprz-rbn` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `wsp-wrm` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `zeb-rozl` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `zmb` | | | | ![planned](https://img.shields.io/badge/planned-yellow) |
