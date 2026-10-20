# Endpoints

## `fetch()`

Any endpoint can be queried by name:

```python
fetch(endpoint: Endpoint, start: str, end: str, *,
      columns: list[str] | None = None, format: OutputFormat = "dict")
```

- `columns=None` returns all columns.
- `columns=[...]` returns these columns plus the endpoint's meta columns
  (`dtime`, `period`, `business_date`, `publication_ts` and their `*_utc`
  variants, where present) and key columns (e.g. `resource_code` on `gen-jw`),
  so every row stays identifiable.
- Rows are filtered on `business_date`.
- `ogr-*-head` endpoints have no date column and are not supported yet.

## Endpoints Coverage

> API reference: `https://api.raporty.pse.pl/api/openapi`

| Endpoint | Column | Description |
|---|---|---|
| `price-cost` | `cen_cost` | CEN price |
| `price-cost` | `ckoeb_cost` | CKOEB price |
| `price-cost` | `ceb_sr_cost` | CEBśr price |
| `price-cost` | `cor_pp_cost` | Operating reserve price (COR) |
| `price-cost` | `imb_energy` | Imbalance energy |
| `price-cost` | `contracting` | KSE contracting status (`short` if < 0, else `long`) |
| `csdac-pln` | `csdac_pln` | SDAC price (PLN) |
| `his-wlk-cal` | `demand` | KSE power demand |
| `his-wlk-cal` | `swm_p` | National cross-border exchange balance (parallel) |
| `his-wlk-cal` | `swm_np` | National cross-border exchange balance (non-parallel) |
| `his-wlk-cal` | `jg` | Total generation of scheduling units in KSE (JGw, JGm, JGz, JGa) |
| `his-wlk-cal` | `jgw1` | Total generation of generating scheduling units JGw (ZAK=1) |
| `his-wlk-cal` | `jgw2` | Total generation of generating scheduling units JGw (ZAK=2) |
| `his-wlk-cal` | `jgm1` | Total generation of energy storage scheduling units JGm (ZAK=1) |
| `his-wlk-cal` | `jgm2` | Total generation of energy storage scheduling units JGm (ZAK=2) |
| `his-wlk-cal` | `jgz1` | Total generation of wind and PV scheduling units JGz (ZAK=1) |
| `his-wlk-cal` | `jgz2` | Total generation of wind and PV scheduling units JGz (ZAK=2) |
| `his-wlk-cal` | `jgz3` | Total generation of wind and PV scheduling units JGz (ZAK=3) |
| `his-wlk-cal` | `jga` | Total generation of aggregator scheduling units (JGa) |
| `his-wlk-cal` | `jgo` | Total consumption of receiving scheduling units (JGo) |
| `his-wlk-cal` | `jnwrb` | Total generation of units not actively participating in balancing market |
| `his-wlk-cal` | `jgm` | Total JGm charging power |
| `his-wlk-cal` | `wi` | Total wind generation |
| `his-wlk-cal` | `pv` | Total photovoltaic generation |
| `kmb-kro-rozl` | `kmb` | Balancing capacity cost (KMB) |
| `kmb-kro-rozl` | `kro` | Operating reserve cost (KRO) |
| `krb-rozl` | `kb` | KB cost |
| `krb-rozl` | `ko` | KO cost |
| `krb-rozl` | `kcz` | KCZ cost |
| `sk` | `sk_d1_fcst` | Forecasted KSE contracting status determined on day d-1 |
| `sk` | `sk_d_fcst` | Forecasted KSE contracting status determined on day d |
| `sk` | `sk_cost` | KSE contracting status |
| `afrr-status` | | |
| `cmbp-tp` | | |
| `cmbu-tu` | | |
| `codn` | | |
| `cor` | | |
| `cor-q-1` | | |
| `cordmax` | | |
| `crb-rozl` | | |
| `csire-kpi1` | | |
| `csire-kpi2` | | |
| `csire-kpi3` | | |
| `csire-kpi4` | | |
| `csire-kpi5` | | |
| `csire-kpi6` | | |
| `csire-kpi7` | | |
| `csire-kpi8` | | |
| `csire-kpi9` | | |
| `csire-kpi10` | | |
| `eb-rozl` | | |
| `en-rozl` | | |
| `energy-prices` | | |
| `gen-jw` | | |
| `his-bil-mocy` | | |
| `his-gen-pal` | | |
| `it-oeb-rbb` | | |
| `it-oeb-rbn` | | |
| `it-omb-rbb` | | |
| `it-omb-rbn` | | |
| `it-opmb-rmb` | | |
| `it-ot-rbn` | | |
| `it-pp-rbb` | | |
| `it-pp-rbn` | | |
| `it-use-rbb` | | |
| `it-use-rbn` | | |
| `kse-load` | | |
| `lolp` | | |
| `mbp-tp` | | |
| `mbu-tu` | | |
| `oeb-bpkdbo` | | |
| `ogr-b` | | |
| `ogr-b-head` | | |
| `ogr-d1` | | |
| `ogr-d1-head` | | |
| `ogr-d2` | | |
| `ogr-d2-head` | | |
| `ogr-d39` | | |
| `ogr-d39-head` | | |
| `ogr-m` | | |
| `ogr-m-head` | | |
| `ogr-oper` | | |
| `ogr-oper-head` | | |
| `ogr-r` | | |
| `ogr-r-head` | | |
| `ogr-rmb` | | |
| `pdgobpkd` | | |
| `pdgopkd` | | |
| `pdgsz` | | |
| `pdwkseub` | | |
| `pk5l-wp` | | |
| `poeb-rbb` | | |
| `poeb-rbn` | | |
| `pomb-rbn` | | |
| `popmb-rmb` | | |
| `poze-redoze` | | |
| `price-fcst` | | |
| `przeplywy-mocy` | | |
| `pwm-dost-op` | | |
| `pwm-igcc-in` | | |
| `pwm-rdb` | | |
| `pwm-rdn` | | |
| `pwm-rdn-rdb` | | |
| `rcco2` | | |
| `rce-pln` | | |
| `ro-prog` | | |
| `ro-rozl` | | |
| `specwezlow` | | |
| `unav-pk5l` | | |
| `use-sprz-rbb` | | |
| `use-sprz-rbn` | | |
| `wsp-wrm` | | |
| `zeb-rozl` | | |
| `zmb` | | |
