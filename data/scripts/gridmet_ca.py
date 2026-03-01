import xarray as xr

ds = xr.open_dataset("gridmet_ca/vpd_2018.nc")
print(ds)
print(dict(ds.dims))
# Should see lat ~235, lon ~26, day 365
