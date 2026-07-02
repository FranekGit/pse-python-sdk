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

| Endpoint | Column | Method | Status |
|---|---|---|---|
| `price-cost` | `cen_cost` | `get_cen()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | `ckoeb_cost` | `get_ckoeb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | `ceb_sr_cost` | `get_ceb_sr()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | `cor_pp_cost` | `get_cor_pp()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | `imb_energy` | `get_imb_energy()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `price-cost` | `contracting` | `get_contracting()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `csdac-pln` | `csdac_pln` | `get_csdac()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `demand` | `get_demand()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `swm_p` | `get_swm_p()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `swm_np` | `get_swm_np()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jg` | `get_jg()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgw1` | `get_jgw1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgw2` | `get_jgw2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgm1` | `get_jgm1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgm2` | `get_jgm2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgz1` | `get_jgz1()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgz2` | `get_jgz2()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgz3` | `get_jgz3()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jga` | `get_jga()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgo` | `get_jgo()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jnwrb` | `get_jnwrb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `jgm` | `get_jgm()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `wi` | `get_wi()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `his-wlk-cal` | `pv` | `get_pv()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `kmb-kro-rozl` | `kmb` | `get_kmb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `kmb-kro-rozl` | `kro` | `get_kro()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | `kb` | `get_kb()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | `ko` | `get_ko()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `krb-rozl` | `kcz` | `get_kcz()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | `sk_d1_fcst` | `get_sk_d1_fcst()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | `sk_d_fcst` | `get_sk_d_fcst()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `sk` | `sk_cost` | `get_sk_cost()` | ![stable](https://img.shields.io/badge/stable-brightgreen) |
| `afrr-status` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cmbp-tp` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cmbu-tu` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `codn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cor` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cor-q-1` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `cordmax` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `crb-rozl` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi1` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi2` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi3` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi4` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi5` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi6` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi7` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi8` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi9` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `csire-kpi10` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `eb-rozl` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `en-rozl` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `energy-prices` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `gen-jw` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `his-bil-mocy` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `his-gen-pal` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-oeb-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-oeb-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-omb-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-omb-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-opmb-rmb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-ot-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-pp-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-pp-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-use-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `it-use-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `kse-load` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `lolp` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `mbp-tp` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `mbu-tu` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `oeb-bpkdbo` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-b` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-b-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d1` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d1-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d2` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d2-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d39` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-d39-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-m` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-m-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-oper` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-oper-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-r` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-r-head` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ogr-rmb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgobpkd` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgopkd` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdgsz` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pdwkseub` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pk5l-wp` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poeb-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poeb-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pomb-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `popmb-rmb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `poze-redoze` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `price-fcst` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `przeplywy-mocy` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-dost-op` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-igcc-in` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `pwm-rdn-rdb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `rcco2` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `rce-pln` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ro-prog` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `ro-rozl` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `specwezlow` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `unav-pk5l` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `use-sprz-rbb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `use-sprz-rbn` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `wsp-wrm` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `zeb-rozl` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
| `zmb` | | | ![planned](https://img.shields.io/badge/planned-yellow) |
